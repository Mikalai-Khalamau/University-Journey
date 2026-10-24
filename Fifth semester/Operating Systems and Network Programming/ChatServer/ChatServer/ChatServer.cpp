#include "Protocol.h"
#include <vector>
#include <thread>
#include <mutex>
#include <memory>

struct ClientInfo {
    std::string name;
    HANDLE hPipe;
    DWORD pid;
    std::mutex writeMtx; 
};

std::mutex clientsMutex;
std::vector<std::shared_ptr<ClientInfo>> activeClients;

static bool SendTo(const std::shared_ptr<ClientInfo>& c, const ChatMessage& m) {
    std::lock_guard<std::mutex> lk(c->writeMtx);
    return PipeWrite(c->hPipe, &m, sizeof(ChatMessage));
}

void ClientHandler(HANDLE hPipe) {
    DWORD serverPid = GetCurrentProcessId();
    ChatMessage msg{};

    if (!PipeRead(hPipe, &msg, sizeof(msg)) || msg.messageType != MSG_HELLO) {
        DisconnectNamedPipe(hPipe);
        CloseHandle(hPipe);
        return;
    }
    msg.sender[sizeof(msg.sender) - 1] = 0;

    auto me = std::make_shared<ClientInfo>();
    me->name = msg.sender;
    me->hPipe = hPipe;
    me->pid = msg.sourcePid;
    PrintLog(msg.sourcePid, "RECEIVE", msg.requestId, "HELLO", msg.payloadSize);

    {
        std::lock_guard<std::mutex> lk(clientsMutex);
        activeClients.push_back(me);
    }

    ChatMessage reply{};
    reply.version = 1;
    reply.messageType = MSG_HELLO_OK;
    reply.sourcePid = serverPid;
    reply.requestId = msg.requestId;
    strncpy_s(reply.text, "Registered successfully", _TRUNCATE);
    reply.payloadSize = (uint32_t)strlen(reply.text);
    SendTo(me, reply);
    PrintLog(serverPid, "SEND", reply.requestId, "HELLO_OK", reply.payloadSize);

    while (PipeRead(hPipe, &msg, sizeof(msg))) {
        msg.sender[sizeof(msg.sender) - 1] = 0;
        msg.receiver[sizeof(msg.receiver) - 1] = 0;
        msg.text[sizeof(msg.text) - 1] = 0;

        if (msg.messageType == MSG_BENCHMARK) {
            msg.messageType = MSG_BENCHMARK_ACK;
            SendTo(me, msg);
            continue;
        }
        if (msg.messageType == MSG_STOP) {
            PrintLog(msg.sourcePid, "RECEIVE", msg.requestId, "STOP", msg.payloadSize);
            break;
        }
        PrintLog(msg.sourcePid, "RECEIVE", msg.requestId, "CHAT", msg.payloadSize);

        std::shared_ptr<ClientInfo> target;
        {
            std::lock_guard<std::mutex> lk(clientsMutex);
            for (auto& c : activeClients)
                if (c->name == msg.receiver) { target = c; break; }
        }

        ChatMessage resp{};
        resp.version = 1;
        resp.sourcePid = serverPid;
        resp.requestId = msg.requestId;

        if (target && SendTo(target, msg)) {
            PrintLog(serverPid, "SEND", msg.requestId, "CHAT", msg.payloadSize);
            resp.messageType = MSG_CHAT_ACK;
            strncpy_s(resp.text, "Delivered", _TRUNCATE);
        }
        else {
            resp.messageType = MSG_ERROR;
            sprintf_s(resp.text, "Error: User '%s' not found!", msg.receiver);
        }
        resp.payloadSize = (uint32_t)strlen(resp.text);
        SendTo(me, resp);
    }

    std::cout << "[INFO] Client " << me->name << " disconnected.\n";
    {
        std::lock_guard<std::mutex> lk(clientsMutex);
        for (auto it = activeClients.begin(); it != activeClients.end(); ++it)
            if (*it == me) { activeClients.erase(it); break; }
    }
    DisconnectNamedPipe(hPipe);
    CloseHandle(hPipe);
}

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    std::cout << "SERVER | PID=" << GetCurrentProcessId()
        << " | VARIANT=27 | STUDENT_ID=" << STUDENT_ID << std::endl;

    while (true) {
        HANDLE hPipe = CreateNamedPipeW(PIPE_NAME,
            PIPE_ACCESS_DUPLEX | FILE_FLAG_OVERLAPPED,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            PIPE_UNLIMITED_INSTANCES, sizeof(ChatMessage), sizeof(ChatMessage), 0, NULL);
        if (hPipe == INVALID_HANDLE_VALUE) { PrintWinError("CreateNamedPipeW"); break; }

        OVERLAPPED ov{};
        ov.hEvent = CreateEventW(NULL, TRUE, FALSE, NULL);
        DWORD n = 0;
        BOOL ok = ConnectNamedPipe(hPipe, &ov);
        DWORD err = GetLastError();
        if (!ok && err == ERROR_IO_PENDING)
            ok = GetOverlappedResult(hPipe, &ov, &n, TRUE);
        else if (!ok && err == ERROR_PIPE_CONNECTED)
            ok = TRUE;
        CloseHandle(ov.hEvent);

        if (ok) std::thread(ClientHandler, hPipe).detach();
        else CloseHandle(hPipe);
    }
}
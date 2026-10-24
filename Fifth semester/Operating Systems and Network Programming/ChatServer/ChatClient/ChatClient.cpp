#include "Protocol.h"
#include <thread>
#include <atomic>
#include <limits>
#include <ios>

std::atomic<bool> running(true);

void RunBenchmarkRTT(HANDLE hPipe, size_t messageSize, int totalMessages = 1000) {
    ChatMessage msg{};
    msg.version = 1;
    msg.messageType = MSG_BENCHMARK;
    msg.sourcePid = GetCurrentProcessId();
    strcpy_s(msg.sender, "BenchWorker");
    size_t copySize = (messageSize < sizeof(msg.text)) ? messageSize : sizeof(msg.text);
    msg.payloadSize = static_cast<uint32_t>(copySize);

    std::cout << "\n[BENCHMARK] Running test: " << totalMessages << " msgs, size = " << messageSize << " bytes...\n";

    LARGE_INTEGER frequency, start, end;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start);

    for (int i = 0; i < totalMessages; ++i) {
        msg.requestId = i + 1;
        if (!PipeWrite(hPipe, &msg, sizeof(ChatMessage))) break;
        ChatMessage reply;
        if (!PipeRead(hPipe, &reply, sizeof(ChatMessage))) break;
    }

    QueryPerformanceCounter(&end);
    double elapsedTime = static_cast<double>(end.QuadPart - start.QuadPart) / frequency.QuadPart;
    double msgsPerSec = totalMessages / elapsedTime;

    std::cout << ">>> RESULTS -> Time: " << elapsedTime << " sec | Speed: " << msgsPerSec << " msgs/sec <<<\n\n";
}

void ReceiverThread(HANDLE hPipe) {
    ChatMessage m;
    while (running && PipeRead(hPipe, &m, sizeof(m))) {
        m.sender[sizeof(m.sender) - 1] = 0;
        m.text[sizeof(m.text) - 1] = 0;
        switch (m.messageType) {
        case MSG_CHAT:
            std::cout << "\n[" << m.sender << "]: " << m.text << "\n> ";
            break;
        case MSG_CHAT_ACK:
            std::cout << "\n[OK] Delivered\n> ";
            break;
        case MSG_ERROR:
            std::cout << "\n[SERVER ERROR]: " << m.text << "\n> ";
            break;
        }
    }
}

int main(int argc, char* argv[]) {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    int runId = (argc > 1) ? std::stoi(argv[1]) : 113;
    DWORD pid = GetCurrentProcessId();

    std::string clientName;
    std::cout << "Enter your unique client name: ";
    std::cin >> clientName;

    (std::cin.ignore)((std::numeric_limits<std::streamsize>::max)(), '\n');

    std::cout << "CLIENT | PID=" << pid << " | VARIANT=27 | RUN_ID=" << runId << " | NAME=" << clientName << std::endl;

    HANDLE hPipe = INVALID_HANDLE_VALUE;
    while (running) {
        hPipe = CreateFileW(PIPE_NAME, GENERIC_READ | GENERIC_WRITE, 0, NULL,
            OPEN_EXISTING, FILE_FLAG_OVERLAPPED, NULL);
        if (hPipe != INVALID_HANDLE_VALUE) break;
        if (GetLastError() == ERROR_PIPE_BUSY) {
            WaitNamedPipeW(PIPE_NAME, 2000);
        }
        else {
            Sleep(500);
        }
    }

    ChatMessage helloMsg{};
    helloMsg.version = 1;
    helloMsg.messageType = MSG_HELLO;
    helloMsg.sourcePid = pid;
    helloMsg.requestId = 1;
    strncpy_s(helloMsg.sender, clientName.c_str(), _TRUNCATE);
    helloMsg.payloadSize = (uint32_t)strlen(helloMsg.sender);

    PipeWrite(hPipe, &helloMsg, sizeof(ChatMessage));

    ChatMessage reply;
    PipeRead(hPipe, &reply, sizeof(ChatMessage));

    RunBenchmarkRTT(hPipe, 64, 1000);
    RunBenchmarkRTT(hPipe, 4096, 1000);

    std::thread receiver(ReceiverThread, hPipe);

    std::cout << "\n========================================\n";
    std::cout << "Chat is ready! Format: <ReceiverName> <Text>\n";
    std::cout << "Type EXIT to quit.\n";
    std::cout << "========================================\n\n> ";

    std::string line;
    uint32_t reqId = 10;

    while (running) {
        if (!std::getline(std::cin, line)) break;
        if (line.empty()) { std::cout << "> "; continue; }
        if (line == "EXIT") {
            running = false;
            break;
        }

        size_t spacePos = line.find(' ');
        std::string receiver, text;

        if (spacePos == std::string::npos) {
            std::cout << "[ERROR] Wrong format! Use: <Receiver> <Text>\n> ";
            continue;
        }

        receiver = line.substr(0, spacePos);
        text = line.substr(spacePos + 1);

        ChatMessage chatMsg{};
        chatMsg.version = 1;
        chatMsg.messageType = MSG_CHAT;
        chatMsg.sourcePid = pid;
        chatMsg.requestId = reqId++;
        strncpy_s(chatMsg.sender, clientName.c_str(), _TRUNCATE);
        strncpy_s(chatMsg.receiver, receiver.c_str(), _TRUNCATE);
        strncpy_s(chatMsg.text, text.c_str(), _TRUNCATE);
        chatMsg.payloadSize = (uint32_t)strlen(chatMsg.text);

        if (!PipeWrite(hPipe, &chatMsg, sizeof(ChatMessage))) {
            PrintWinError("PipeWrite (Chat)");
            break;
        }
    }

    running = false;
    ChatMessage stop{};
    stop.version = 1;
    stop.messageType = MSG_STOP;
    stop.sourcePid = pid;
    PipeWrite(hPipe, &stop, sizeof(stop));

    CancelIoEx(hPipe, NULL);
    if (receiver.joinable()) {
        receiver.join();
    }
    CloseHandle(hPipe);
    return 0;
}
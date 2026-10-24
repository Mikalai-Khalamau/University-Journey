#pragma once
#include <iostream>
#include <string>
#include <windows.h>
#include <cstdint>

#define PIPE_NAME L"\\\\.\\pipe\\ChatVariant27Pipe"
#define STUDENT_ID 113
#define MAX_TEXT_LEN (1024 + STUDENT_ID)

enum MessageType : uint32_t {
    MSG_HELLO = 1,
    MSG_HELLO_OK,
    MSG_CHAT,
    MSG_ERROR,
    MSG_STOP,
    MSG_BENCHMARK,
    MSG_BENCHMARK_ACK,
    MSG_CHAT_ACK        
};

struct ChatMessage {
    uint32_t version;
    uint32_t messageType;
    uint32_t sourcePid;
    uint32_t requestId;
    uint32_t payloadSize;
    char sender[64];
    char receiver[64];
    char text[MAX_TEXT_LEN];
};

inline bool PipeWrite(HANDLE h, const void* buf, DWORD size) {
    OVERLAPPED ov{};
    ov.hEvent = CreateEventW(NULL, TRUE, FALSE, NULL);
    DWORD n = 0;
    BOOL ok = WriteFile(h, buf, size, NULL, &ov);
    if (ok || GetLastError() == ERROR_IO_PENDING)
        ok = GetOverlappedResult(h, &ov, &n, TRUE);
    CloseHandle(ov.hEvent);
    return ok && n == size;
}

inline bool PipeRead(HANDLE h, void* buf, DWORD size) {
    OVERLAPPED ov{};
    ov.hEvent = CreateEventW(NULL, TRUE, FALSE, NULL);
    DWORD n = 0;
    BOOL ok = ReadFile(h, buf, size, NULL, &ov);
    if (ok || GetLastError() == ERROR_IO_PENDING)
        ok = GetOverlappedResult(h, &ov, &n, TRUE);
    CloseHandle(ov.hEvent);
    return ok && n > 0;
}

inline void PrintWinError(const std::string& funcName) {
    DWORD errCode = GetLastError();
    LPVOID lpMsgBuf = nullptr;
    FormatMessageA(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL, errCode, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPSTR)&lpMsgBuf, 0, NULL
    );
    std::cerr << "[ERROR] " << funcName << " | Code: " << errCode << " | " << (lpMsgBuf ? (LPSTR)lpMsgBuf : "") << std::endl;
    if (lpMsgBuf) LocalFree(lpMsgBuf);
}

inline void PrintLog(uint32_t pid, const std::string& action, uint32_t reqId, const std::string& typeStr, uint32_t size) {
    SYSTEMTIME st;
    GetLocalTime(&st);
    printf("[%02d:%02d:%02d.%03d]\nPID=%u\n%s\nrequestId=%u\ntype=%s\nsize=%u\n\n",
        st.wHour, st.wMinute, st.wSecond, st.wMilliseconds,
        pid, action.c_str(), reqId, typeStr.c_str(), size);
}
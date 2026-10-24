#pragma once

#include <windows.h>
#include <iostream>
#include <string>
#include <vector>

inline void PrintLastError(const std::wstring& operationName) {
    DWORD errorCode = ::GetLastError();
    LPWSTR messageBuffer = nullptr;

    size_t size = FormatMessageW(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL,
        errorCode,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPWSTR)&messageBuffer,
        0,
        NULL
    );

    std::wstring message = (size > 0 && messageBuffer) ? std::wstring(messageBuffer, size) : L"Unknown error";
    if (messageBuffer) LocalFree(messageBuffer);

    std::wcerr << L"[ОШИБКА WinAPI] Операция: " << operationName
        << L" | Код ошибки: " << errorCode
        << L" | Описание: " << message << std::endl;
}

class Timer {
public:
    Timer() {
        QueryPerformanceFrequency(&frequency_);
        Reset();
    }

    void Reset() {
        QueryPerformanceCounter(&startTime_);
    }

    double GetElapsedMilliseconds() const {
        LARGE_INTEGER endTime;
        QueryPerformanceCounter(&endTime);
        return static_cast<double>(endTime.QuadPart - startTime_.QuadPart) * 1000.0 / frequency_.QuadPart;
    }

private:
    LARGE_INTEGER frequency_;
    LARGE_INTEGER startTime_;
};
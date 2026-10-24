#pragma once
#include <windows.h>
#include <vector>
#include <string>
#include <iostream>

struct AsyncFileInfo {
    HANDLE hFile = INVALID_HANDLE_VALUE;
    OVERLAPPED overlapped = { 0 };
    LARGE_INTEGER fileSize = { 0 };
    LARGE_INTEGER currentOffset = { 0 };
    std::wstring fileName;
    bool isCompleted = false;
};

class AsyncIoManager {
private:
    double lastExecutionTimeMs = 0.0;

public:
    AsyncIoManager() = default;
    ~AsyncIoManager() = default;

    bool ReadFilesAsync(const std::vector<std::wstring>& filePaths, DWORD blockSize);
    double GetLastExecutionTimeMs() const { return lastExecutionTimeMs; }
};
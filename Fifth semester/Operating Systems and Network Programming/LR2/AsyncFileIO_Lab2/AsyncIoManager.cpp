#include "AsyncIoManager.h"
#include "Utils.h"
#include <iomanip>

bool AsyncIoManager::ReadFilesAsync(const std::vector<std::wstring>& filePaths, DWORD blockSize) {
    size_t fileCount = filePaths.size();
    if (fileCount == 0) return false;

    std::vector<AsyncFileInfo> files(fileCount);
    std::vector<HANDLE> events;
    std::vector<BYTE*> buffers(fileCount, nullptr);

    // 1. Открытие файлов и инициализация
    for (size_t i = 0; i < fileCount; ++i) {
        files[i].fileName = filePaths[i];

        files[i].hFile = CreateFileW(
            filePaths[i].c_str(),
            GENERIC_READ,
            FILE_SHARE_READ,
            NULL,
            OPEN_EXISTING,
            FILE_FLAG_OVERLAPPED | FILE_FLAG_NO_BUFFERING,
            NULL
        );

        if (files[i].hFile == INVALID_HANDLE_VALUE) {
            PrintLastError(L"CreateFileW (Чтение)");
            for (size_t j = 0; j < i; ++j) {
                if (files[j].overlapped.hEvent) CloseHandle(files[j].overlapped.hEvent);
                if (files[j].hFile != INVALID_HANDLE_VALUE) CloseHandle(files[j].hFile);
                if (buffers[j]) VirtualFree(buffers[j], 0, MEM_RELEASE);
            }
            return false;
        }

        GetFileSizeEx(files[i].hFile, &files[i].fileSize);
        files[i].overlapped.hEvent = CreateEvent(NULL, TRUE, FALSE, NULL);
        events.push_back(files[i].overlapped.hEvent);

        buffers[i] = static_cast<BYTE*>(VirtualAlloc(NULL, blockSize, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE));

        files[i].overlapped.Offset = 0;
        files[i].overlapped.OffsetHigh = 0;

        BOOL readResult = ReadFile(files[i].hFile, buffers[i], blockSize, NULL, &files[i].overlapped);
        if (!readResult && GetLastError() != ERROR_IO_PENDING) {
            PrintLastError(L"ReadFile (Начальное чтение)");
            return false;
        }
    }

    Timer timer;
    size_t activeFiles = fileCount;

    std::vector<size_t> blockCounters(fileCount, 0);
    const size_t MAX_BLOCKS_TO_SHOW = 5; 

    // 2. Основной цикл асинхронного чтения
    while (activeFiles > 0) {
        DWORD dwWait = WaitForMultipleObjects(static_cast<DWORD>(events.size()), events.data(), FALSE, INFINITE);

        if (dwWait >= WAIT_OBJECT_0 && dwWait < WAIT_OBJECT_0 + events.size()) {
            size_t idx = dwWait - WAIT_OBJECT_0;

            if (files[idx].isCompleted) continue;

            DWORD bytesRead = 0;
            if (GetOverlappedResult(files[idx].hFile, &files[idx].overlapped, &bytesRead, TRUE)) {
                files[idx].currentOffset.QuadPart += bytesRead;
                blockCounters[idx]++;

                bool isDataValid = (bytesRead > 0 && buffers[idx][0] == 'A');

                bool shouldShow = (blockCounters[idx] <= MAX_BLOCKS_TO_SHOW) ||
                    (files[idx].currentOffset.QuadPart >= files[idx].fileSize.QuadPart);

                if (shouldShow) {
                    double currentTimeMs = timer.GetElapsedMilliseconds();
                    std::wcout << L"   [" << files[idx].fileName
                        << L"] " << (isDataValid ? L"OK" : L"WARN")
                        << L" блок #" << blockCounters[idx]
                        << L" " << bytesRead << L" байт"
                        << L" | прогресс: " << files[idx].currentOffset.QuadPart
                        << L"/" << files[idx].fileSize.QuadPart
                        << L" | время: " << std::fixed << std::setprecision(1) << currentTimeMs << L" мс\n";
                }

                ResetEvent(files[idx].overlapped.hEvent);

                if (files[idx].currentOffset.QuadPart >= files[idx].fileSize.QuadPart) {
                    files[idx].isCompleted = true;
                    activeFiles--;

                    if (blockCounters[idx] > MAX_BLOCKS_TO_SHOW) {
                        double currentTimeMs = timer.GetElapsedMilliseconds();
                        std::wcout << L"   [" << files[idx].fileName
                            << L"] ... (пропущено " << (blockCounters[idx] - MAX_BLOCKS_TO_SHOW - 1)
                            << L" блоков) ... ЗАВЕРШЕН за "
                            << std::fixed << std::setprecision(1) << currentTimeMs << L" мс\n";
                    }
                }
                else {
                    files[idx].overlapped.Offset = files[idx].currentOffset.LowPart;
                    files[idx].overlapped.OffsetHigh = files[idx].currentOffset.HighPart;

                    BOOL nextReadResult = ReadFile(files[idx].hFile, buffers[idx], blockSize, NULL, &files[idx].overlapped);
                    if (!nextReadResult && GetLastError() != ERROR_IO_PENDING) {
                        PrintLastError(L"ReadFile (Последующее чтение)");
                        return false;
                    }
                }
            }
            else {
                PrintLastError(L"GetOverlappedResult");
                return false;
            }
        }
    }

    lastExecutionTimeMs = timer.GetElapsedMilliseconds();

    // 3. Закрытие ресурсов
    for (size_t i = 0; i < fileCount; ++i) {
        if (files[i].overlapped.hEvent) CloseHandle(files[i].overlapped.hEvent);
        if (files[i].hFile != INVALID_HANDLE_VALUE) CloseHandle(files[i].hFile);
        if (buffers[i]) VirtualFree(buffers[i], 0, MEM_RELEASE);
    }

    return true;
}
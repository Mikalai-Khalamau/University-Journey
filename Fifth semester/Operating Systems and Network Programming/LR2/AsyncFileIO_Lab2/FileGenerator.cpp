#include "FileGenerator.h"
#include "Utils.h"
#include <vector>
#include <iostream>

namespace FileGenerator {

    bool CreateTestFile(const std::wstring& filePath, size_t sizeInMB) {
        std::wcout << L"[Генерация] Создание файла: " << filePath << L" (" << sizeInMB << L" МБ)..." << std::endl;

        HANDLE hFile = CreateFileW(
            filePath.c_str(),
            GENERIC_WRITE,
            0,
            NULL,
            CREATE_ALWAYS,
            FILE_ATTRIBUTE_NORMAL,
            NULL
        );

        if (hFile == INVALID_HANDLE_VALUE) {
            PrintLastError(L"CreateFileW (Генерация тестового файла)");
            return false;
        }

        const DWORD chunkSize = 1024 * 1024; 
        std::vector<char> buffer(chunkSize, 'A');

        DWORD bytesWritten = 0;
        for (size_t i = 0; i < sizeInMB; ++i) {
            if (!WriteFile(hFile, buffer.data(), chunkSize, &bytesWritten, NULL)) {
                PrintLastError(L"WriteFile (Генерация тестового файла)");
                CloseHandle(hFile);
                return false;
            }
        }

        FlushFileBuffers(hFile);
        CloseHandle(hFile);
        std::wcout << L"[Генерация] Успешно создан: " << filePath << std::endl;
        return true;
    }

} 
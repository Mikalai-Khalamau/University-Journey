#include <windows.h>
#include <iostream>
#include <vector>
#include <sstream>
#include <string>
#include <iomanip>
#include "AsyncIoManager.h"
#include "FileGenerator.h"

const std::vector<size_t> FILE_SIZES_MB = { 10, 100, 500 };
const std::vector<DWORD> BLOCK_SIZES = { 4096, 65536, 1048576, 4194304 };
const int RUNS_PER_COMBINATION = 3;

const std::vector<std::wstring> BASE_FILES = {
    L"test_file_1.dat",
    L"test_file_2.dat",
    L"test_file_3.dat",
    L"test_file_4.dat"
};

struct ExperimentResult {
    size_t fileSizeMB;     
    DWORD blockSize;
    double avgTimeMs;
    double speedMBps;
};

void PrintTable(const std::vector<ExperimentResult>& results) {
    std::wcout << L"\n\n";

    const int col1Width = 16;  
    const int col2Width = 16;  
    const int col3Width = 16;  
    const int col4Width = 16; 

    std::wstring separator = L"+" + std::wstring(col1Width, L'-') + L"+"
        + std::wstring(col2Width, L'-') + L"+"
        + std::wstring(col3Width, L'-') + L"+"
        + std::wstring(col4Width, L'-') + L"+";

    std::wcout << separator << L"\n";
    std::wcout << L"| " << std::setw(col1Width - 2) << std::left << L"Размер файла"
        << L"| " << std::setw(col2Width - 2) << std::left << L"Размер блока"
        << L"| " << std::setw(col3Width - 2) << std::left << L"Время (мс)"
        << L"| " << std::setw(col4Width - 2) << std::left << L"Скорость" << L"|\n";

    std::wcout << L"| " << std::setw(col1Width - 2) << std::left << L"(1 файл)"
        << L"| " << std::setw(col2Width - 2) << std::left << L"(байт)"
        << L"| " << std::setw(col3Width - 2) << std::left << L"(среднее)"
        << L"| " << std::setw(col4Width - 2) << std::left << L"(МБ/с)" << L"|\n";

    std::wcout << separator << L"\n";

    for (const auto& r : results) {
        std::wstringstream ssSize, ssBlock, ssTime, ssSpeed;

        ssSize << r.fileSizeMB << L" МБ";
        ssBlock << r.blockSize;
        ssTime << std::fixed << std::setprecision(2) << r.avgTimeMs;
        ssSpeed << std::fixed << std::setprecision(2) << r.speedMBps;

        std::wcout << L"| " << std::setw(col1Width - 2) << std::left << ssSize.str()
            << L"| " << std::setw(col2Width - 2) << std::left << ssBlock.str()
            << L"| " << std::setw(col3Width - 2) << std::left << ssTime.str()
            << L"| " << std::setw(col4Width - 2) << std::left << ssSpeed.str() << L"|\n";
    }

    std::wcout << separator << L"\n";
    std::wcout << L"\nПримечание: Скорость рассчитана для общего объема (4 файла)\n";
}

int main() {
    SetConsoleOutputCP(1251);
    SetConsoleCP(1251);
    std::wcout.imbue(std::locale(""));

    std::wcout.flush();

    std::wcout << L"\n[DEBUG] Начало экспериментов..." << std::endl;
    std::wcout.flush();

    std::vector<ExperimentResult> allResults;

    for (size_t fileSizeMB : FILE_SIZES_MB) {
        std::wcout << L"\n------------------------------------------------------------" << std::endl;
        std::wcout << L"[GEN] Генерация 4 файлов по " << fileSizeMB << L" МБ..." << std::endl;
        std::wcout.flush();

        bool generationSuccess = true;
        for (const auto& fileName : BASE_FILES) {
            if (!FileGenerator::CreateTestFile(fileName, fileSizeMB)) {
                std::wcout << L"[ERROR] Ошибка генерации файла: " << fileName << std::endl;
                generationSuccess = false;
                break;
            }
        }

        if (!generationSuccess) {
            std::wcout << L"[WARN] Пропускаем размер " << fileSizeMB << L" МБ" << std::endl;
            continue;
        }

        std::wcout << L"[OK] Файлы успешно созданы" << std::endl;
        std::wcout.flush();

        for (DWORD blockSize : BLOCK_SIZES) {
            std::wcout << L"\n[TEST] Размер файла=" << fileSizeMB
                << L" МБ, блок=" << blockSize << L" байт" << std::endl;
            std::wcout.flush();

            std::vector<double> times;

            for (int run = 1; run <= RUNS_PER_COMBINATION; ++run) {
                std::wcout << L"   Прогон " << run << L"/" << RUNS_PER_COMBINATION << L"..." << std::endl;
                std::wcout.flush();

                AsyncIoManager manager;
                if (manager.ReadFilesAsync(BASE_FILES, blockSize)) {
                    double timeMs = manager.GetLastExecutionTimeMs();
                    times.push_back(timeMs);
                    std::wcout << L"   [Прогон " << run << L" завершен] "
                        << std::fixed << std::setprecision(2) << timeMs << L" мс" << std::endl;
                }
                else {
                    std::wcout << L"   [ERROR] Ошибка чтения" << std::endl;
                    break;
                }
            }

            if (times.size() == RUNS_PER_COMBINATION) {
                double sumTime = 0;
                for (double t : times) sumTime += t;
                double avgTime = sumTime / times.size();

                double totalSizeMB = static_cast<double>(fileSizeMB) * 4.0;
                double speedMBps = (totalSizeMB * 1000.0) / avgTime; 

                ExperimentResult result;
                result.fileSizeMB = fileSizeMB;  
                result.blockSize = blockSize;
                result.avgTimeMs = avgTime;
                result.speedMBps = speedMBps;
                allResults.push_back(result);

                std::wcout << L"   [RESULT] Среднее: " << std::fixed << std::setprecision(2) << avgTime
                    << L" мс, Скорость: " << speedMBps << L" МБ/с" << std::endl;
            }
        }
    }

    std::wcout << L"  ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ" << std::endl;

    if (!allResults.empty()) {
        PrintTable(allResults);
    }
    else {
        std::wcout << L"\n[ERROR] Не удалось получить результаты экспериментов" << std::endl;
    }

    std::wcout << L"\nНажмите Enter для выхода...";
    std::wcin.get();
    std::wcin.get();

    return 0;
}
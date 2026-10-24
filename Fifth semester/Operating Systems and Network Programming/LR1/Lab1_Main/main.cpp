#include <windows.h>
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <numeric>
#include <algorithm>
#include <fstream>

struct BenchmarkResult {
    int count;
    double totalTimeMs;
    double avgTimePerObjectUs;
};

// Высокоточный таймер
double GetTimeInMicroseconds() {
    LARGE_INTEGER frequency, counter;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&counter);
    return (static_cast<double>(counter.QuadPart) * 1000000.0) / static_cast<double>(frequency.QuadPart);
}

// Обработка ошибок WinAPI
void PrintLastError(const std::string& operationName) {
    DWORD errorCode = GetLastError();
    LPSTR messageBuffer = nullptr;

    DWORD size = FormatMessageA(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL, errorCode, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPSTR)&messageBuffer, 0, NULL
    );

    std::cerr << "[ОШИБКА] Операция: " << operationName << " | Код: " << errorCode << "\n";
    if (size > 0 && messageBuffer != nullptr) {
        std::cerr << "         Описание: " << messageBuffer;
        LocalFree(messageBuffer);
    }
}

// Расчет медианы
double CalculateMedian(std::vector<double> values) {
    std::sort(values.begin(), values.end());
    return values[values.size() / 2];
}

// Минимальная функция потока
DWORD WINAPI DummyThread(LPVOID) { return 0; }

// Бенчмарк Потоков
BenchmarkResult BenchmarkThreads(int count, bool showDetails) {
    if (showDetails) {
        std::cout << "  Тестирование потоков (CreateThread), N = " << count << "\n";
    }

    double startTime = GetTimeInMicroseconds();

    for (int i = 1; i <= count; ++i) {
        DWORD threadId = 0;
        HANDLE hThread = CreateThread(NULL, 0, DummyThread, NULL, 0, &threadId);

        if (!hThread) {
            PrintLastError("CreateThread");
            continue;
        }

        if (showDetails) {
            std::cout << "[Thread #" << i << "] TID: " << threadId << " | Состояние: Running\n";
        }

        WaitForSingleObject(hThread, INFINITE);

        DWORD exitCode = 0;
        GetExitCodeThread(hThread, &exitCode);

        if (showDetails) {
            std::cout << "[Thread #" << i << "] TID: " << threadId << " | Состояние: Finished | Код: " << exitCode << "\n";
        }

        CloseHandle(hThread);
    }

    double endTime = GetTimeInMicroseconds();
    return { count, (endTime - startTime) / 1000.0, (endTime - startTime) / count };
}

// Бенчмарк Процессов
BenchmarkResult BenchmarkProcesses(int count, bool showDetails) {
    if (showDetails) {
        std::cout << "  Тестирование процессов (CreateProcess), N = " << count << "\n";
    }

    double startTime = GetTimeInMicroseconds();

    for (int i = 1; i <= count; ++i) {
        STARTUPINFOW si = { sizeof(si) };
        PROCESS_INFORMATION pi = { 0 };
        wchar_t cmdLine[] = L"ChildWorker.exe";

        BOOL success = CreateProcessW(NULL, cmdLine, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);

        if (!success) {
            PrintLastError("CreateProcessW");
            continue;
        }

        if (showDetails) {
            std::cout << "[Process #" << i << "] PID: " << pi.dwProcessId << " | Состояние: Running\n";
        }

        WaitForSingleObject(pi.hProcess, INFINITE);

        DWORD exitCode = 0;
        GetExitCodeProcess(pi.hProcess, &exitCode);

        if (showDetails) {
            std::cout << "[Process #" << i << "] PID: " << pi.dwProcessId << " | Состояние: Finished | Код: " << exitCode << "\n";
        }

        CloseHandle(pi.hThread);
        CloseHandle(pi.hProcess);
    }

    double endTime = GetTimeInMicroseconds();
    return { count, (endTime - startTime) / 1000.0, (endTime - startTime) / count };
}

int main() {
    setlocale(LC_ALL, "Russian");

    // ИЗМЕНЕНИЕ: Заданы 11 точек от 1 до 100 с шагом 10
    const std::vector<int> objectCounts = { 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 };
    const int RUNS_COUNT = 3;

    struct SummaryRow {
        std::string type;
        int count;
        double medianTotalMs;
        double medianAvgPerObjUs;
    };

    std::vector<SummaryRow> summaryTable;

    // Замеры для Потоков
    for (int count : objectCounts) {
        std::vector<double> totals, avgs;
        for (int run = 1; run <= RUNS_COUNT; ++run) {
            bool showDetails = (run == 1 && count <= 10);
            BenchmarkResult res = BenchmarkThreads(count, showDetails);
            totals.push_back(res.totalTimeMs);
            avgs.push_back(res.avgTimePerObjectUs);
        }
        summaryTable.push_back({ "Thread", count, CalculateMedian(totals), CalculateMedian(avgs) });
    }

    // Замеры для Процессов
    for (int count : objectCounts) {
        std::vector<double> totals, avgs;
        for (int run = 1; run <= RUNS_COUNT; ++run) {
            bool showDetails = (run == 1 && count <= 10);
            BenchmarkResult res = BenchmarkProcesses(count, showDetails);
            totals.push_back(res.totalTimeMs);
            avgs.push_back(res.avgTimePerObjectUs);
        }
        summaryTable.push_back({ "Process", count, CalculateMedian(totals), CalculateMedian(avgs) });
    }

    // Итоговый вывод в консоль
    std::cout << "======================================================================\n";
    std::cout << "                      ИТОГОВЫЕ РЕЗУЛЬТАТЫ\n";
    std::cout << std::left << std::setw(12) << "Тип объекта"
        << std::setw(12) << "Кол-во"
        << std::setw(22) << "Общее время (мс)"
        << std::setw(24) << "Среднее на 1 объект (мкс)" << "\n";

    for (const auto& row : summaryTable) {
        std::cout << std::left << std::setw(12) << row.type
            << std::setw(12) << row.count
            << std::setw(22) << std::fixed << std::setprecision(3) << row.medianTotalMs
            << std::setw(24) << std::fixed << std::setprecision(2) << row.medianAvgPerObjUs << "\n";
    }

    // Экспорт результатов в файл CSV для построения графиков
    std::ofstream csvFile("results.csv");
    if (csvFile.is_open()) {
        csvFile << "Type;Count;TotalTimeMs;AvgTimePerObjUs\n";
        for (const auto& row : summaryTable) {
            csvFile << row.type << ";" << row.count << ";"
                << row.medianTotalMs << ";" << row.medianAvgPerObjUs << "\n";
        }
        csvFile.close();
        std::cout << "\n[ИНФО] Результаты успешно сохранены в файл results.csv\n";
    }

    system("pause");
    return 0;
}
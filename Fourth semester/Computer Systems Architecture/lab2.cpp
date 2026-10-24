#include <chrono>
#include <cmath>
#include <condition_variable>
#include <fstream>
#include <string>
#include <vector>
#include <iostream>
#include <mutex>
#include <sched.h>
#include <thread>
#include <unistd.h>
#include <iomanip>

double readDouble(const std::string &msg) {
    std::cout << msg << '\n';
    double input = 0;
    std::cin >> input;
    return input;
}

void pinToCore(int core) {
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(core, &set);
    sched_setaffinity(0, sizeof(set), &set);
}

double CalculateFunction(double x) {
    return std::exp(std::cos(x)) * std::cos(std::sin(x));
}

double computeSeriesASM(double x, int max_iter, double eps, bool use_eps, int &out_iters) {
    double series = 1.0;
    double func = CalculateFunction(x);

    double term = 1.0;
    double fact = 1.0;
    double cos_val = 1.0;
    int k = 0;

    out_iters = 0;

    do {
        if (k > 0) {
            fact = fact * (double)k;

            double kx = k * x;

            asm volatile (
                "movsd %[kx], %%xmm0\n"
                "call cos\n"
                "movsd %%xmm0, %[cos_val]\n"
                : [cos_val] "=m" (cos_val)
                : [kx] "m" (kx)
                : "xmm0", "rax", "rcx", "rdx", "rsi", "rdi", "memory"
            );

            asm volatile (
                "movsd %[cos_val], %%xmm0\n"
                "divsd %[fact], %%xmm0\n"
                "movsd %%xmm0, %[term]\n"
                : [term] "=m" (term)
                : [cos_val] "m" (cos_val), [fact] "m" (fact)
                : "xmm0"
            );

            series = series + term;
        }

        out_iters = k;
        k++;

        if (use_eps) {
            double diff = series - func;
            if (diff < 0) diff = -diff;
            if (diff < eps) break;
        }

    } while (k <= max_iter);

    out_iters = k - 1;
    return series;
}

int runConvergenceMode() {
    double a = readDouble("Input left coordinate of segment (a): ");
    double b = readDouble("Input right coordinate of segment (b): ");
    if (a > b) {
        std::cout << "Error: a > b\n";
        return 1;
    }

    double eps = readDouble("Epsilon (accuracy): ");
    if (eps <= 0) {
        std::cout << "Error: epsilon must be > 0\n";
        return 1;
    }

    double h = readDouble("Step (h): ");
    if (h <= 0 || h > b - a) {
        std::cout << "Error: invalid step\n";
        return 1;
    }

    std::cout << std::setw(12) << "x"
              << std::setw(18) << "Y(x)"
              << std::setw(18) << "S(x)"
              << std::setw(18) << "|Y-S|"
              << std::setw(12) << "n" << "\n";
    std::cout << std::string(78, '-') << "\n";

    std::ofstream fileOut("convergence.csv");
    if (!fileOut.is_open()) {
        std::cout << "Cannot open convergence.csv\n";
        return 1;
    }
    fileOut << "x,y_x,s_x,error,iterations,time_ms\n";

    for (double x = a; x <= b + 1e-10; x += h) {
        int iterations = 0;

        auto start = std::chrono::high_resolution_clock::now();
        double s_x = computeSeriesASM(x, 1000000, eps, true, iterations);
        auto end = std::chrono::high_resolution_clock::now();

        double y_x = CalculateFunction(x);
        double error = std::abs(y_x - s_x);
        double duration = std::chrono::duration<double, std::milli>(end - start).count();

        std::cout << std::setw(12) << x
                  << std::setw(18) << y_x
                  << std::setw(18) << s_x
                  << std::setw(18) << error
                  << std::setw(12) << iterations << "\n";

        fileOut << x << "," << y_x << "," << s_x << "," << error << "," << iterations << "," << duration << "\n";
    }

    fileOut.close();
    return 0;
}

void runSingleCoreBenchmark(std::string fileName, double x) {
    std::ofstream fileOut(fileName);
    if (!fileOut.is_open()) {
        std::cout << "Cannot open " << fileName << "\n";
        return;
    }
    fileOut << "iterations,time_ns\n";

    pinToCore(0);

    for (int iterations = 1000; iterations <= 50000; iterations += 100) {
        int dummy_iters = 0;

        auto start = std::chrono::high_resolution_clock::now();
        computeSeriesASM(x, iterations, 0.0, false, dummy_iters);
        auto end = std::chrono::high_resolution_clock::now();

        double duration = std::chrono::duration<double, std::nano>(end - start).count();
        fileOut << iterations << "," << duration << "\n";
    }
}

void worker(int core_id, double x, int iter_start, int iter_end, int iter_step,
    std::ofstream &fileOut, std::mutex &file_mtx, std::mutex &start_mtx,
    std::condition_variable &start_cv, bool &start_flag) {

    pinToCore(core_id);

    {
        std::unique_lock<std::mutex> lk(start_mtx);
        start_cv.wait(lk, [&]() { return start_flag; });
    }

    for (int iterations = iter_start; iterations <= iter_end; iterations += iter_step) {
        int dummy = 0;

        auto start = std::chrono::high_resolution_clock::now();
        computeSeriesASM(x, iterations, 0.0, false, dummy);
        auto end = std::chrono::high_resolution_clock::now();

        double time = std::chrono::duration<double, std::nano>(end - start).count();
        std::lock_guard<std::mutex> lock(file_mtx);
        fileOut << core_id << "," << iterations << "," << time << "\n";
    }
}

void runMultiCoreBenchmark(std::string fileName, double x) {
    unsigned int cores = std::thread::hardware_concurrency();

    std::ofstream fileOut(fileName);
    if (!fileOut.is_open()) {
        std::cout << "Cannot open file\n";
        return;
    }
    fileOut << "core,iterations,time_ns\n";

    std::vector<std::thread> threads;
    std::mutex file_mtx;
    std::mutex start_mtx;
    std::condition_variable start_cv;
    bool start_flag = false;

    const int iter_start = 1000;
    const int iter_end = 50000;
    const int iter_step = 100;

    for (int i = 0; i < cores; i++) {
        threads.emplace_back(worker, i, x, iter_start, iter_end, iter_step,
            std::ref(fileOut), std::ref(file_mtx), std::ref(start_mtx),
            std::ref(start_cv), std::ref(start_flag));
    }

    {
        std::lock_guard<std::mutex> lk(start_mtx);
        start_flag = true;
    }
    start_cv.notify_all();

    for (auto &t : threads) {
        t.join();
    }
}

int main() {
    std::ios::sync_with_stdio(false);

    int mode;
    std::cout << "Select mode:\n";
    std::cout << "1 - Convergence mode\n";
    std::cout << "2 - Single-core benchmark\n";
    std::cout << "3 - Multi-core benchmark\n";
    std::cin >> mode;

    if (mode == 1) {
        return runConvergenceMode();
    } else if (mode == 2) {
        double x = readDouble("Enter x value: ");
        std::string fileName;
        std::cout << "Enter filename: ";
        std::cin >> fileName;
        runSingleCoreBenchmark(fileName, x);
    } else if (mode == 3) {
        double x = readDouble("Enter x value: ");
        std::string fileName;
        std::cout << "Enter filename: ";
        std::cin >> fileName;
        runMultiCoreBenchmark(fileName, x);
    } else {
        std::cout << "Invalid mode\n";
    }

    return 0;
}
#include <chrono>
#include <cmath>
#include <fstream>
#include <string>
#include <vector>
#include <iostream>
#include <iomanip>
#define CL_TARGET_OPENCL_VERSION 300
#include <CL/cl.h>

float readFloat(const std::string &msg) {
    std::cout << msg << '\n';
    float input = 0;
    std::cin >> input;
    return input;
}

float CalculateFunction(float x) {
    return std::exp(std::cos(x)) * std::cos(std::sin(x));
}

float computeSeriesCPU(float x, int max_iter, float eps, bool use_eps, int &out_iters) {
    float series = 1.0f;
    float fact = 1.0f;
    int k = 0;
    out_iters = 0;

    for (k = 1; k <= max_iter; k++) {
        fact = fact * (float)k;
        float cos_val = std::cos(k * x);
        float term = cos_val / fact;
        series += term;
        out_iters = k;

        if (use_eps) {
            float true_val = CalculateFunction(x);
            if (std::abs(series - true_val) < eps) break;
        }
    }
    return series;
}

const char* kernelSource =
"__kernel void compute_series(\n"
"    __global const float* x_vals,\n"
"    __global const int* max_iters,\n"
"    __global float* results,\n"
"    __global int* out_iters,\n"
"    float eps,\n"
"    int use_eps,\n"
"    int num_points)\n"
"{\n"
"    int gid = get_global_id(0);\n"
"    if (gid >= num_points) return;\n"
"    \n"
"    float x = x_vals[gid];\n"
"    int max_iter = max_iters[0];\n"
"    \n"
"    float series = 1.0f;\n"
"    float fact = 1.0f;\n"
"    int k = 0;\n"
"    int iter_count = 0;\n"
"    \n"
"    for (k = 1; k <= max_iter; k++) {\n"
"        fact = fact * (float)k;\n"
"        float kx = k * x;\n"
"        float cos_val = cos(kx);\n"
"        float term = cos_val / fact;\n"
"        series += term;\n"
"        iter_count = k;\n"
"        \n"
"        if (use_eps) {\n"
"            float true_val = exp(cos(x)) * cos(sin(x));\n"
"            float diff = series - true_val;\n"
"            if (diff < 0.0f) diff = -diff;\n"
"            if (diff < eps) break;\n"
"        }\n"
"    }\n"
"    \n"
"    results[gid] = series;\n"
"    out_iters[gid] = iter_count;\n"
"}\n";

void checkError(cl_int err, const char* msg) {
    if (err != CL_SUCCESS) {
        std::cout << "OpenCL error: " << msg << " (code: " << err << ")\n";
        exit(1);
    }
}

void runComparisonMode() {
    float a = readFloat("Input left coordinate of segment (a): ");
    float b = readFloat("Input right coordinate of segment (b): ");
    if (a > b) {
        std::cout << "Error: a > b\n";
        return;
    }

    float eps = readFloat("Epsilon (accuracy): ");
    if (eps <= 0) {
        std::cout << "Error: epsilon must be > 0\n";
        return;
    }

    float h = readFloat("Step (h): ");
    if (h <= 0 || h > b - a) {
        std::cout << "Error: invalid step\n";
        return;
    }

    std::vector<float> x_values;
    for (float x = a; x <= b + 1e-6; x += h) {
        x_values.push_back(x);
    }
    int num_points = x_values.size();

    std::cout << "\nNumber of points: " << num_points << "\n";
    std::cout << "Step h: " << h << "\n\n";

    // CPU calculation
    auto cpu_start = std::chrono::high_resolution_clock::now();
    std::vector<float> cpu_results(num_points);
    std::vector<int> cpu_iters(num_points);

    for (int i = 0; i < num_points; i++) {
        cpu_results[i] = computeSeriesCPU(x_values[i], 1000000, eps, true, cpu_iters[i]);
    }

    auto cpu_end = std::chrono::high_resolution_clock::now();
    float cpu_time = std::chrono::duration<float, std::milli>(cpu_end - cpu_start).count();

    // GPU calculation
    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_program program;
    cl_kernel kernel;
    cl_int err;

    err = clGetPlatformIDs(1, &platform, NULL);
    checkError(err, "clGetPlatformIDs");

    err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);
    if (err != CL_SUCCESS) {
        err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_CPU, 1, &device, NULL);
        checkError(err, "clGetDeviceIDs");
    }

    char device_name[128];
    clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(device_name), device_name, NULL);
    std::cout << "Using device: " << device_name << "\n";

    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    checkError(err, "clCreateContext");

    const cl_queue_properties props[] = {0};
    queue = clCreateCommandQueueWithProperties(context, device, props, &err);
    checkError(err, "clCreateCommandQueueWithProperties");

    cl_mem buf_x = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(float) * num_points, NULL, &err);
    checkError(err, "clCreateBuffer buf_x");

    int max_iter = 1000000;
    cl_mem buf_max_iter = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(int), NULL, &err);
    checkError(err, "clCreateBuffer buf_max_iter");

    cl_mem buf_results = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(float) * num_points, NULL, &err);
    checkError(err, "clCreateBuffer buf_results");

    cl_mem buf_iters = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(int) * num_points, NULL, &err);
    checkError(err, "clCreateBuffer buf_iters");

    err = clEnqueueWriteBuffer(queue, buf_x, CL_TRUE, 0, sizeof(float) * num_points, x_values.data(), 0, NULL, NULL);
    checkError(err, "clEnqueueWriteBuffer buf_x");

    err = clEnqueueWriteBuffer(queue, buf_max_iter, CL_TRUE, 0, sizeof(int), &max_iter, 0, NULL, NULL);
    checkError(err, "clEnqueueWriteBuffer buf_max_iter");

    program = clCreateProgramWithSource(context, 1, &kernelSource, NULL, &err);
    checkError(err, "clCreateProgramWithSource");

    err = clBuildProgram(program, 1, &device, NULL, NULL, NULL);
    if (err != CL_SUCCESS) {
        char log[10240];
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, sizeof(log), log, NULL);
        std::cout << "Build error: " << log << "\n";
        checkError(err, "clBuildProgram");
    }

    kernel = clCreateKernel(program, "compute_series", &err);
    checkError(err, "clCreateKernel");

    err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &buf_x);
    err |= clSetKernelArg(kernel, 1, sizeof(cl_mem), &buf_max_iter);
    err |= clSetKernelArg(kernel, 2, sizeof(cl_mem), &buf_results);
    err |= clSetKernelArg(kernel, 3, sizeof(cl_mem), &buf_iters);
    err |= clSetKernelArg(kernel, 4, sizeof(float), &eps);
    int use_eps = 1;
    err |= clSetKernelArg(kernel, 5, sizeof(int), &use_eps);
    err |= clSetKernelArg(kernel, 6, sizeof(int), &num_points);
    checkError(err, "clSetKernelArg");

    size_t global_size = num_points;

    auto gpu_start = std::chrono::high_resolution_clock::now();
    err = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &global_size, NULL, 0, NULL, NULL);
    checkError(err, "clEnqueueNDRangeKernel");

    clFinish(queue);
    auto gpu_end = std::chrono::high_resolution_clock::now();
    float gpu_time = std::chrono::duration<float, std::milli>(gpu_end - gpu_start).count();

    std::vector<float> gpu_results(num_points);
    std::vector<int> gpu_iters(num_points);

    err = clEnqueueReadBuffer(queue, buf_results, CL_TRUE, 0, sizeof(float) * num_points, gpu_results.data(), 0, NULL, NULL);
    checkError(err, "clEnqueueReadBuffer results");

    err = clEnqueueReadBuffer(queue, buf_iters, CL_TRUE, 0, sizeof(int) * num_points, gpu_iters.data(), 0, NULL, NULL);
    checkError(err, "clEnqueueReadBuffer iters");

    std::cout << std::setw(12) << "x"
              << std::setw(18) << "Y(x)"
              << std::setw(18) << "S(x)"
              << std::setw(18) << "|Y-S|"
              << std::setw(12) << "n" << "\n";
    std::cout << std::string(78, '-') << "\n";

    for (int i = 0; i < std::min(10, num_points); i++) {
        float y_x = CalculateFunction(x_values[i]);
        float error = std::abs(y_x - gpu_results[i]);
        std::cout << std::setw(12) << x_values[i]
                  << std::setw(18) << y_x
                  << std::setw(18) << gpu_results[i]
                  << std::setw(18) << error
                  << std::setw(12) << gpu_iters[i] << "\n";
    }

    if (num_points > 10) {
        std::cout << "... (showing first 10 of " << num_points << " points)\n";
    }

    std::cout << "\n=== PERFORMANCE COMPARISON ===\n";
    std::cout << "Number of points: " << num_points << "\n";
    std::cout << "CPU time: " << cpu_time << " ms\n";
    std::cout << "GPU time: " << gpu_time << " ms\n";
    std::cout << "Speedup (CPU/GPU): " << cpu_time / gpu_time << "x\n";

    if (cpu_time / gpu_time > 1) {
        std::cout << "GPU is faster by " << cpu_time / gpu_time << "x\n";
    } else {
        std::cout << "CPU is faster by " << gpu_time / cpu_time << "x\n";
    }

    std::ofstream fileOut("comparison.csv");
    fileOut << "x,y_x,s_x,error,iterations\n";
    for (int i = 0; i < num_points; i++) {
        float y_x = CalculateFunction(x_values[i]);
        float error = std::abs(y_x - gpu_results[i]);
        fileOut << x_values[i] << "," << y_x << "," << gpu_results[i] << "," << error << "," << gpu_iters[i] << "\n";
    }
    fileOut.close();

    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
    clReleaseMemObject(buf_x);
    clReleaseMemObject(buf_max_iter);
    clReleaseMemObject(buf_results);
    clReleaseMemObject(buf_iters);
}

int main() {
    std::ios::sync_with_stdio(false);
    runComparisonMode();
    return 0;
}
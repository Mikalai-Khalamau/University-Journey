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
"        \n"
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

int runGPUMode() {
    float a = readFloat("Input left coordinate of segment (a): ");
    float b = readFloat("Input right coordinate of segment (b): ");
    if (a > b) {
        std::cout << "Error: a > b\n";
        return 1;
    }

    float eps = readFloat("Epsilon (accuracy): ");
    if (eps <= 0) {
        std::cout << "Error: epsilon must be > 0\n";
        return 1;
    }

    float h = readFloat("Step (h): ");
    if (h <= 0 || h > b - a) {
        std::cout << "Error: invalid step\n";
        return 1;
    }

    std::vector<float> x_values;
    for (float x = a; x <= b + 1e-6; x += h) {
        x_values.push_back(x);
    }
    int num_points = x_values.size();

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

    auto start = std::chrono::high_resolution_clock::now();
    err = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &global_size, NULL, 0, NULL, NULL);
    checkError(err, "clEnqueueNDRangeKernel");

    clFinish(queue);
    auto end = std::chrono::high_resolution_clock::now();

    std::vector<float> results(num_points);
    std::vector<int> iterations(num_points);

    err = clEnqueueReadBuffer(queue, buf_results, CL_TRUE, 0, sizeof(float) * num_points, results.data(), 0, NULL, NULL);
    checkError(err, "clEnqueueReadBuffer results");

    err = clEnqueueReadBuffer(queue, buf_iters, CL_TRUE, 0, sizeof(int) * num_points, iterations.data(), 0, NULL, NULL);
    checkError(err, "clEnqueueReadBuffer iters");

    float gpu_time = std::chrono::duration<float, std::milli>(end - start).count();

    std::cout << std::setw(12) << "x"
              << std::setw(18) << "Y(x)"
              << std::setw(18) << "S(x)"
              << std::setw(18) << "|Y-S|"
              << std::setw(12) << "n" << "\n";
    std::cout << std::string(78, '-') << "\n";

    std::ofstream fileOut("gpu_convergence.csv");
    fileOut << "x,y_x,s_x,error,iterations,time_ms\n";

    for (int i = 0; i < num_points; i++) {
        float y_x = CalculateFunction(x_values[i]);
        float error = std::abs(y_x - results[i]);
        std::cout << std::setw(12) << x_values[i]
                  << std::setw(18) << y_x
                  << std::setw(18) << results[i]
                  << std::setw(18) << error
                  << std::setw(12) << iterations[i] << "\n";
        fileOut << x_values[i] << "," << y_x << "," << results[i] << "," << error << "," << iterations[i] << "," << gpu_time / num_points << "\n";
    }

    fileOut.close();
    std::cout << "\nGPU execution time: " << gpu_time << " ms\n";

    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
    clReleaseMemObject(buf_x);
    clReleaseMemObject(buf_max_iter);
    clReleaseMemObject(buf_results);
    clReleaseMemObject(buf_iters);

    return 0;
}

void runGPUBenchmark(std::string fileName, float x) {
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

    context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    checkError(err, "clCreateContext");

    const cl_queue_properties props[] = {0};
    queue = clCreateCommandQueueWithProperties(context, device, props, &err);
    checkError(err, "clCreateCommandQueueWithProperties");

    cl_mem buf_x = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(float), NULL, &err);
    checkError(err, "clCreateBuffer buf_x");

    cl_mem buf_max_iter = clCreateBuffer(context, CL_MEM_READ_ONLY, sizeof(int), NULL, &err);
    checkError(err, "clCreateBuffer buf_max_iter");

    cl_mem buf_results = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(float), NULL, &err);
    checkError(err, "clCreateBuffer buf_results");

    cl_mem buf_iters = clCreateBuffer(context, CL_MEM_WRITE_ONLY, sizeof(int), NULL, &err);
    checkError(err, "clCreateBuffer buf_iters");

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

    std::ofstream fileOut(fileName);
    fileOut << "iterations,time_ns\n";

    for (int iterations = 1000; iterations <= 50000; iterations += 100) {
        err = clEnqueueWriteBuffer(queue, buf_x, CL_TRUE, 0, sizeof(float), &x, 0, NULL, NULL);
        err |= clEnqueueWriteBuffer(queue, buf_max_iter, CL_TRUE, 0, sizeof(int), &iterations, 0, NULL, NULL);
        checkError(err, "clEnqueueWriteBuffer");

        err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &buf_x);
        err |= clSetKernelArg(kernel, 1, sizeof(cl_mem), &buf_max_iter);
        err |= clSetKernelArg(kernel, 2, sizeof(cl_mem), &buf_results);
        err |= clSetKernelArg(kernel, 3, sizeof(cl_mem), &buf_iters);
        float eps = 0.0f;
        err |= clSetKernelArg(kernel, 4, sizeof(float), &eps);
        int use_eps = 0;
        err |= clSetKernelArg(kernel, 5, sizeof(int), &use_eps);
        int num_points = 1;
        err |= clSetKernelArg(kernel, 6, sizeof(int), &num_points);
        checkError(err, "clSetKernelArg");

        auto start = std::chrono::high_resolution_clock::now();

        size_t global_size = 1;
        err = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &global_size, NULL, 0, NULL, NULL);
        checkError(err, "clEnqueueNDRangeKernel");

        clFinish(queue);
        auto end = std::chrono::high_resolution_clock::now();

        float duration = std::chrono::duration<float, std::nano>(end - start).count();
        fileOut << iterations << "," << duration << "\n";
    }

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

    int mode;
    std::cout << "Select mode:\n";
    std::cout << "1 - GPU convergence mode\n";
    std::cout << "2 - GPU benchmark\n";
    std::cin >> mode;

    if (mode == 1) {
        return runGPUMode();
    } else if (mode == 2) {
        float x = readFloat("Enter x value: ");
        std::string fileName;
        std::cout << "Enter filename (e.g., 3_gpu.csv): ";
        std::cin >> fileName;
        runGPUBenchmark(fileName, x);
    } else {
        std::cout << "Invalid mode\n";
    }

    return 0;
}
#include <iostream>
#include <iomanip>
#include <cstdint>
#include <chrono>

using namespace std;

__declspec(align(8)) int8_t A[8] = { 1, -2, 3, -4, 5, -6, 7, -8 };
__declspec(align(8)) int8_t B[8] = { 2, 3, -4, 5, -6, 7, -8, 9 };
__declspec(align(8)) int8_t C[8] = { 1, -1, 2, -2, 3, -3, 4, -4 };
__declspec(align(8)) int16_t D[8] = { 10, -20, 30, -40, 50, -60, 70, -80 };

__declspec(align(8)) int16_t F_mmx[8] = { 0 };

__declspec(align(8)) int16_t F_cpp[8] = { 0 };

__declspec(align(8)) int16_t Aw[8];
__declspec(align(8)) int16_t Bw[8];
__declspec(align(8)) int16_t Cw[8];
__declspec(align(8)) int16_t Sw[8];

const int REPEAT = 1000000;


void CalcMMX()
{
    __asm
    {
        // Распаковка A из 8 байт в 8 слов

        lea eax, A
        movq mm0, qword ptr[eax]

        pxor mm1, mm1
        pcmpgtb mm1, mm0

        movq mm2, mm0
        punpcklbw mm2, mm1

        lea eax, Aw
        movq qword ptr[eax], mm2

        movq mm2, mm0
        punpckhbw mm2, mm1

        lea eax, Aw
        movq qword ptr[eax + 8], mm2

        // Распаковка B из 8 байт в 8 слов

        lea eax, B
        movq mm0, qword ptr[eax]

        pxor mm1, mm1
        pcmpgtb mm1, mm0

        movq mm2, mm0
        punpcklbw mm2, mm1

        lea eax, Bw
        movq qword ptr[eax], mm2

        movq mm2, mm0
        punpckhbw mm2, mm1

        lea eax, Bw
        movq qword ptr[eax + 8], mm2

        // Распаковка C из 8 байт в 8 слов

        lea eax, C
        movq mm0, qword ptr[eax]

        pxor mm1, mm1
        pcmpgtb mm1, mm0

        movq mm2, mm0
        punpcklbw mm2, mm1

        lea eax, Cw
        movq qword ptr[eax], mm2

        movq mm2, mm0
        punpckhbw mm2, mm1

        lea eax, Cw
        movq qword ptr[eax + 8], mm2

        // Обработка элементов 0-3

        lea eax, Bw
        movq mm0, qword ptr[eax]

        lea eax, Cw
        movq mm1, qword ptr[eax]

        paddsw mm0, mm1         // mm0 = B + C

        lea eax, Sw
        movq qword ptr[eax], mm0

        lea eax, Aw
        movq mm1, qword ptr[eax]

        pmullw mm1, mm0         // mm1 = A * (B + C)

        lea eax, D
        movq mm2, qword ptr[eax]

        psubsw mm1, mm2         // mm1 = A * (B + C) - D

        lea eax, F_mmx
        movq qword ptr[eax], mm1   


        // Обработка элементов 47

        lea eax, Bw
        movq mm0, qword ptr[eax + 8]

        lea eax, Cw
        movq mm1, qword ptr[eax + 8]

        paddsw mm0, mm1         // mm0 = B + C

        lea eax, Sw
        movq qword ptr[eax + 8], mm0

        lea eax, Aw
        movq mm1, qword ptr[eax + 8]

        pmullw mm1, mm0         // mm1 = A * (B + C)

        lea eax, D
        movq mm2, qword ptr[eax + 8]

        psubsw mm1, mm2         // mm1 = A * (B + C) - D

        lea eax, F_mmx
        movq qword ptr[eax + 8], mm1

        emms
    }
}


void CalcCPP()
{
    for (int i = 0; i < 8; i++)
    {
        int b_plus_c = (int)B[i] + (int)C[i];
        int a_mul = (int)A[i] * b_plus_c;
        int result = a_mul - (int)D[i];

        F_cpp[i] = (int16_t)result;
    }
}


int main()
{
    setlocale(LC_ALL, "Russian");

    auto t1 = chrono::high_resolution_clock::now();

    for (int i = 0; i < REPEAT; i++)
    {
        CalcMMX();
    }

    auto t2 = chrono::high_resolution_clock::now();
    auto t3 = chrono::high_resolution_clock::now();

    for (int i = 0; i < REPEAT; i++)
    {
        CalcCPP();
    }

    auto t4 = chrono::high_resolution_clock::now();

    long long mmxMicros = chrono::duration_cast<chrono::microseconds>(t2 - t1).count();
    long long cppMicros = chrono::duration_cast<chrono::microseconds>(t4 - t3).count();

    cout << "mmx time: " << mmxMicros << " mks\n";
    cout << "c++ time: " << cppMicros << " mks\n\n";

    cout << " i | F_mmx | F_cpp\n";
    cout << "---+-------+-------\n";

    for (int i = 0; i < 8; i++)
    {
        cout << setw(2) << i + 1 << " |"
            << setw(6) << (int)F_mmx[i] << " |"
            << setw(6) << (int)F_cpp[i] << "\n";
    }

    return 0;
}
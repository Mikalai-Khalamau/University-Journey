#pragma once

#include <string>

namespace FileGenerator {
    bool CreateTestFile(const std::wstring& filePath, size_t sizeInMB);
}
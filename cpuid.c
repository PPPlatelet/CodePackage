#include <stdio.h>
#include <intrin.h>

void get_processor_id(char* buffer) {
    int cpuInfo[4];
    __cpuid(cpuInfo, 1);

    unsigned int eax = cpuInfo[0]; // CPU Signature
    unsigned int edx = cpuInfo[3]; // Feature flags

    // ProcessorId = EDX:EAX
    sprintf_s(buffer, 17, "%08X%08X", edx, eax); // 16字符 + 1终止符
}

int main() {
    char processor_id[17] = { 0 }; // 16 chars + null terminator
    get_processor_id(processor_id);
    printf("Processor ID: %s\n", processor_id);
    return 0;
}

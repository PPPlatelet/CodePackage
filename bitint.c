#include <stdio.h>
#include <string.h>
#define MAX_DIGITS 100100 // 定义最大位数

// 实现大整数加法
void addBigInt(const char *num1, const char *num2, char *result) {
    int len1 = strlen(num1);
    int len2 = strlen(num2);
    int carry = 0; // 进位
    int i = len1 - 1, j = len2 - 1, k = 0;

    char temp[MAX_DIGITS + 1]; // 临时存储反向结果

    while (i >= 0 || j >= 0 || carry) {
        int digit1 = (i >= 0) ? num1[i--] - '0' : 0;
        int digit2 = (j >= 0) ? num2[j--] - '0' : 0;
        int sum = digit1 + digit2 + carry;
        temp[k++] = (sum % 10) + '0'; // 存储当前位的结果
        carry = sum / 10;            // 更新进位
    }

    temp[k] = '\0';

    // 将结果反转并存入结果字符串
    int len = k;
    for (int x = 0; x < len; x++) {
        result[x] = temp[len - 1 - x];
    }
    result[len] = '\0';
}

int main() {   

    return 0;
}

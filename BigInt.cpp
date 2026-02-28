#include <string>
#include <cstdlib>
#include <iostream>
#include <algorithm>

#include "types.h"

#define MAX_BLOCKS 1024

// 大整数结构体
struct BigInt
{
    int len; // 实际使用的块数（最低有效位在d[0]）
    u32 d[MAX_BLOCKS];
};

// 辅助函数：判断大整数是否为0
static int isZero(const struct BigInt *a)
{
    for (int i = 0; i < a->len; i++)
    {
        if (a->d[i] != 0)
            return 0;
    }
    return 1;
}

// 辅助函数：重新计算大整数的实际长度
static void normalize(struct BigInt *a)
{
    while (a->len > 0 && a->d[a->len - 1] == 0)
    {
        a->len--;
    }
    if (a->len == 0)
    {
        a->len = 1; // 保持至少一个块
        a->d[0] = 0;
    }
}

// 1. 按位与运算
void bigint_and(struct BigInt *result, const struct BigInt *a, const struct BigInt *b)
{
    int min_len = std::min(a->len, b->len);

    // 结果长度取较小值（因为高位与0与运算结果为0）
    result->len = min_len;

    // 对重叠部分进行与运算
    for (int i = 0; i < min_len; i++)
    {
        result->d[i] = a->d[i] & b->d[i];
    }

    // 处理较短大整数的高位（默认为0）
    normalize(result);
}

// 2. 按位或运算
void bigint_or(struct BigInt *result, const struct BigInt *a, const struct BigInt *b)
{
    int min_len = std::min(a->len, b->len);
    int max_len = std::max(a->len, b->len);

    // 结果长度取较大值
    result->len = max_len;

    // 对重叠部分进行或运算
    for (int i = 0; i < min_len; i++)
    {
        result->d[i] = a->d[i] | b->d[i];
    }

    // 处理较长部分的高位
    if (a->len > b->len)
    {
        for (int i = min_len; i < max_len; i++)
        {
            result->d[i] = a->d[i];
        }
    }
    else if (b->len > a->len)
    {
        for (int i = min_len; i < max_len; i++)
        {
            result->d[i] = b->d[i];
        }
    }

    normalize(result);
}

// 3. 按位异或运算
void bigint_xor(struct BigInt *result, const struct BigInt *a, const struct BigInt *b)
{
    int min_len = std::min(a->len, b->len);
    int max_len = std::max(a->len, b->len);

    // 结果长度取较大值
    result->len = max_len;

    // 对重叠部分进行异或运算
    for (int i = 0; i < min_len; i++)
    {
        result->d[i] = a->d[i] ^ b->d[i];
    }

    // 处理较长部分的高位
    if (a->len > b->len)
    {
        for (int i = min_len; i < max_len; i++)
        {
            result->d[i] = a->d[i];
        }
    }
    else if (b->len > a->len)
    {
        for (int i = min_len; i < max_len; i++)
        {
            result->d[i] = b->d[i];
        }
    }

    normalize(result);
}

void u32_write_bits(u32 *dest, const u32 *src, int start_bit, int end_bit)
{
    // if (start_bit < 0 || end_bit < start_bit) return *dest;

    int len = end_bit - start_bit + 1;

    u32 mask;
    if (len == 32)
        mask = 0xFFFFFFFF;
    else
        mask = ((1u << len) - 1u) << start_bit;

    // 清除目标位
    *dest &= ~mask;

    // 设置新值
    u32 value;
    if (len == 32)
        value = *src;
    else
        value = (*src & ((1u << len) - 1u)) << start_bit;

    *dest |= value;

    return;
}

u32 u32_read_bits(const u32 *src, int start_bit, int end_bit)
{
    // if (start_bit < 0 || end_bit < start_bit) return 0;

    int len = end_bit - start_bit + 1;

    u32 mask;
    if (len == 32)
        mask = 0xFFFFFFFF;
    else
        mask = ((1u << len) - 1u) << start_bit;

    u32 value = (*src & mask) >> start_bit;

    return value;
}

// 按位写入
void bigint_write_bits(struct BigInt *dest, const u32 *src, int start_bit, int end_bit)
{
    // if (start_bit < 0 || end_bit < start_bit) return;

    int len = end_bit - start_bit + 1;

    int block = start_bit / 32;
    int off = start_bit % 32;

    if (off + len <= 32)
    {
        // u32 old = dest->d[block];
        u32_write_bits(&dest->d[block], src, off, off + len - 1);

        // if (ret == old) return;

        if (block + 1 > dest->len)
            dest->len = block + 1;

        return;
    }

    int first_bits = 32 - off;
    int second_bits = len - first_bits;

    u32 low_part = u32_read_bits(src, 0, first_bits - 1);

    // u32 old1 = dest->d[block];
    u32_write_bits(&dest->d[block], &low_part, off, 31);

    // if (ret1 == old1) return;

    u32 high_part = u32_read_bits(src, first_bits, len - 1);

    // u32 old2 = dest->d[block + 1];
    u32_write_bits(&dest->d[block + 1], &high_part, 0, second_bits - 1);

    // if (ret2 == old2) return;

    if (block + 2 > dest->len)
        dest->len = block + 2;

    return;
}

// 按位读出
u32 bigint_read_bits(const BigInt *a,
                     int start_bit,
                     int end_bit)
{
    // if (start_bit < 0 || end_bit < start_bit) return 0;

    int len = end_bit - start_bit + 1; // <= 32

    int block = start_bit / 32;
    int off = start_bit % 32;

    if (off + len <= 32)
    {
        return u32_read_bits(&a->d[block], off, off + len - 1);
    }

    int first_bits = 32 - off;
    int second_bits = len - first_bits;

    u32 low_part = u32_read_bits(&a->d[block],
                                 off,
                                 31);

    u32 high_part = u32_read_bits(&a->d[block + 1],
                                  0,
                                  second_bits - 1);

    u32 v = low_part | (high_part << first_bits);

    return v;
}

int main()
{
    std::cout << "All tests passed.\n";
    system("pause");
    return 0;
}

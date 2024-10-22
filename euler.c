#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SAFE_FREE(ptr) \
    do { if (ptr != NULL) free(ptr), ptr = NULL; } while(0)

void printPyramid(int N) {
    int maxStars = 1 + 4 * (N - 1);  // 最宽一行的星号数量

    for (int i = 0; i < N - 1; i++)
    {
        for (int j = 0; j < 2 * (N - i - 1); j++)
        {
            printf(" ");
        }
        for (int j = 0; j < 1 + (4 * i); j++)
        {
            printf("*");
        }
        printf("\n");
    }
    for (int i = 0; i < maxStars; i++)
    {
        printf("*");
    }
    printf("\n");
    for (int i = 0; i < N - 1; i++)
    {
        for (int j = 0; j < 2 * (i + 1); j++)
        {
            printf(" ");
        }
        for (int j = 0; j < 1 + (4 * (N - i - 2)); j++)
        {
            printf("*");
        }
        printf("\n");
    }
}

int main() {
    int number, cnt = 0;
    scanf("%d", &number);

    if (number < 1)
    {
        return 1;
    }

    int* isprime = (int*)malloc((number + 1) * sizeof(int));
    int* primes = (int*)calloc(number + 1, sizeof(int));
    memset(isprime, 1, (number + 1) * sizeof(int));
    isprime[0] = 0;
    isprime[1] = 0;

    for (int i = 2; i <= number; i++)
    {
        if (isprime[i])
        {
            primes[++cnt] = i;
        }

        for (int j = 1; j <= cnt && i * primes[j] <= number; j++)
        {
            isprime[i * primes[j]] = 0;
            if (i % primes[j] == 0) { break; }
        }
    }

    printf("%d\n", cnt);

    SAFE_FREE(isprime);
    SAFE_FREE(primes);

    system("pause");

    return 0;
}

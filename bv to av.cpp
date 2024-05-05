#include <iostream>
#include <string>
#include <unordered_map>
#include <cmath>

static const int s[] = {11, 10, 3, 8, 4, 6};
static const int xor_val = 177451812;
static const unsigned long long add_val = 8728348608;
static const std::string table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF";
std::unordered_map<char, int> tr = {};

static void init_tr() noexcept {
    for (int i = 0; i < 58; ++i) {
        tr[table[i]] = i;
    }
}

static long long dec(const std::string& x) noexcept {
    unsigned long long r = 0;
    for (int i = 0; i < 6; ++i) {
        r += tr[x[s[i]]] * (unsigned long long)pow(58, i);
    }
    return (r - add_val) ^ xor_val;
}

static std::string enc(const unsigned long long& x) noexcept {
    unsigned long long num = (x ^ xor_val) + add_val;
    char r[] = "BV1  4 1 7  ";
    for (int i = 0; i < 6; ++i) {
        r[s[i]] = table[num / (unsigned long long)pow(58, i) % 58];
    }
    return std::string(r);
}

//test code
int main() {
    init_tr();
    std::cout << dec("BV17x411w7KC") << std::endl;
    std::cout << dec("BV1Q541167Qg") << std::endl;
    std::cout << dec("BV1mK4y1C7Bz") << std::endl;
    std::cout << enc(170001) << std::endl;
    std::cout << enc(455017605) << std::endl;
    std::cout << enc(882584971) << std::endl;
    return 0;
}
#include <iostream>
#include <complex>

int main() {
    // 创建两个复数
    std::complex<double> c1(5.0, 3.0); // 5 + 3i
    std::complex<double> c2(2.0, -4.0); // 2 - 4i

    // 输出复数
    std::cout << "c1: " << c1 << std::endl;
    std::cout << "c2: " << c2 << std::endl;

    // 复数加法
    std::complex<double> sum = c1 + c2;
    std::cout << "Sum: " << sum << std::endl; // 输出 7 - i

    // 复数减法
    std::complex<double> diff = c1 - c2;
    std::cout << "Difference: " << diff << std::endl; // 输出 3 + 7i

    // 复数乘法
    std::complex<double> product = c1 * c2;
    std::cout << "Product: " << product << std::endl; // 输出 -37 + 2i

    // 复数除法
    std::complex<double> quotient = c1 / c2;
    std::cout << "Quotient: " << quotient << std::endl; // 输出 0.4 - 1.2i

    // 复数的共轭
    std::complex<double> conjugate = std::conj(c1);
    std::cout << "Conjugate of c1: " << conjugate << std::endl; // 输出 5 - 3i

    // 复数的模
    double modulus = std::abs(c1);
    std::cout << "Modulus of c1: " << modulus << std::endl; // 输出 sqrt(34)

    // 复数的辐角
    double argument = std::arg(c1);
    std::cout << "Argument of c1: " << argument << std::endl; // 输出 atan(3/5)

    return 0;
}
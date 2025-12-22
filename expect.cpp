#include <expected>
#include <iostream>

std::expected<int, std::string> divide(int a, int b) {
    if (b == 0) {
        return std::unexpected<std::string>("Division by zero");
    }
    return a / b;
}

int main() {
    auto result = divide(10, 5);
    if (result) {
        std::cout << "Result: " << *result << std::endl;
    } else {
        std::cout << "Error: " << result.error() << std::endl;
    }
    auto result2 = divide(10, 0);
    if (result2) {
        std::cout << "Result: " << *result2 << std::endl;
    } else {
        std::cout << "Error: " << result2.error() << std::endl;
    }
    return 0;
}
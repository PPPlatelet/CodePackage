#include <iostream>
#include <map>
#include <functional>

void foo()
{
    std::cout << "foo() called" << std::endl;
}

void bar()
{
    std::cout << "bar() called" << std::endl;
}

int main()
{
    std::map<std::string, std::function<void()>>funcMap;
    funcMap["foo"] = foo;
    funcMap["bar"] = bar;

    std::string choice;
    std::cout << "Enter 'foo' or 'bar': ";
    std::cin >> choice;
    if (funcMap.find(choice) != funcMap.end())
    {
        funcMap[choice]();
    }
    else
    {
        std::cout << "Invalid choice! " << std::endl;
    }

    system("pause");

    return 0;
}
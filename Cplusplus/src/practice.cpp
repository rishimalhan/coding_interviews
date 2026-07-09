#include <iostream>

int frequency(long int number, int k)
{
    int counter = 0;
    while (number >= 1 || number <= -1)
    {
        if (number % 10 == k)
            counter += 1;
        number /= 10;
    }
    return counter;
}

bool palindrome_detector(int number)
{
    int copy_number = number;
    int reverse_number = 0;
    while (copy_number != 0)
    {
        reverse_number = (reverse_number * 10) + (copy_number % 10);
        copy_number /= 10;
    }
    return (number == reverse_number);
}

template <typename T>
T multiply(T x, T y)
{
    return x * y;
}

int main(int argv, char **argc)
{
    std::cout << frequency(1001, 1) << "\n";
    std::cout << frequency(1332456321345, 3) << "\n";
    std::cout << multiply<int>(5, 3) << "\n";
    std::cout << multiply<float>(3.0, 3000.983758578) << "\n";
    std::cout << sizeof(45678) << "\n";
    std::cout << palindrome_detector(12201) << "\n";
    return 0;
}

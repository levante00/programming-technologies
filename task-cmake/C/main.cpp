#include "main.h"
#include <iostream>

int main() {

  Object input;
  Pair item;

  std::cin >> input.number;
  std::cin >> input.str;

  item.a = input.number;
  item.b = (input.str).length();

  std::cout << "input pair 1: " << item.a << std::endl;
  std::cout << "input pair 2: " << item.b << std::endl;

  return 0;
}

#include <iostream>

using namespace std;

int a = 5;
int b = 10;
auto sum(auto a, auto b) { return a + b; }
auto subtract(auto a, auto b) { return a - b; }
auto product(auto a, auto b) { return a * b; }
auto modulo(auto a, auto b) { return a % b; }

int main() {

  auto x = sum(a, b);
  subtract(a, b);
  product(a, b);
  modulo(a, b);

  return 0;
}
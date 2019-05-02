
#include <iostream>

int main() {
  using F = void(*)(int);
  F fn = (F)5;
  fn(3); // 5 3
}

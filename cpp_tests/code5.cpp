#include <iostream>
#include <vector>

using namespace std;

std::vector<int> mylist = {1, 2, 3};
int a = mylist.front();
std::vector<int> b = std::vector<int>(mylist.begin() + 1, mylist.end());

template <typename T>

void cons(vector<T> &mylist, T elem) {
  mylist.insert(mylist.begin(), elem);
}

int main() {
  cons(mylist, 0);

  return 0;
}
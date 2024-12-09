#include <iostream>
#include <vector>

using namespace std;

std::vector<int> mylist = {1, 2, 3};
int a = mylist.front();
std::vector<int>(mylist.begin() + 1, mylist.end())

([] {
std::vector<int> temp = {0};
  temp.insert(temp.end(), mylist.begin(), mylist.end());
  return temp;
}())

    int main() {

  return 0;
}
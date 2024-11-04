#include <iostream>

auto add(auto x, auto y){
    return (x+y);
}

auto not_q(auto x){
    return !x;
}

int main(){
    int x = 5;
    int y = 6;


    // std::cout << add(x,y);

    std::cout << not_q(true);
}
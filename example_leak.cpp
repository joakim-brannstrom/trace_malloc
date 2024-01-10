#include <iostream>
#include <thread>

int main(int argc, char **argv) {
    for (int i = 0; i < 3; ++i) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        int* x = new int;
        *x = 42;
    }
    return 0;
}

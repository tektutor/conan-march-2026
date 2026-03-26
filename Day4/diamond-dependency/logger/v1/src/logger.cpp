#include "logger.h"
#include <iostream>

void logger::log(std::string msg) {
    std::cout << "[Logger 1.0] " << msg << std::endl;
}

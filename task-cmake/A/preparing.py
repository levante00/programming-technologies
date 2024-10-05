find = "index.h"

f = open(find, "w+")

f.write(
    "#pragma once\n#include <iostream>\n#include <string>\n\nstruct Object{\n\n    std::string  str;\n    int number;\n\n};"
)

f.close()

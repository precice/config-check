from enum import Enum

import color as c

#colors: 0:grey, 1:red 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, 7:white
class Severity(Enum):
    DEBUG = c.dyeing("DEBUG", c.blue)
    WARNING = c.dyeing("WARNING", c.yellow)
    ERROR = c.dyeing("ERROR", c.red)
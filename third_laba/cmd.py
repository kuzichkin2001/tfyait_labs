from enum import Enum


class ECmd(Enum):
    JMP = 1
    JZ = 2
    SET = 3
    ADD = 4
    SUB = 5
    MUL = 6
    DIV = 7
    AND = 8
    OR = 9
    CMPE = 10
    CMPNE = 11
    CMPL = 12
    CMPLE = 13
    CMPG = 14
    CMPGE = 15
    OUTPUT = 16
    INPUT = 17

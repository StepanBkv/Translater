import json
import re
from os import path

with open("settings.txt", "r", encoding="utf-8") as read_file:
    input_file = read_file.readline().strip()
    output_dir = read_file.readline().strip()

with open(output_dir + "I.json", "r") as read_file:
    I = json.load(read_file)

with open(output_dir + "C.json", "r") as read_file:
    C = json.load(read_file)

with open(output_dir + "N.json", "r") as read_file:
    N = json.load(read_file)

name = path.basename(input_file)
name = path.splitext(name)[0]
with open(output_dir + name + "_lex.txt", "r") as read_file:
    INPUT = read_file.read().split()

STACK = []
OUTPUT = []

m = 0


def priority(str):
    if str in ["R5", "R9", "АЭМ", "Ф", "ARR", "W2", "W1", "W5", "W4", "FUNC"]:
        return 0
    if str in ["R6", "R10", "R3", "W6", "W3", "R4"]:
        return 1
    if str in ["O12", "W7", "RETURN"]:
        return 2
    if str == "O16":
        return 3
    if str == "O17":
        return 4
    if str == "O18":
        return 5
    if str in ["O6", "O7", "O8", "O9", "O10", "O11"]:
        return 6
    if str in ["O1", "O2"]:
        return 7
    if str in ["O3", "O4", "O13"]:
        return 8
    if str in ["O5", "O14", "O15"]:
        return 9
    if str in [":", "R7", "R8"]:
        return 10


for i in range(len(INPUT)):
    lexem = INPUT[i]

    if lexem == "R2" or lexem in I.values() or lexem in C.values() or lexem in N.values():
        OUTPUT.append(lexem)
        continue

    if lexem == "R5" and i > 1 and INPUT[i - 1] in I.values():
        STACK.append(1)
        STACK.append("Ф")
        continue

    if lexem == "R3":
        while STACK[len(STACK) - 1] != "АЭМ" and STACK[len(STACK) - 1] != "Ф" and STACK[len(STACK) - 1] != "ARR" and \
                STACK[len(STACK) - 1] != "R5":
            if STACK[len(STACK) - 1] == "W7":
                STACK.pop()
                OUTPUT.append("БП")
            else:
                OUTPUT.append(STACK.pop())
        op = STACK.pop()
        if op == "R5":
            STACK.append(1)
            STACK.append("ARR")
        else:
            STACK[len(STACK) - 1] += 1
            STACK.append(op)
        continue

    if lexem == "R5":
        STACK.append("R5")
        continue

    if lexem == "R9":
        STACK.append(2)
        STACK.append("АЭМ")
        continue

    if lexem == "W2":
        STACK.append("W2")
        continue

    if lexem == "W6":
        while STACK[len(STACK) - 1] != "W2":
            if STACK[len(STACK) - 1] == "W7":
                STACK.pop()
                OUTPUT.append("БП")
            else:
                OUTPUT.append(STACK.pop())
        STACK.pop()
        m += 1
        STACK.append(f"M{m}")
        STACK.append("W2")
        OUTPUT.append(f"M{m}")
        OUTPUT.append("УПЛ")
        continue

    if lexem == "W3":
        STACK.append("W3")
        continue

    if lexem == "W1":
        STACK.append("W1")
        continue

    if lexem == "W5":
        STACK.append("W5")
        continue

    if lexem == "W4":
        STACK.append("W4")
        continue

    if lexem == "W8":
        STACK.append("RETURN")
        continue

    if lexem == "R7":
        if STACK[len(STACK) - 1] == "W1":
            OUTPUT.append(1)
            OUTPUT.append("НП")
        elif STACK[len(STACK) - 1] == "W5":
            OUTPUT.append("WH")
        elif STACK[len(STACK) - 1] == "W4":
            OUTPUT.append("FOR")
        elif STACK[len(STACK) - 1] == "W2":
            m += 1
            OUTPUT.append(f"M{m} УПЛ")
        elif STACK[len(STACK) - 1] == "W3":
            m += 1
            OUTPUT.append(f"M{m}")
            OUTPUT.append("БП")
            OUTPUT.append(f"M{m - 1}")
            OUTPUT.append(":")
        continue

    if lexem == "R8":
        if STACK[-1] == "W1" or STACK[-1] == "FUNC":
            OUTPUT.append("КП")
        elif STACK[-1] == "W5" or STACK[-1] == "W4":
            OUTPUT.append("END")
        elif STACK[-1] == "W3":
            OUTPUT.append(f"M{m}")
            OUTPUT.append(":")
        STACK.pop()
        continue

    if lexem == "R4":
        while len(STACK) > 0 and STACK[-1] != "R5" and STACK[-1] != "W1" and STACK[-1] != "W2" and STACK[-1] != "W3" and \
                STACK[-1] != "W4" and STACK[-1] != "W5" and STACK[-1] != "FUNC":
            if STACK[len(STACK) - 1] == "W7":
                STACK.pop()
                OUTPUT.append("БП")
            else:
                OUTPUT.append(STACK.pop())
        continue

    if lexem == "R6":
        while len(STACK) > 0 and STACK[len(STACK) - 1] != "R5" and STACK[len(STACK) - 1] != "Ф" and STACK[
            len(STACK) - 1] != "ARR":
            if STACK[len(STACK) - 1] == "W7":
                STACK.pop()
                OUTPUT.append("БП")
            else:
                OUTPUT.append(STACK.pop())
        if len(STACK) > 0:
            op = STACK.pop()
            if op == "Ф":
                if INPUT[i - 1] == "R5":
                    OUTPUT.append(STACK.pop())
                else:
                    OUTPUT.append(STACK.pop() + 1)
                OUTPUT.append("Ф")
            if op == "ARR":
                OUTPUT.append(STACK.pop() + 1)
                OUTPUT.append("ARR")

        continue

    if lexem == "R10":
        while STACK[len(STACK) - 1] != "АЭМ":
            if STACK[len(STACK) - 1] == "W7":
                STACK.pop()
                OUTPUT.append("БП")
            else:
                OUTPUT.append(STACK.pop())
        STACK.pop()
        OUTPUT.append(STACK.pop())
        OUTPUT.append("АЭМ")
        continue

    if len(STACK) == 0 or priority(STACK[len(STACK) - 1]) < priority(lexem):
        STACK.append(lexem)
        continue

    while len(STACK) > 0 and priority(STACK[len(STACK) - 1]) >= priority(lexem):
        if STACK[len(STACK) - 1] == "W7":
            STACK.pop()
            OUTPUT.append("БП")
        else:
            OUTPUT.append(STACK.pop())
    STACK.append(lexem)

while len(STACK) > 0:
    if STACK[len(STACK) - 1] == "W7":
        STACK.pop()
        OUTPUT.append("БП")
    else:
        OUTPUT.append(STACK.pop())

with open(output_dir + name + "_pol.txt", "w", encoding="utf-8") as write_file:
    write_file.write(" ".join(map(str, OUTPUT)))
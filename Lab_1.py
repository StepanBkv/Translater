import json
import re

# Служебные слова
with open("W.json", "r") as read_file:
    W = json.load(read_file)
# Операции
with open("O.json", "r") as read_file:
    O = json.load(read_file)
# Разделители
with open("R.json", "r") as read_file:
    R = json.load(read_file)


def IS_SEPARATOR(symbol):
    return symbol in " \{\}(),;\n\t[]"


def IS_OPERATION(symbol):
    return symbol in "+-*/%<>=!"


def IS_DOUBLE_OPERATION(symbols):
    return symbols in O


def IS_COMMENTARY(symbol):
    return symbol == "#"


def IS_SPACE(symbol):
    return symbol == " "


def IS_E(symbol):
    return re.match("[eE]", symbol)


def IS_DIGIT(symbol):
    return re.match("[0-9]", symbol)


def IS_LETTER(symbol):
    return re.match("[a-zA-Z]", symbol)


def IS_UNDERSCORE(symbol):
    return symbol == "_"


def IS_MINUS(symbol):
    return symbol == "-"


def IS_DOT(symbol):
    return symbol == "."


def IS_END(symbol):
    return symbol == "\n"


def IS_SPECIAL(symbol):
    return symbol in "$@&"


def IS_QUOTES(symbol):
    return re.match("'", symbol)


def IS_DOUBLE_QUOTES(symbol):
    return re.match("\"", symbol)


with open("settings.txt", "r") as read_file:
    input_file = read_file.readline().strip()
    output_dir = read_file.readline().strip()

with open(input_file, "r") as read_file:
    INPUT = read_file.read()

OUTPUT = []

I = {}  # индетификаторы
N = {}  # числовые константы
C = {}  # символьные константы

STATE = "START"

accumulator = ""
for i in range(len(INPUT)):
    if STATE == "ERROR":
        break
    sym = INPUT[i]
    # операция
    if STATE == "OPERATION":
        STATE = "START"
        if not sym in O.keys():
            OUTPUT.append(O[accumulator])
            accumulator = ""
        else:
            OUTPUT.append(O[accumulator + sym])
            accumulator = ""
        continue

    # стартовое состояние
    if STATE == "START":
        if IS_SPECIAL(sym):
            STATE = "1"
            continue
        elif IS_UNDERSCORE(sym) or IS_LETTER(sym):
            STATE = "2"
            accumulator += sym
            continue
        elif IS_DIGIT(sym):
            STATE = "3"
            accumulator += sym
            continue
        elif IS_DOT(sym):
            STATE = "4"
            accumulator += sym
            continue
        elif IS_OPERATION(sym):
            STATE = "OPERATION"
            accumulator += sym
            continue
        elif IS_QUOTES(sym):
            STATE = "QUOTES"
            continue
        elif IS_DOUBLE_QUOTES(sym):
            STATE = "DOUBLE_QUOTES"
            continue
        elif IS_SEPARATOR(sym):
            STATE = "SEPARATOR"
        elif IS_COMMENTARY(sym):
            STATE = "COMMENTARY"
            continue
        else:
            STATE = "ERROR"

    # после специального символа
    if STATE == "1":
        if IS_UNDERSCORE(sym) or IS_LETTER(sym):
            STATE = "2"
            accumulator += sym
        else:
            STATE = "ERROR"
        continue

    # после подчеркивания или буквы
    if STATE == "2":
        if IS_UNDERSCORE(sym) or IS_DIGIT(sym) or IS_LETTER(sym):
            accumulator += sym
        elif IS_SEPARATOR(sym) or IS_OPERATION(sym) or IS_COMMENTARY(sym):
            if accumulator in W.keys():
                OUTPUT.append(W[accumulator])
            elif accumulator in I.keys():
                OUTPUT.append(I[accumulator])
            else:
                I[accumulator] = f"I{len(I) + 1}"
                OUTPUT.append(I[accumulator])

            if IS_SEPARATOR(sym):
                STATE = "SEPARATOR"
            if IS_OPERATION(sym):
                STATE = "OPERATION"
            if IS_COMMENTARY(sym):
                STATE = "COMMENTARY"

            accumulator = ""
        else:
            STATE = "ERROR"
            continue

    # после цифры
    if STATE == "3":
        if IS_DIGIT(sym):
            accumulator += sym
        elif IS_DOT(sym):
            STATE = "4"
        elif IS_E(sym):
            STATE = "5"
        elif IS_SEPARATOR(sym) or IS_OPERATION(sym) or IS_COMMENTARY(sym):
            if accumulator in N.keys():
                OUTPUT.append(N[accumulator])
            else:
                N[accumulator] = f"N{len(N) + 1}"
                OUTPUT.append(N[accumulator])

            if IS_SEPARATOR(sym):
                STATE = "SEPARATOR"
            if IS_OPERATION(sym):
                STATE = "OPERATION"
            if IS_COMMENTARY(sym):
                STATE = "COMMENTARY"

            accumulator = ""
        else:
            STATE = "ERROR"
            continue

    # после точки
    if STATE == "4":
        if IS_DIGIT(sym):
            STATE = "5"
            accumulator += sym
        else:
            STATE = "ERROR"
        continue

    # после точки и цифры
    if STATE == "5":
        if IS_DIGIT(sym):
            accumulator += sym
            continue
        elif IS_E(sym):
            STATE = "6"
            accumulator += sym
            continue
        elif IS_SEPARATOR(sym) or IS_OPERATION(sym) or IS_COMMENTARY(sym):
            if accumulator in N.keys():
                OUTPUT.append(N[accumulator])
            else:
                N[accumulator] = f"N{len(N) + 1}"
                OUTPUT.append(N[accumulator])

            if IS_SEPARATOR(sym):
                STATE = "SEPARATOR"
            if IS_OPERATION(sym):
                STATE = "OPERATION"
            if IS_COMMENTARY(sym):
                STATE = "COMMENTARY"

            accumulator = ""
        else:
            STATE = "ERROR"
            continue

    # после е
    if STATE == "6":
        if IS_MINUS(sym):
            STATE = "7"
            accumulator += sym
        elif IS_DIGIT(sym):
            STATE = "8"
            accumulator += sym
        else:
            STATE = "ERROR"
        continue

    # после минуса
    if STATE == "7":
        if IS_DIGIT(sym):
            STATE = "8"
            accumulator += sym
        else:
            STATE = "ERROR"
        continue

    if STATE == "8":
        if IS_DIGIT(sym):
            accumulator += sym
        elif IS_SEPARATOR(sym) or IS_OPERATION(sym) or IS_COMMENTARY(sym):
            if accumulator in N.keys():
                OUTPUT.append(N[accumulator])
            else:
                N[accumulator] = f"N{len(N) + 1}"
                OUTPUT.append(N[accumulator])

            if IS_SEPARATOR(sym):
                STATE = "SEPARATOR"
            if IS_OPERATION(sym):
                STATE = "OPERATION"
            if IS_COMMENTARY(sym):
                STATE = "COMMENTARY"

            accumulator = ""
        else:
            STATE = "ERROR"
            continue

    # разделитель
    if STATE == "SEPARATOR":
        if not IS_SPACE(sym):
            OUTPUT.append(R[sym])
        STATE = "START"
        accumulator = ""
        continue

    # комментарий
    if STATE == "COMMENTARY":
        if IS_END(sym):
            STATE = "START"
        accumulator = ""
        continue

    # строка с одинарными кавычками
    if STATE == "QUOTES":
        if IS_QUOTES(sym):
            if accumulator in C.keys():
                OUTPUT.append(C[accumulator])
            else:
                C[accumulator] = f"C{len(C) + 1}"
                OUTPUT.append(C[accumulator])
            STATE = "START"
            accumulator = ""
        else:
            accumulator += sym
        continue

    # строка с двойными кавычками
    if STATE == "DOUBLE_QUOTES":
        if IS_DOUBLE_QUOTES(sym):
            if accumulator in C.keys():
                OUTPUT.append(C[accumulator])
            else:
                C[accumulator] = f"C{len(C) + 1}"
                OUTPUT.append(C[accumulator])
            STATE = "START"
            accumulator = ""
        else:
            accumulator += sym
        continue

with open(output_dir + "/result.txt", "w") as write_file:
    write_file.write(" ".join(OUTPUT))

with open(output_dir + "/N.json", "w") as write_file:
    json.dump(N, write_file)

with open(output_dir + "/C.json", "w") as write_file:
    json.dump(C, write_file)

with open(output_dir + "/I.json", "w") as write_file:
    json.dump(I, write_file)

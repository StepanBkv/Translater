import json
from os import path

with open("settings.txt", "r", encoding="utf-8") as read_file:
    input_file = read_file.readline().strip()
    output_dir = read_file.readline().strip()

with open(output_dir + "I.json", "r", encoding="utf-8") as read_file:
    I = json.load(read_file)

with open(output_dir + "C.json", "r", encoding="utf-8") as read_file:
    C = json.load(read_file)

with open(output_dir + "N.json", "r", encoding="utf-8") as read_file:
    N = json.load(read_file)

with open("W.json", "r", encoding="utf-8") as read_file:
    W = json.load(read_file)

with open("O.json", "r", encoding="utf-8") as read_file:
    O = json.load(read_file)

with open("R.json", "r", encoding="utf-8") as read_file:
    R = json.load(read_file)

name = path.basename(input_file)
name = path.splitext(name)[0]
with open(output_dir + name + "_pol.txt", "r", encoding="utf-8") as read_file:
    INPUT = read_file.read().split()

STACK = []
OUTPUT = []


class Function:
    def __init__(self, name, type, point):
        self.name = name
        self.type = type
        self.point = point


functions = []
func_stack = []


def wrap(string, m=""):
    return m.ljust(5, " ") + string.strip() + "\n"


for i in range(len(INPUT)):
    lexem = INPUT[i]

    if lexem in O.values():
        for key, value in O.items():
            if value == lexem:
                if lexem == "O14":
                    id = STACK.pop()
                    STACK.append(wrap(f"{id} = {id} + 1"))
                elif lexem == "O15":
                    id = STACK.pop()
                    STACK.append(wrap(f"{id} = {id} - 1"))
                elif lexem == "O6":
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(f"{id1} .LT. {id2}")
                elif lexem == "O7":
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(f"{id1} .GT. {id2}")
                elif lexem == "O8":
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(f"{id1} .EQ. {id2}")
                elif lexem == "O9":
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(f"{id1} .NE. {id2}")
                elif lexem == "O10":
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(f"{id1} .LE. {id2}")
                elif lexem == "O11":
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(f"{id1} .GE. {id2}")
                elif lexem == "O12":
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(wrap(f"{id1} {key} {id2}"))
                else:
                    id2 = STACK.pop()
                    id1 = STACK.pop()
                    STACK.append(f"{id1} {key} {id2}")


    elif lexem in I.values():
        for key, value in I.items():
            if value == lexem:
                STACK.append(key)

    elif lexem in C.values():
        for key, value in C.items():
            if value == lexem:
                STACK.append('"' + key + '"')

    elif lexem in N.values():
        for key, value in N.items():
            if value == lexem:
                STACK.append(key)

    elif lexem == "Ф":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        if (func := list(filter(lambda function: function.name == params[0], functions))) and func[
            0].type == "function":
            STACK.append(wrap(f"{params[0]}({','.join(map(str.strip, params[1:]))})"))
        else:
            STACK.append(wrap(f"call {params[0]}({','.join(map(str.strip, params[1:]))})"))

    elif lexem == "АЭМ":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        STACK.append(f"{params[0]}{''.join(map(lambda x: '[' + str(x) + ']', params[1:]))}")

    elif lexem == "INTEGER":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        STACK.append(wrap(f"integer :: {','.join(params)}"))

    elif lexem == "REAL":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        STACK.append(wrap(f"real :: {','.join(params)}"))

    elif lexem == "CHARACTER":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        STACK.append(wrap(f"character :: {','.join(params)}"))

    elif lexem == "MASS":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        STACK.append(wrap(f"{params[1]}, dimension ({','.join(params[2:])}) :: {params[0]}"))

    elif lexem == "НП":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        func = Function(params[0], "subroutine", len(STACK))
        functions.append(func)
        func_stack.append(func)
        STACK.append(wrap(f"subroutine {func.name}({','.join(params[1:])})"))

    elif lexem == "КО":
        continue

    elif lexem == "RETURN":
        func = functions[-1]
        STACK[func.point] = STACK[func.point].replace("subroutine", "function")
        func.type = "function"
        STACK.append(wrap(f"{func.name} = {STACK.pop()}"))

    elif lexem == "КП":
        func = func_stack.pop()
        STACK.append(wrap(f"end {func.type} {func.name}"))

    elif lexem == "УПЛ":
        m = STACK.pop()
        exp = STACK.pop()
        STACK.append(wrap(f"if (.not. ({exp})) goto {m}"))

    elif lexem == "БП":
        STACK.append(wrap(f"goto {STACK.pop()}"))

    elif lexem == ":":
        m = STACK.pop()
        op = STACK.pop()
        STACK.append(wrap(op, m))

    elif lexem == "ARR":
        n = int(STACK.pop())
        params = STACK[-n:]
        del STACK[-n:]
        STACK.append(f"(/{','.join(params)}/)")

    elif lexem == "WH":
        STACK.append(wrap(f"do while({STACK.pop()})"))

    elif lexem == "FOR":
        params = STACK[-3:]
        del STACK[-3:]
        STACK.append(params[0])
        STACK.append(wrap(f"do while({params[1]})"))
        step = params[2]

    elif lexem == "END":
        if step:
            STACK.append(step)
            step = ""
        STACK.append(wrap("end do"))

    elif lexem == "R2":
        # OUTPUT.extend(STACK)
        STACK.append("\n")
        # STACK.clear()

    else:
        STACK.append(lexem)

with open(output_dir + name + "_mach.txt", "w", encoding="utf-8") as write_file:
    OUTPUT.extend(STACK)
    write_file.write("".join(OUTPUT))
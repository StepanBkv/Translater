import re
from os import path
from anytree import Node, RenderTree

with open("settings.txt", "r", encoding="utf-8") as read_file:
    input_file = read_file.readline().strip()
    output_dir = read_file.readline().strip()

name = path.basename(input_file)
name = path.splitext(name)[0]
with open(output_dir + name + "_mach.txt", "r") as read_file:
    INPUT = read_file.read()


# обработка входного текста
def process(text):
    not_character = True
    temp = ""
    for char in INPUT:
        if (char == " " or char == "\n") and not_character:
            char = "*"
        if char == "\"":
            not_character = not not_character
        temp += char

    temp = temp.split("*")
    temp = [str.replace("*", " ") for str in temp]

    temp1 = []
    for str in temp:
        temp1.extend(re.split("([\(\)\,/\[\]])", str))

    temp = list(filter(bool, temp1))
    temp1 = []
    for lexem in temp:
        if lexem[0] != "\"" and lexem[-1] != "\"":
            temp1.extend(re.split("(\n)", lexem))
        else:
            temp1.append(lexem)

    return list(filter(bool, temp1))


str_counter = 0
error = ""


# анализ обработанного текста
def get(point):
    if point < len(program_text):
        return program_text[point]
    else:
        return '/n'


def text(point, parent):
    global str_counter
    str_counter += 1
    if (p := string(point, parent)):
        if (p1 := text(p, parent)):
            return p1
        return p
    else:
        error = f"Error in string {str_counter}"


def string(point, parent):
    if m(point) and (p := operator(point + 1, parent)) or \
            (p := operator(point, parent)) or \
            (p := description(point, parent)):
        return p


def function(point, parent):
    node = Node("function")
    if get(point) == "function" and identificator(point + 1) and get(point + 2) == "(" and get(point + 3) == ")" and (
    p := text(point + 4, node)) and get(p) == "end" and get(p + 1) == "function" and identificator(p + 2) or \
            get(point) == "function" and identificator(point + 1) and get(point + 2) == "(" and (
    p := arguments(point + 3, node)) and get(p) == ")" and (p := text(p + 1, node)) and get(p) == "end" and get(
        p + 1) == "function" and identificator(p + 2):
        node.parent = parent
        node.data = program_text[point:p + 3]
        return p + 3


def program(point, parent):
    node = Node("program")
    if get(point) == "program" and identificator(point + 1) and (p := text(point + 2, node)) and get(
            p) == "end" and get(p + 1) == "program" and identificator(p + 2):
        node.parent = parent
        node.data = program_text[point:p + 3]
        return p + 3


def subroutine(point, parent):
    node = Node("subroutine")
    if get(point) == "subroutine" and identificator(point + 1) and get(point + 2) == "(" and get(point + 3) == ")" and (
    p := text(point + 4, node)) and get(p) == "end" and get(p + 1) == "subroutine" and identificator(p + 2) or \
            get(point) == "subroutine" and identificator(point + 1) and get(point + 2) == "(" and (
    p := arguments(point + 3, node)) and get(p) == ")" and (p := text(p + 1, node)) and get(p) == "end" and get(
        p + 1) == "subroutine" and identificator(p + 2):
        node.parent = parent
        node.data = program_text[point:p + 3]
        return p + 3


def do_while(point, parent):
    node = Node("while")
    if get(point) == "do" and get(point + 1) == "while" and get(point + 2) == "(" and (
    p := condition(point + 3, node)) and get(p) == ")" and (p := text(p + 1, node)) and get(p) == "end" and get(
            p + 1) == "do":
        node.parent = parent
        node.data = program_text[point:p + 2]
        return p + 2


def m(p):
    return get(p) not in ["call", "function", "subroutine"] and re.match("^[\d\w]{1,5}$", get(p))


def description(point, parent):
    node = Node("value description")
    if get(point) == "integer" and get(point + 1) == "::" and (p := parametrs(point + 2)):
        node.parent = parent
        node.data = program_text[point:p]
        return p
    if get(point) == "real" and get(point + 1) == "::" and (p := parametrs(point + 2)):
        node.parent = parent
        node.data = program_text[point:p]
        return p
    if get(point) == "character" and get(point + 1) == "::" and (p := parametrs(point + 2)):
        node.parent = parent
        node.data = program_text[point:p]
        return p
    if get(point) == "integer" and get(point + 1) == "," and get(point + 2) == "dimension" and get(
            point + 3) == "(" and (p := arguments(point + 4, node)) and get(p) == ")" and get(p + 1) == "::" and (
    p := parametrs(p + 2)):
        node.parent = parent
        node.data = program_text[point:p]
        return p
    if get(point) == "real" and get(point + 1) == "," and get(point + 2) == "dimension" and get(point + 3) == "(" and (
    p := arguments(point + 4, node)) and get(p) == ")" and get(p + 1) == "::" and (p := parametrs(p + 2)):
        node.parent = parent
        node.data = program_text[point:p]
        return p
    if get(point) == "character" and get(point + 1) == "," and get(point + 2) == "dimension" and get(
            point + 3) == "(" and (p := arguments(point + 4, node)) and get(p) == ")" and get(p + 1) == "::" and (
    p := parametrs(p + 2)):
        node.parent = parent
        node.data = program_text[point:p]
        return p


def if_operator(point, parent):
    node = Node("conditional operator")
    if get(point) == "if" and get(point + 1) == "(" and (p := condition(point + 2, node)) and get(p) == ")" and (
    p := operator(p + 1, node)):
        node.parent = parent
        node.data = program_text[point:p]
        return p


def condition(point, parent):
    if get(point) == ".not." and get(point + 1) == "(" and (p := condition(point + 2, parent)) and get(p) == ")":
        return p + 1
    if (p := expression(point, parent)) and compare(p) and (p := expression(p + 1, parent)):
        return p


def compare(point):
    return get(point) in ['.LT.', '.GT.', '.EQ.', '.NE.', '.LE.', '.GE.']


def operator(point, parent):
    if p := assign(point, parent):
        return p
    if p := if_operator(point, parent):
        return p
    if p := goto(point, parent):
        return p
    if p := call_sub(point, parent):
        return p
    if p := call_func(point, parent):
        return p
    if p := program(point, parent):
        return p
    if p := function(point, parent):
        return p
    if p := subroutine(point, parent):
        return p
    if p := do_while(point, parent):
        return p


def assign(point, parent):
    node = Node("assign operator")
    if identificator(point) and get(point + 1) == "=" and (p := expression(point + 2, node)):
        node.parent = parent
        node.data = program_text[point:p]
        return p
    if identificator(point) and get(point + 1) == "=" and get(point + 2) == "(" and get(point + 3) == "/" and (
    p := arguments(point + 4, node)) and get(p) == "/" and get(p + 1) == ")":
        node.parent = parent
        node.data = program_text[point:p + 2]
        return p + 2


def goto(point, parent):
    node = Node("unconditional jump")
    if get(point) == "goto" and m(point + 1):
        node.parent = parent
        node.data = program_text[point:point + 2]
        return point + 2


def call_sub(point, parent):
    node = Node("subroutine call")
    if get(point) == "call" and identificator(point + 1) and get(point + 2) == "(" and get(point + 3) == ")":
        node.parent = parent
        node.data = program_text[point:point + 4]
        return point + 4
    if get(point) == "call" and identificator(point + 1) and get(point + 2) == "(" and (
    p := arguments(point + 3, node)) and get(p) == ")":
        node.parent = parent
        node.data = program_text[point:p + 1]
        return p + 1


def call_func(point, parent):
    node = Node("function call")
    if identificator(point) and get(point + 1) == "(" and get(point + 2) == ")":
        node.parent = parent
        node.data = program_text[point:point + 3]
        return point + 3
    if identificator(point) and get(point + 1) == "(" and (p := arguments(point + 2, node)) and get(p) == ")":
        node.parent = parent
        node.data = program_text[point:p + 1]
        return p + 1


def identificator(point):
    return re.match("^[\d\w_]+$", get(point))


def expression(point, parent):
    if (p := argument(point, parent)) and operation(p) and (p := expression(p + 1, parent)):
        return p
    if get(point) == "(" and (p := expression(point + 1, parent)) and get(p) == ")":
        return p + 1
    if get(point) == "-" and (p := expression(point + 1, parent)):
        return p
    if p := argument(point, parent):
        return p


def parametrs(point):
    if identificator(point) and get(point + 1) == "," and (p := parametrs(point + 2)):
        return p
    if identificator(point):
        return point + 1


def arguments(point, parent):
    if (p := argument(point, parent)):
        if get(p) == "," and (p1 := arguments(p + 1, parent)):
            return p1
        return p


def argument(point, parent):
    if const(point):
        return point + 1
    if (p := call_func(point, parent)):
        return p
    if identificator(point) and get(point + 1) == "[" and (p := argument(point + 2, parent)) and get(p) == "]":
        return p + 1
    if identificator(point):
        return point + 1


def const(point):
    return character(point) or integer(point) or real(point)


def character(point):
    return get(point)[0] == "\"" and get(point)[-1] == "\""


def integer(point):
    return re.match("\d+", get(point))


def real(point):
    return re.match("\d*\.\d*", get(point))


def operation(point):
    if get(point) in ["+", "-", "*", "/", "**", "%"]:
        return True


program_text = process(INPUT)
point = 0
root = Node("program_text")

while p := text(point, root):
    point = p

if point < len(program_text):
    error = f"Error in string {str_counter}"

if error:
    print(f"Uncorrect syntax in line {str_counter}")
else:
    print("Successful")
    with open(output_dir + name + "_sin.txt", "w", encoding="utf-8") as write_file:
        for pre, fill, node in RenderTree(root):
            write_file.write("%s%s\n" % (pre, node.name))
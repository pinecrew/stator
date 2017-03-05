#!/usr/bin/env python3

from pyparsing import Group, SkipTo, Forward, Word, ZeroOrMore, OneOrMore, Optional, StringEnd, alphas, nums

alphabet = alphas + nums + " ,.?!':;\\_@()[]\n\t"

def command(name, required_args=1, optional_args=0):
    rq_arg = "{" + Word(alphabet) + "}"
    op_arg = "[" + Word(alphabet) + "]"
    # TODO: нужно придумать, как передавать позиции оптиональных и неопциональных аргументов
    cmd = "\\" + name + optional_args * op_arg + required_args * rq_arg
    return Group(cmd).setResultsName("cmd")

def environment(name):
    return Group("\\begin{" + name + "}" + Word(alphabet) + "\\end{" + name + "}").setResultsName("env")

section = Forward()
subsection = Forward()
subsubsection = Forward()
section << Group(command("section") + SkipTo(section | StringEnd() | subsection) + ZeroOrMore(subsection))
subsection << Group(command("subsection") + SkipTo(section | subsection | StringEnd() | subsubsection) + ZeroOrMore(subsubsection))
subsubsection << Group(command("subsubsection") + SkipTo(section | subsection | subsubsection | StringEnd()))


# команды
title = command("title")
b = command("b")
i = command("i")
u = command("u")
s = command("s")
url = command("url", 2)
inc = command("includegraphics")

# окружения
ep = environment("epigraph")
eq = environment("equation")
fig = environment("figure")


entire_file = Group(SkipTo(section) + ZeroOrMore(section))
parse_list = entire_file.parseFile("test.tex").asList()
# print(parse_list)
print(parse_list[0][0])
for i in parse_list[0][1:]:
    print(i)

# Идея такая: сначала определяем иерархию,
# потом проводим замены в различных частях
# команд и окружений
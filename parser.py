#!/usr/bin/env python3

from pyparsing import Group, SkipTo, Forward, Word, ZeroOrMore, OneOrMore, Optional, StringEnd, alphanums, alphas, matchPreviousExpr, MatchFirst

alphabet = alphanums + " ,.?!':;@()[]\n\t"

# def command(name, required_args=1, optional_args=0):
#     rq_arg = "{" + Word(alphabet) + "}"
#     op_arg = "[" + Word(alphabet) + "]"
#     # TODO: нужно придумать, как передавать позиции оптиональных и неопциональных аргументов
#     cmd = "\\" + name + (op_arg + required_args * rq_arg
#     return Group(cmd).setResultsName("cmd")

# def environment(name):
#     return Group("\\begin{" + name + "}" + Word(alphabet) + "\\end{" + name + "}").setResultsName("env")



# команды
# title = command("title")
# b = command("b")
# i = command("i")
# u = command("u")
# s = command("s")
# url = command("url", 2)
# fig = command("figure", 2)

# # окружения
# ep = environment("epigraph")
# eq = environment("equation")
# quote = environment("quote")
# code = environment("code")

text = Word(alphabet)
content = Forward()
env_open = Word(alphas)
env_close = matchPreviousExpr(env_open)
env = MatchFirst(Group("\\begin{" + env_open + "}" + ZeroOrMore("[" + content + "]") + ZeroOrMore("{" + content + "}") + content + "\end{" + env_close + "}").setResultsName("env"))
cmd = Group("\\" + Word(alphas) + ZeroOrMore("[" + content + "]") + ZeroOrMore("{" + content + "}")).setResultsName("cmd")
content << ((text | env | cmd) + Optional(content))

# section = Forward()
# subsection = Forward()
# subsubsection = Forward()
# section << Group(command("section") + Optional(content) + (section | StringEnd() | subsection) + ZeroOrMore(subsection))
# subsection << Group(command("subsection") + Optional(content) + (section | subsection | StringEnd() | subsubsection) + ZeroOrMore(subsubsection))
# subsubsection << Group(command("subsubsection") + Optional(content) + (section | subsection | subsubsection | StringEnd()))


# entire_file = Group(SkipTo(section) + ZeroOrMore(section))
parse_list = content.parseFile("test.tex").asList()
print(parse_list)
# print(parse_list[0][0])
# for i in parse_list[0][1:]:
#     print(i)

# Идея такая: сначала определяем иерархию,
# потом проводим замены в различных частях
# команд и окружений
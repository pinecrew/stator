#!/usr/bin/env python3
from pyparsing import *

### Описание грамматики
tex = Forward()
# Просто текст. Srange нужен для поддержки русского
plain_text = alphanums + srange(r"[\0x80-\0x7FF]") + ".,;:'!? "
# Экранирование
escape = "\\"
# Ключевое понятие теха
group = "{" + tex + "}"
# Команда. Необязательные аргументы пока не поддерживаются
opt_arg = "[" + tex + "]"
args = Forward()
args << (group | opt_arg) + Optional(args)
command = Group(escape + Word(alphas) + Optional(args))
# Математический треш -- то, что находится внутри формул
math = Forward()
math_group = "{" + math + "}"
math_opt_arg = "[" + tex + "]"
math_args = Forward()
math_args << (group | opt_arg) + Optional(math_args)
math_command = Group(escape + Word(alphas) + Optional(math_args))
math << (Word(plain_text + "^_+-*/()[]=") | math_command | math_group) + Optional(math)
# Блоки кода
code = Group("\\begin{code}" + Optional(args) + Word(plain_text + "(){}[]\"'\n\t") + "\\end{code}")
inline_eq = Combine("\\(" + math + "\\)")
eq = Combine("\\[" + math + "\\]")
comment = Group("%" + SkipTo(LineEnd()))
tex << (Word(plain_text) | group | inline_eq | eq | comment | code | command) + Optional(tex)

test = r'''
\begin{epigraph}
    У этой штуки был фатальный недостаток...
\end{epigraph}

\section{Немного арифметики}
Попробуем разные виды формул: \( f(x) = \sin{x} \)
\( \sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} + o(x^6) \) % проверка комментария

\subsection{Вопрос вот в чём: чему равно \( \zeta(3) \)?}
\[
    \zeta(3) = \sum_{n = 1}^\infty \frac{1}{n^3}
\]

% comment code
% \subsection{123}
\begin{code}[rust]
    fn main() {
        println!("Hello World!");
    }
\end{code}
'''

tokens = tex.parseString(test).asList()
for token in tokens:
    print(token)

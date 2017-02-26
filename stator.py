#!/usr/bin/env python3
import os
import re
import shutil
from hashlib import md5
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


template = r'''
\documentclass[10pt]{article}
\usepackage{graphics}
\usepackage{geometry}
\usepackage{amsmath}

\pagestyle{empty}
\newsavebox{\mybox}

\newlength{\mywidth}
\newlength{\myheight}
\newlength{\mydepth}

\setlength{\topskip}{0pt}
\setlength{\parindent}{0pt}
\setlength{\abovedisplayskip}{0pt}
\setlength{\belowdisplayskip}{0pt}

\begin{lrbox}{\mybox}
\scalebox{1.5}{%s}
\end{lrbox}

\settowidth {\mywidth}  
    {\usebox{\mybox}}
\settoheight{\myheight}
    {\usebox{\mybox}}
\settodepth {\mydepth}
    {\usebox{\mybox}}

\newwrite\foo
\immediate\openout\foo=\jobname.depth
    \immediate\write\foo{\the\mydepth}
\closeout\foo

%% set the paper-size and do everything in one pdflatex run
\addtolength{\myheight} {\mydepth}
\geometry{paperwidth=\mywidth,
    paperheight=\myheight,margin=0pt}

\begin{document}
\usebox{\mybox}
\end{document}
'''

def tex_to_svg(tex):
    file_contents = template % tex
    file_name = md5(file_contents.encode()).hexdigest()
    with open("/tmp/{}.tex".format(file_name), "w") as f:
        f.write(file_contents)
    os.system("latex -output-directory=/tmp /tmp/{}.tex".format(file_name))
    os.system("dvisvgm --exact --no-fonts /tmp/{0}.dvi -o /tmp/{0}.svg".format(file_name))
    os.system("python3 -m scour.scour --strip-xml-prolog --enable-viewboxing --enable-id-stripping --enable-comment-stripping --shorten-ids --indent=none -i /tmp/{0}.svg -o /tmp/{0}1.svg".format(file_name))
    depth = "0pt"
    with open("/tmp/{}.depth".format(file_name), "r") as f:
        depth = f.read().strip()
    svg = ""
    with open("/tmp/{}1.svg".format(file_name), "r") as f:
        svg = f.read().strip()
    svg = "{} style=\"vertical-align: -{};\" {}".format(svg[:4], depth, svg[4:])
    return svg


def code_highlight(code, lang="bash"):
    # print(code)
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = HtmlFormatter(cssclass="source")
    return highlight(code, lexer, formatter)


def render(filename):
    with open(filename, "r") as f:
        text = f.read()
    i = text.find("~~~")
    meta = text[:i]
    text = text[i+3:].strip()
    metadata = {}
    for i in meta.split("\n"):
        if i.strip():
            print("i is", i)
            k, v = i.split(":")
            metadata[k.strip()] = v.strip()
    if "layout" not in metadata:
        metadata["layout"] = "base"
    with open("layouts/{layout}.html".format(**metadata), "r") as f:
        layout = f.read()
    print("1")
    result = re.sub(r"```(\w+)\n([\s\S]*?)```", lambda m: "<p>{}</p>".format(code_highlight(m.group(2), m.group(1))), text)
    print("2")
    result = re.sub(r"`([\s\S]*?)`", lambda m: "<code>{}</code>".format(m.group(1)), result)
    result = re.sub(r"(\\\([\s\S]*?\\\))", lambda m: tex_to_svg(m.group(1)), result)
    result = re.sub(r"(\\\[[\s\S]*?\\\])", lambda m: "<p class=formula>{}</p>".format(tex_to_svg(m.group(1))), result)
    result = layout % result
    
    with open("site/" + filename, "w") as f:
        f.write(result)

if __name__ == '__main__':
    pages = filter(lambda s: s.endswith(".html"), os.listdir())
    if os.path.exists("site"):
        shutil.rmtree("site")
    os.mkdir("site")
    for page in pages:
        render(page)
    for f in ["styles", "fonts", "img"]:
        shutil.copytree(f, "site/" + f)

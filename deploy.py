#!/usr/bin/python
# python 3 is what we use
import os, re
from shutil import copyfile

with open("_book/index.html", "rt") as fin:
    with open("index.html", "wt") as fout:
        for line in fin:
            line = line.replace('href="gitbook', 'href="site/gitbook')
            line = line.replace('src="gitbook', 'src="site/gitbook')
            fout.write(line)


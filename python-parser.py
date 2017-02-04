__author__ = 'lan'
from os.path import isfile
import re
import os
import sys

class PythonParser:
    def __init__(self):
        self.indent_dict = {'tab': 0, 'space': 0}
        self.line_length_dict = {'char80': 0, 'char120': 0, 'char150': 0}
        self.imports_dict = {'separated': 0, 'non_separated': 0}
        self.whitespace_dict = {'non_extra': 0, 'extra': 0}

    def parse(self, py_file):
        if not isfile(py_file) or not py_file.endswith('.py'):
            print "wrong type. need .py file."
            exit(1)

        with open(py_file, 'r') as fd:
            stream = fd.read()
            self.indent(stream)
            self.line_length(stream)
            self.imports(stream)
            self.whitespace(stream)

    def indent(self, stream):
        tab_pattern = re.compile(r'^\t+.*', re.M)
        space_pattern = re.compile(r'^\s+.*', re.M)

        tab_re = re.findall(tab_pattern, stream)
        if tab_re is not None:
            self.indent_dict['tab'] += len(tab_re)

        space_re = re.findall(space_pattern, stream)
        if space_re is not None:
            self.indent_dict['space'] += len(space_re)

    def line_length(self, stream):
        stream_list = stream.split('\n')
        for each_line in stream_list:
            if each_line.__len__() < 80:
                self.line_length_dict['char80'] += 1
            elif each_line.__len__() < 120:
                self.line_length_dict['char120'] += 1
            else:
                self.line_length_dict['char150'] += 1

    def imports(self, stream):
        separated_pattern = re.compile(r'^\s*\t*import\s+[\w.]+([^,]\s*|\s*#.*)$', re.M)
        non_separated_pattern = re.compile(r'^\s*\t*import\s+\w+\s*,\s+\w+', re.M)

        separated_re = re.findall(separated_pattern, stream)
        if separated_re is not None:
            self.imports_dict['separated'] += len(separated_re)

        non_separated_re = re.findall(non_separated_pattern, stream)
        if non_separated_re is not None:
            self.imports_dict['non_separated'] += len(non_separated_re)

    def whitespace(self, stream):
        non_extra_pattern = re.compile(r'\S+[\(\)\[\],]\S+|\S+:\s|\S\s=\s', re.M)  # redundant whitespace occurs in three cases: , : =
        extra_pattern = re.compile(r'\(\s+|\s+[\(\)\[\]]|\s+[:,]\s+|\s{2,}=|=\s{2,}', re.M)

        non_extra_re = re.findall(non_extra_pattern, stream)
        if non_extra_re is not None:
            self.whitespace_dict['non_extra'] += len(non_extra_re)

        extra_re = re.findall(extra_pattern, stream)
        if extra_re is not None:
            self.whitespace_dict['extra'] += len(extra_re)


if __name__ == '__main__':
    py_parser = PythonParser()
    # a.parse("E:\\Python_workspace\\popularconvention\\python-parser.py")

    dir_path = url = sys.argv[1]
    # dir_path = '/Users/sun/Workspace/Coding_Convention'
    for file_name in os.listdir(dir_path):
        if not file_name.endswith('.py'):
            continue
        print "Parsing file : " + file_name
        py_parser.parse(os.path.join(dir_path, file_name))
    print py_parser.indent_dict
    print py_parser.line_length_dict
    print py_parser.imports_dict
    print py_parser.whitespace_dict

__author__ = 'yyq'
from os.path import isfile
import re
import os
import sys

class cplusplusParser:
    def __init__(self):
        self.indent_dict = {'tab': 0, 'space': 0}
        self.block_statement_dict = {'one_space': 0, 'no_space': 0, 'new_line': 0}
        self.constant_dict = {'pascal': 0,'all_caps': 0, 'not_all_caps': 0}
        self.condition_statement_dict = {'one_space': 0, 'no_space': 0}
        self.argument_dict = {'one_space': 0, 'no_space': 0}
        self.line_length_dict = {'char80': 0, 'char120': 0, 'char150': 0}

    def parse(self, cpp_file):
        if not isfile(cpp_file) or (not cpp_file.endswith('.cpp')  and not cpp_file.endswith('.h')):
            print "wrong type. need .cpp file or .h file."
            exit(1)

        with open(cpp_file, 'r') as fd:
            stream = fd.read()
            self.indent(stream)
            self.block_statement(stream)
            self.constant(stream)
            self.condition_statement(stream)
            self.argument(stream)
            self.line_length(stream)

    def indent(self, stream):
        tab_pattern = re.compile(r'^\t+.*', re.M)
        space_pattern = re.compile(r'^\s+.*', re.M)

        tab_re = re.findall(tab_pattern, stream)
        if tab_re is not None:
            self.indent_dict['tab'] += len(tab_re)

        space_re = re.findall(space_pattern, stream)
        if space_re is not None:
            self.indent_dict['space'] += len(space_re)

    def block_statement(self, stream):
        one_space_pattern = re.compile(r'((if|while|switch|try).*\s+\{)|(\}\s+(else|catch|finally).*\s+\{)', re.M)
        no_space_pattern = re.compile(r'((if|while|switch).*\)\{)|(try|else|finally)\{|(\}\s*(else|catch|finally).*\)\{)', re.M)
        new_line_pattern = re.compile(r'((if|while|switch).*\)\s*$)|((if|while|switch).*\)\s*\/[\/\*])|(try|else|finally)\s*\/[\/\*]|(^\s*(else|catch|finally))', re.M)

        one_space_re = re.findall(one_space_pattern, stream)
        if one_space_re is not None:
            self.block_statement_dict['one_space'] += len(one_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.block_statement_dict['no_space'] += len(no_space_re)

        new_line_re = re.findall(new_line_pattern, stream)
        if new_line_re is not None:
            self.block_statement_dict['new_line'] += len(new_line_re)

    def constant(self, stream):
        pascal_pattern = re.compile(r'const\s+\w+\s+([A-Z][a-z0-9]+)+\s*=', re.M)
        all_caps_pattern = re.compile(r'const\s+\w+\s+([A-Z0-9_]+)+\s*=', re.M)
        no_all_caps_pattern = re.compile(r'const\s+\w+\s+([a-z][A-Za-z0-9_]*)+\s*=', re.M)

        pascal_re = re.findall(pascal_pattern, stream)
        if pascal_re is not None:
          self.constant_dict['pascal'] += len(pascal_re)

        all_caps_re = re.findall(all_caps_pattern, stream)
        if all_caps_re is not None:
            self.constant_dict['all_caps'] += len(all_caps_re)

        no_all_caps_re = re.findall(no_all_caps_pattern, stream)
        if no_all_caps_re is not None:
            self.constant_dict['not_all_caps'] += len(no_all_caps_re)

    def condition_statement(self, stream):
        one_space_pattern = re.compile(r'(if|while|switch)\s+\(', re.M)
        no_space_pattern = re.compile(r'(if|while|switch)\(', re.M)

        one_space_re = re.findall(one_space_pattern, stream)
        if one_space_re is not None:
            self.condition_statement_dict['one_space'] += len(one_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.condition_statement_dict['no_space'] += len(no_space_re)

    def argument(self, stream):
        one_space_pattern = re.compile(r'^(\s*|\t*)(\w+\s+\w+\s+\w+|if|while|switch)\s*\(\s+', re.M)
        no_space_pattern = re.compile(r'^(\s*|\t*)(\w+\s+\w+\s+\w+|if|while|switch)\s*\(\S+', re.M)

        one_space_re = re.findall(one_space_pattern, stream)
        if one_space_re is not None:
            self.argument_dict['one_space'] += len(one_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.argument_dict['no_space'] += len(no_space_re)

    def line_length(self, stream):
        stream_list = stream.split('\n')
        for each_line in stream_list:
            if each_line.__len__() < 80:
                self.line_length_dict['char80'] += 1
            elif each_line.__len__() < 120:
                self.line_length_dict['char120'] += 1
            else:
                self.line_length_dict['char150'] += 1

if __name__ == '__main__':
    cpp_parser = cplusplusParser()
    dir_path = url = sys.argv[1]
    for file_name in os.listdir(dir_path):
        print file_name
        if not file_name.endswith('.cpp') and not file_name.endswith('.h'):
            continue
        print "Parsing file : " + file_name
        cpp_parser.parse(os.path.join(dir_path, file_name))
    print cpp_parser.indent_dict
    print cpp_parser.block_statement_dict
    print cpp_parser.constant_dict
    print cpp_parser.condition_statement_dict
    print cpp_parser.argument_dict
    print cpp_parser.line_length_dict
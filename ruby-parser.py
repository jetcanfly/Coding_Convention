__author__ = 'lan'
from os.path import isfile
import re
import os
import sys
from multiprocessing import Process
from multiprocessing.managers import BaseManager


class RubyParser:
    def __init__(self):
        self.indent_dict = {'tab': 0, 'space': 0}
        self.line_length_dict = {'char80': 0, 'char120': 0, 'char150': 0}
        self.whitespace_dict = {'spaces': 0, 'no_space': 0}
        self.assign_default_val_dict = {'spaces': 0, 'no_space': 0}
        self.numeric_literal_dict = {'underscore': 0, 'no_underscore': 0}
        self.def_no_args_dict = {'omit': 0, 'use': 0}
        self.def_args_dict = {'omit': 0, 'use': 0}

    def parse(self, rb_file):
        if not isfile(rb_file) or not rb_file.endswith('.rb'):
            print "wrong type. need .rb file."
            exit(1)

        with open(rb_file, 'r') as fd:
            stream = fd.read()
            self.indent(stream)
            self.line_length(stream)
            self.whitespace(stream)
            self.assign_default_val(stream)
            self.numeric_literal(stream)
            self.def_no_args(stream)
            self.def_args(stream)

    def indent(self, stream):
        tab_pattern = re.compile(r'^\t+.*', re.M)
        space_pattern = re.compile(r'^ +.*', re.M)

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

    def whitespace(self, stream):
        replace_comment = "CONVENTION-PLACEHOLDER"  # eliminate disturbing string
        operators = '[+=*/%>?:{}]'
        symbols = '[,;]'

        spaces_pattern1 = re.compile(r'\w+{}'.format(operators))
        spaces_pattern2 = re.compile(r'{}\w+'.format(operators))
        spaces_pattern3 = re.compile(r'{}\w+'.format(symbols))
        spaces_pattern4 = re.compile(r'\s+{}\s+'.format(operators))
        spaces_pattern5 = re.compile(r'\s+{}\s+'.format(symbols))

        no_spaces_pattern1 = re.compile(r'\w+{}'.format(operators))
        no_spaces_pattern2 = re.compile(r'{}\w+'.format(operators))
        no_spaces_pattern3 = re.compile(r'{}\w+'.format(symbols))

        stream_list = stream.split('\n')
        for each_line in stream_list:
            new_line = re.sub(r"'.*?'", replace_comment, each_line)
            new_line = re.sub(r'".*?"', replace_comment, new_line)
            if re.search(spaces_pattern1, new_line) is None and \
               re.search(spaces_pattern2, new_line) is None and \
               re.search(spaces_pattern3, new_line) is None:
                if re.search(spaces_pattern4, new_line) is not None or \
                   re.search(spaces_pattern5, new_line) is not None:
                    self.whitespace_dict['spaces'] += 1
            elif re.search(no_spaces_pattern1, new_line) is not None or \
                 re.search(no_spaces_pattern2, new_line) is not None or \
                 re.search(no_spaces_pattern3, new_line) is not None:
                self.whitespace_dict['no_space'] += 1

    def assign_default_val(self, stream):
        spaces_pattern = re.compile(r'^[\s\t]*def.*\((\s*\w+\s+=\s+[\[\]:\w,]+\s*)+\)', re.M)
        no_space_pattern = re.compile(r'^[\s\t]*def.*\((\s*\w+=[\[\]:\w,]+\s*)+\)', re.M)

        spaces_re = re.findall(spaces_pattern, stream)
        if spaces_re is not None:
            self.assign_default_val_dict['spaces'] += len(spaces_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.assign_default_val_dict['no_space'] += len(no_space_re)

    def numeric_literal(self, stream):
        replace_comment = "CONVENTION-PLACEHOLDER"  # eliminate disturbing string
        underscore_pattern = re.compile(r'[0-9]+(_[0-9]{3,})+', re.M)
        no_underscore_pattern = re.compile(r'[0-9]{4,}', re.M)

        new_stream = re.sub(r"'.*?'", replace_comment, stream)
        new_stream = re.sub(r'".*?"', replace_comment, new_stream)

        underscore_re = re.findall(underscore_pattern, new_stream)
        if underscore_re is not None:
            self.numeric_literal_dict['underscore'] += len(underscore_re)

        no_underscore_re = re.findall(no_underscore_pattern, new_stream)
        if no_underscore_re is not None:
            self.numeric_literal_dict['no_underscore'] += len(no_underscore_re)

    def def_no_args(self, stream):
        omit_pattern = re.compile(r'^[\s\t]*def\s+\w+\s*[^(),\w]*(#+.*)*$', re.M)
        use_pattern = re.compile(r'^[\s\t]*def\s+\w+\s*\(\s*\)', re.M)

        omit_re = re.findall(omit_pattern, stream)
        if omit_re is not None:
            self.def_no_args_dict['omit'] += len(omit_re)

        use_re = re.findall(use_pattern, stream)
        if use_re is not None:
            self.def_no_args_dict['use'] += len(omit_re)

    def def_args(self, stream):
        omit_pattern = re.compile(r'^[\s\t]*def\s+\w+\s+\w[^()]*(#+.*)*$', re.M)
        use_pattern = re.compile(r'^[\s\t]*def\s+\w+\s*\((\s*[\w=]+,?)+\s*', re.M)

        omit_re = re.findall(omit_pattern, stream)
        if omit_re is not None:
            self.def_args_dict['omit'] += len(omit_re)

        use_re = re.findall(use_pattern, stream)
        if use_re is not None:
            self.def_args_dict['use'] += len(use_re)

    def __str__(self):
        return_string = ''
        for each in self.__dict__:
            if each.endswith('_dict'):
                return_string += '{}: '.format(each).ljust(30)
                return_string += '{}\n'.format(self.__dict__[each])
        return return_string


class MyManager(BaseManager):
    pass


def manager():
    m = MyManager()
    m.start()
    return m

MyManager.register('RubyParser', RubyParser)


def run(ruby_parser, rb_file):
    t1 = Process(target=ruby_parser.parse, args=(rb_file,))
    t1.start()
    t1.join(10)
    if t1.is_alive():
        t1.terminate()

if __name__ == '__main__':
    manager = manager()
    rb_parser = manager.RubyParser()
    dir_path = url = sys.argv[1]
    file_count = 0
    for file_name in os.listdir(dir_path):
        if not file_name.endswith('.rb'):
            continue
        file_count += 1
        print str(file_count) + " Parsing file : " + file_name
        run(rb_parser, os.path.join(dir_path, file_name))
    print('\n')

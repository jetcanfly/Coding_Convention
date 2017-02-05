__author__ = 'lan'
from os.path import isfile
import re
import os
import sys
import threading


class JSParser:
    def __init__(self):
        self.indent_dict = {'tab': 0, 'space': 0}
        self.comma_dict = {'first': 0, 'last': 0}
        self.function_def_dict = {'one_space': 0, 'no_space': 0}
        self.argument_def_dict = {'one_space': 0, 'no_space': 0}
        self.literal_def_dict = {'trace_space': 0, 'both_space': 0, 'no_space': 0}
        self.condition_statement_dict = {'one_space': 0, 'no_space': 0}
        self.block_statement_dict = {'one_space': 0, 'no_space': 0, 'new_line': 0}
        self.line_length_dict = {'char80': 0, 'char120': 0, 'char150': 0}
        self.quotes_dict = {'single_quote': 0, 'double_quote': 0}

    def run(self, js_file):
        t1 = threading.Thread(target=self.parse, args=(js_file,))
        t1.start()
        t1.join(10)

    def parse(self, js_file):
        if not isfile(js_file) or not js_file.endswith('.js'):
            print "wrong type. need .js file."
            exit(1)

        with open(js_file, 'r') as fd:
            stream = fd.read()
            self.comma(stream)
            self.indent(stream)
            self.function_def(stream)
            self.argument_def(stream)
            self.literal_def(stream)
            self.condition_statement(stream)
            self.block_statement(stream)
            self.line_length(stream)
            self.quotes(stream)

    def comma(self, stream):
        first_pattern = re.compile(r'^\s*,.*', re.M)
        last_pattern = re.compile(r'.*,\s*$', re.M)

        first_re = re.findall(first_pattern, stream)
        if first_re is not None:
            self.comma_dict['first'] += len(first_re)

        last_re = re.findall(last_pattern, stream)
        if last_re is not None:
            self.comma_dict['last'] += len(last_re)

    def indent(self, stream):
        tab_pattern = re.compile(r'^\t+.*', re.M)
        space_pattern = re.compile(r'^\s+.*', re.M)

        tab_re = re.findall(tab_pattern, stream)
        if tab_re is not None:
            self.indent_dict['tab'] += len(tab_re)

        space_re = re.findall(space_pattern, stream)
        if space_re is not None:
            self.indent_dict['space'] += len(space_re)

    def function_def(self, stream):
        one_space_pattern = re.compile(r'function\s+\S+\s+\(', re.M)
        # no_space_pattern = re.compile(r'function(\s+.)*\(', re.M)
        no_space_pattern = re.compile(r'function\s+\S+\(', re.M)

        one_space_re = re.findall(one_space_pattern, stream)
        if one_space_re is not None:
            self.function_def_dict['one_space'] += len(one_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.function_def_dict['no_space'] += len(no_space_re)

    def argument_def(self, stream):
        one_space_pattern = re.compile(r'(function|if|while|switch)(\s+\w*)?\s*\(\s+', re.M)
        no_space_pattern = re.compile(r'(function|if|while|switch)(\s+\w*)?\s*\(\S+', re.M)

        one_space_re = re.findall(one_space_pattern, stream)
        if one_space_re is not None:
            self.argument_def_dict['one_space'] += len(one_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.argument_def_dict['no_space'] += len(no_space_re)

    def literal_def(self, stream):
        trace_space_pattern = re.compile(r'\w:\s+[\w"{}\/]'.format("'"), re.M)
        both_space_pattern = re.compile(r'\w\s+:\s+[\w"{}\/]'.format("'"), re.M)
        no_space_pattern = re.compile(r'\w:[\w"{}\/]'.format("'"), re.M)

        trace_space_re = re.findall(trace_space_pattern, stream)
        if trace_space_re is not None:
            self.literal_def_dict['trace_space'] += len(trace_space_re)

        both_space_re = re.findall(both_space_pattern, stream)
        if both_space_re is not None:
            self.literal_def_dict['both_space'] += len(both_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.literal_def_dict['no_space'] += len(no_space_re)

    def condition_statement(self, stream):
        one_space_pattern = re.compile(r'(if|while|switch)\s+\(', re.M)
        no_space_pattern = re.compile(r'(if|while|switch)\(', re.M)

        one_space_re = re.findall(one_space_pattern, stream)
        if one_space_re is not None:
            self.condition_statement_dict['one_space'] += len(one_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.condition_statement_dict['no_space'] += len(no_space_re)

    def block_statement(self, stream):
        one_space_pattern = re.compile(r'((if|while|switch).*\)\s+\{)|(\}\s+else)', re.M)
        no_space_pattern = re.compile(r'((if|while|switch).*\)\{)|(\}else)', re.M)
        new_line_pattern = re.compile(r'((if|while|switch).*\)\s*$)|((if|while|switch).*\)\s*\/[\/\*])|(^\s*else)', re.M)

        one_space_re = re.findall(one_space_pattern, stream)
        if one_space_re is not None:
            self.block_statement_dict['one_space'] += len(one_space_re)

        no_space_re = re.findall(no_space_pattern, stream)
        if no_space_re is not None:
            self.block_statement_dict['no_space'] += len(no_space_re)

        new_line_re = re.findall(new_line_pattern, stream)
        if new_line_re is not None:
            self.block_statement_dict['new_line'] += len(new_line_re)

    def line_length(self, stream):
        stream_list = stream.split('\n')
        for each_line in stream_list:
            if each_line.__len__() < 80:
                self.line_length_dict['char80'] += 1
            elif each_line.__len__() < 120:
                self.line_length_dict['char120'] += 1
            else:
                self.line_length_dict['char150'] += 1

    def quotes(self, stream):
        replace_comment = "CONVENTION-PLACEHOLDER"
        single_pattern1 = re.compile(r'{}'.format(replace_comment), re.M)
        single_pattern2 = re.compile(r'\"[\\w\\s<>/=]*{}[\\w\\s<>/=]*\"'.format(replace_comment), re.M)
        single_pattern3 = re.compile(r'"', re.M)

        double_pattern1 = re.compile(r'{}'.format(replace_comment), re.M)
        double_pattern2 = re.compile(r"'[\\w\\s<>/=]*{}[\\w\\s<>/=]*'".format(replace_comment), re.M)
        double_pattern3 = re.compile(r"'", re.M)

        new_stream = re.sub(r"'.*?'", replace_comment, stream)
        new_stream = new_stream.split('\n')
        for each_line in new_stream:
            if re.search(single_pattern1, each_line) is not None and \
               re.search(single_pattern2, each_line) is None and \
               re.search(single_pattern3, each_line) is None:
                self.quotes_dict['single_quote'] += 1

        new_stream = re.sub(r'".*?"', replace_comment, stream)
        new_stream = new_stream.split('\n')
        for each_line in new_stream:
            if re.search(double_pattern1, each_line) is not None and \
               re.search(double_pattern2, each_line) is None and \
               re.search(double_pattern3, each_line) is None:
                self.quotes_dict['double_quote'] += 1

    def __str__(self):
        return_string = ''
        for each in self.__dict__:
            if each.endswith('_dict'):
                return_string += '{}: '.format(each).ljust(30)
                return_string += '{}\n'.format(self.__dict__[each])
        return return_string


if __name__ == '__main__':
    js_parser = JSParser()
    print js_parser
    dir_path = url = sys.argv[1]
    for file_name in os.listdir(dir_path):
        if not file_name.endswith('.js'):
            continue
        print "Parsing file : " + file_name
        # js_parser.parse(os.path.join(dir_path, file_name))
        js_parser.run(os.path.join(dir_path, file_name))
    print('\n')
    print js_parser

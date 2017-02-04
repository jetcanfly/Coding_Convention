__author__ = 'lan'
from os.path import isfile
import re

class JavaParser:
    def __init__(self):
        self.indent_dict = {'tab': 0, 'space': 0}
        self.block_statement_dict = {'one_space': 0, 'no_space': 0, 'new_line': 0}
        self.constant_dict = {'all_caps': 0, 'not_all_caps': 0}
        self.condition_statement_dict = {'one_space': 0, 'no_space': 0}
        self.argument_dict = {'one_space': 0, 'no_space': 0}
        self.line_length_dict = {'char80': 0, 'char120': 0, 'char150': 0}
        self.static_var_dict = {'prefix': 0, 'no_prefix': 0}
        self.final_static_order_dict = {'accstfin': 0, 'accfinst': 0, 'finaccst': 0, 'staccfin': 0}

    def parse(self, java_file):
        if not isfile(java_file) or not java_file.endswith('.java'):
            print "wrong type. need .java file."
            exit(1)

        with open(java_file, 'r') as fd:
            stream = fd.read()
            self.indent(stream)
            self.block_statement(stream)
            self.constant(stream)
            self.condition_statement(stream)
            self.argument(stream)
            self.line_length(stream)
            self.static_var(stream)
            self.final_static_order(stream)

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
        all_caps_pattern = re.compile(r'^\s*\w*\s*(static\s+\w*\s*final\s|final\s+\w*\s*static\s)\w+\s[A-Z0-9_]+(\s|=|;)', re.M)
        no_all_caps_pattern = re.compile(r'^\s*\w*\s*(static\s+\w*\s*final\s|final\s+\w*\s*static\s)\w+\s[a-zA-Z0-9_]+(\s|=|;)', re.M)

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

    def static_var(self, stream):
        prefix_pattern = re.compile(r'static\s+\w+\s+(_|\$)\w+', re.M)
        no_prefix_pattern = re.compile(r'static\s+\w+\s+[^_$]\w+', re.M)

        prefix_re = re.findall(prefix_pattern, stream)
        if prefix_re is not None:
            self.static_var_dict['prefix'] += len(prefix_re)

        no_prefix_re = re.findall(no_prefix_pattern, stream)
        if no_prefix_re is not None:
            self.static_var_dict['no_prefix'] += len(no_prefix_re)

    def final_static_order(self, stream):
        accstfin_pattern = re.compile(r'^\w*\s*(public|private|protected){1}\s+\w*\s*(static){1}\s+\w*\s*(final|volatile){1}\s+\w+\s+[a-zA-Z0-9_]+(\s|=|;)', re.M)
        accfinst_pattern = re.compile(r'^\w*\s*(public|private|protected){1}\s+\w*\s*(final|volatile){1}\s+\w*\s*(static){1}\s+\w+\s+[a-zA-Z0-9_]+(\s|=|;)', re.M)
        finaccst_pattern = re.compile(r'^\w*\s*(final|volatile){1}\s+\w*\s*(public|private|protected){1}\s+\w*\s*(static){1}\s+\w+\s+[a-zA-Z0-9_]+(\s|=|;)', re.M)
        staccfin_pattern = re.compile(r'^\w*\s*(static){1}\s+\w*\s*(public|private|protected){1}\s+\w*\s*(final|volatile){1}\s+\w+\s+[a-zA-Z0-9_]+(\s|=|;)', re.M)

        accstfin_re = re.findall(accstfin_pattern, stream)
        if accstfin_re is not None:
            self.final_static_order_dict['accstfin'] += len(accstfin_re)

        accfinst_re = re.findall(accfinst_pattern, stream)
        if accfinst_re is not None:
            self.final_static_order_dict['accfinst'] += len(accfinst_re)

        finaccst_re = re.findall(finaccst_pattern, stream)
        if finaccst_re is not None:
            self.final_static_order_dict['finaccst'] += len(finaccst_re)

        staccfin_re = re.findall(staccfin_pattern, stream)
        if staccfin_re is not None:
            self.final_static_order_dict['staccfin'] += len(staccfin_re)


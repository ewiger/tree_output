# -*- coding: utf-8 -*-
'''
tree_output
===========

Python library to simplify building of tree output with command-line
interfaces.

Copyright (c) 2014 Yauhen Yakimovich
Licensed under the MIT License (MIT). Read a copy of LICENSE distributed with
this code.
'''
import sys
import json
import colorama
from colorama import Fore, Back, Style
from tree_output.version import version as tree_output_version

__version__ = tree_output_version


FOREMAP = {
    'black': Fore.BLACK,
    'red': Fore.RED,
    'green': Fore.GREEN,
    'yellow': Fore.YELLOW,
    'blue': Fore.BLUE,
    'magenta': Fore.MAGENTA,
    'cyan': Fore.CYAN,
    'white': Fore.WHITE,
    'reset': Fore.RESET,
}
BACKMAP = {
    'black': Back.BLACK,
    'red': Back.RED,
    'green': Back.GREEN,
    'yellow': Back.YELLOW,
    'blue': Back.BLUE,
    'magenta': Back.MAGENTA,
    'cyan': Back.CYAN,
    'white': Back.WHITE,
    'reset': Back.RESET,
}
STYLEMAP = {
    'dim': Style.DIM,
    'normal': Style.NORMAL,
    'bright': Style.BRIGHT,
    'reset_all': Style.RESET_ALL,
}


class HierarchicalOutput(object):

    def __init__(self):
        self.level = 0

    @staticmethod
    def factory(format='json'):
        format = format.lower()
        if format == 'json':
            return JsonOutput()
        elif format == 'ansi':
            return AnsiOutput()
        elif format == 'ascii':
            return AsciiOutput()
        elif format is None:
            return NullOutput()
        else:
            raise Exception('Unknown format')

    def emit(self, record, closed=False):
        '''
        Implement in format-specific adapter the aggregation of the output
        record.
        '''
        if closed:
            self.remove_level()

    def add_level(self):
        self.level += 1

    def remove_level(self):
        if self.level > 0:
            self.level -= 1


class NullOutput(HierarchicalOutput):

    def add_level(self):
        '''Do nothing'''

    def remove_level(self):
        '''Do nothing'''

    def emit(self, record, closed=False):
        '''Do nothing'''
        HierarchicalOutput.emit(self, record, closed)


class JsonOutput(HierarchicalOutput):

    def __init__(self):
        super(JsonOutput, self).__init__()
        self.data = list()
        self.root = self.data
        self.parents = list()
        self.parents.append(self.data)

    def add_level(self):
        super(JsonOutput, self).add_level()
        self.parents.append(self.data)
        sub_data = list()
        self.data.append(sub_data)
        self.data = sub_data

    def remove_level(self):
        super(JsonOutput, self).remove_level()
        if len(self.parents) > 0:
            self.data = self.parents.pop()

    def emit(self, record, closed=False):
        self.data.append(record)
        HierarchicalOutput.emit(self, record, closed)

    def __str__(self):
        '''Represent as JSON'''
        return json.dumps(self.root)


class AsciiOutput(HierarchicalOutput):

    def __init__(self):
        super(AsciiOutput, self).__init__()
        self.branch = '+-- '
        self.hanging_branch = '`-- '
        self.pipe_branch = '|   '

    def emit(self, record, closed=False):
        branch = self.branch
        # Accept values from the record.
        name = None
        colors = dict()
        if type(record) == dict:
            name = record.get('name')
            value = record.get('value')
            if 'forecolor' in record:
                colors['fore'] = record['forecolor']
            if 'backcolor' in record:
                colors['back'] = record['backcolor']
            if 'style' in record:
                colors['style'] = record['style']
        else:
            value = str(record)
        # Do name output.
        if name is not None:
            self.output_named(name, value, branch=branch, colors=colors)
            return
        # Do value output.
        if type(value) == list:
            for index in enumerate(value):
                if closed and index == len(value):
                    self.output(value[index], branch=self.hanging_branch,
                                colors=colors)
                elif index == 0:
                    self.output(value[index], branch=branch, colors=colors)
                    branch = self.pipe_branch
                else:
                    self.output(value[index], branch=branch, colors=colors)
        else:
            if closed:
                self.output(value, branch=self.hanging_branch, colors=colors)
            else:
                self.output(value, branch=branch, colors=colors)
        HierarchicalOutput.emit(self, record, closed)

    def output_indent(self):
        prefix = ''
        if self.level > 0:
            prefix = (self.pipe_branch + ' ') * (self.level)
        if prefix:
            sys.stdout.write(prefix)

    def output_named(self, name, value, branch, colors):
        self.output_indent()
        self.color_write('[ %s ]: %s' % (name, value), branch=branch,
                         colors=colors)

    def output(self, line, branch, colors):
        if not line:
            # Ignore color handling.
            return
        # Do padding on the left side according to level.
        prefix = ''
        if self.level > 0:
            prefix = self.pipe_branch * (self.level)
        sys.stdout.write(prefix)
        # Write level char: branch, hanging branch or a pipe.
        sys.stdout.write(branch)
        # Write value
        sys.stdout.write('%s\n' % line)
        # Flush
        sys.stdout.flush()


class AnsiOutput(AsciiOutput):

    def __init__(self):
        super(AsciiOutput, self).__init__()
        self.branch = u'├──'
        self.hanging_branch = u'└──'
        self.pipe_branch = u'│  '
        self.bracket_colors = {
            'fore': 'red',
            'style': 'bright',
        }
        self.branch_colors = {
            'fore': 'cyan',
            'style': 'bright',
        }
        colorama.init(autoreset=True)

    def bake_colors(self, colors):
        result = ''
        if 'fore' in colors:
            result += FOREMAP[colors['fore']]
        if 'back' in colors:
            result += BACKMAP[colors['back']]
        if 'style' in colors:
            result += STYLEMAP[colors['style']]
        return result

    def output_colors_reset(self):
        sys.stdout.write(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def output_indent(self):
        if self.level == 0:
            return
        sys.stdout.write(self.bake_colors(self.branch_colors))
        super(AnsiOutput, self).output_indent()
        self.output_colors_reset()

    def output_named(self, name, value, branch, colors):
        self.output_indent()
        sys.stdout.write(self.bake_colors(self.branch_colors) + self.branch
                         + u'─┐')
        self.output_colors_reset()
        line = self.bake_colors(self.bracket_colors) + '[ ' \
            + Fore.RESET + Back.RESET + Style.RESET_ALL \
            + self.bake_colors(colors) + name \
            + Fore.RESET + Back.RESET + Style.RESET_ALL \
            + self.bake_colors(self.bracket_colors) + ' ] ' \
            + Fore.RESET + Back.RESET + Style.RESET_ALL
        if value:
            line += u' ➜  ' + value
        sys.stdout.write(' ' + line + '\n')

    def output(self, line, branch, colors):
        if not line:
            # Just handle colors.
            sys.stdout.write(self.bake_colors(colors))
            return
        # Do padding on the left side according to level.
        self.output_indent()
        # Write level char: branch, hanging branch or a pipe.
        sys.stdout.write(self.bake_colors(self.branch_colors) + branch + ' ')
        self.output_colors_reset()
        # Write value
        sys.stdout.write(self.bake_colors(colors) + '%s\n' % line)
        self.output_colors_reset()
        # Flush
        sys.stdout.flush()

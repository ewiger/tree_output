# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import codecs
import unittest
from StringIO import StringIO
# We include <pkg_root>/src, <pkg_root>/lib/python
extend_path = lambda root_path, folder: sys.path.insert(
    0, os.path.join(root_path, folder))
ROOT = os.path.dirname(os.path.dirname(__file__))
extend_path(ROOT, '')
# import tree_output
from tree_output import HierarchicalOutput


EXPECTED_ANSI = os.path.join(os.path.dirname(__file__),
                             'mock', 'expected_ansi')


class TestHierarchicalOutput(unittest.TestCase):

    def test_json(self):
        # Emit output
        tree_output = HierarchicalOutput.factory('json')
        tree_output.emit('foo')
        tree_output.add_level()
        tree_output.emit('bar')

        tree_output.add_level()
        for num in range(10):
            tree_output.emit(num)
        tree_output.emit(10, closed=True)
        tree_output.remove_level()

        tree_output.emit('baz', closed=True)

        tree_output.remove_level()
        tree_output.emit('foo2')

        # Assertion:
        expected = '["bar", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "baz", "foo2"]'
        assert expected == str(tree_output)

    def test_ascii(self):
        # Capture STDOUT.
        output = StringIO()
        sys_output = sys.stdout
        sys.stdout = output

        # Do output
        tree_output = HierarchicalOutput.factory('ascii')
        tree_output.emit('foo')
        tree_output.add_level()
        tree_output.emit('bar')

        tree_output.add_level()
        for num in range(10):
            tree_output.emit(num)
        tree_output.emit(10, closed=True)
        tree_output.remove_level()

        tree_output.emit('baz', closed=True)

        tree_output.remove_level()
        tree_output.emit('foo2')

        # Assertion:
        expected = '''+-- foo
|   +-- bar
|   |   +-- 0
|   |   +-- 1
|   |   +-- 2
|   |   +-- 3
|   |   +-- 4
|   |   +-- 5
|   |   +-- 6
|   |   +-- 7
|   |   +-- 8
|   |   +-- 9
|   |   `-- 10
|   `-- baz
+-- foo2
'''
        sys.stdout = sys_output
        obtained = output.getvalue()
        # print(obtained)
        assert expected == obtained

    def test_ansi(self):
        # Call colorama.init() before STDOUT capture.
        tree_output = HierarchicalOutput.factory('ansi')
        import colorama
        # Comment this out in order to see output in colors.
        colorama.deinit()

        # Capture STDOUT.
        output = StringIO()
        sys_output = sys.stdout
        sys.stdout = output

        # Do output
        tree_output.emit({'name': 'bazar', 'value': 'foo'})
        tree_output.add_level()
        tree_output.emit('bar')

        tree_output.add_level()
        for num in range(10):
            tree_output.emit(num)
        tree_output.emit(10, closed=True)
        tree_output.remove_level()

        tree_output.emit('baz', closed=True)

        tree_output.remove_level()
        tree_output.emit('foo2')
        tree_output.emit('end', closed=True)

        # Assertion:
        expected = codecs.open(EXPECTED_ANSI, 'r', 'utf-8').read()
        sys.stdout = sys_output
        obtained = output.getvalue()
        # Write to mock
        # with codecs.open(EXPECTED_ANSI, 'w+', 'utf-8') as mock:
        #     mock.write(obtained)
        # print('\n' + obtained)
        assert expected == obtained

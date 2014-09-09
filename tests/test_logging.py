from __future__ import print_function
import os
import sys
import logging
import unittest
# We include <pkg_root>/src, <pkg_root>/lib/python
extend_path = lambda root_path, folder: sys.path.insert(
    0, os.path.join(root_path, folder))
ROOT = os.path.dirname(os.path.dirname(__file__))
extend_path(ROOT, '')
# import tree_output
from tree_output import HierarchicalOutput
from tree_output.log_handler import HierarchicalOutputHandler


class TestHierarchicalLogHandler(unittest.TestCase):

    def test_log_handling(self):
        # Line up.
        houtput = HierarchicalOutput.factory(format='json')
        #houtput = HierarchicalOutput.factory(format='ansi')
        handler = HierarchicalOutputHandler(houtput=houtput)
        logger = logging.getLogger('foo')
        logging.root.addHandler(handler)
        # Emission.
        logger.info('foo')
        logger.info('bar', extra={'add_hlevel': True})
        logger.info('foo2')
        logger.info('bar', extra={'add_hlevel': True})
        logger.info('foo2')
        # houtput.add_level()
        # for num in range(10):
        #     houtput.emit(num)
        # houtput.emit(10, closed=True)
        # houtput.remove_level()

        # houtput.emit('baz', closed=True)

        # houtput.remove_level()
        # houtput.emit('foo2')

        print(str(houtput))

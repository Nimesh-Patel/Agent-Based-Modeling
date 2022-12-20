# -*- coding: utf-8 -*-
import sys
import os.path
import unittest
import contextlib
import importlib


def classcase(name):
    return ''.join(x.capitalize() for x in name.replace('-', '_').split('_'))


class TestExamples(unittest.TestCase):
    '''
    Test examples models.  This creates a model object and iterates it through
    some steps.  The idea is to get code coverage, rather than to test the
    details of each example's model.
    '''

    EXAMPLES = os.path.abspath(os.path.join(os.path.dirname(__file__), '../examples'))

    @contextlib.contextmanager
    def active_example_dir(self, example):
        'save and restore sys.path and sys.modules'
        old_sys_path = sys.path[:]
        old_sys_modules = sys.modules.copy()
        old_cwd = os.getcwd()
        example_path = os.path.abspath(os.path.join(self.EXAMPLES, example))
        try:
            sys.path.insert(0, example_path)
            os.chdir(example_path)
            yield
        finally:
            os.chdir(old_cwd)
            added = [m for m in sys.modules.keys() if m not in old_sys_modules]
            for mod in added:
                del sys.modules[mod]
            sys.modules.update(old_sys_modules)
            sys.path[:] = old_sys_path

    def test_examples(self):
        for example in os.listdir(self.EXAMPLES):
            if not os.path.isdir(os.path.join(self.EXAMPLES, example)):
                continue
            if hasattr(self, 'test_{}'.format(example.replace('-', '_'))):
                # non-standard example; tested below
                continue

            print("testing example {!r}".format(example))
            with self.active_example_dir(example):
                try:
                    # model.py at the top level
                    mod = importlib.import_module('model'.format(example))
                except ImportError:
                    # <example>/model.py
                    mod = importlib.import_module('{}.model'.format(example.replace('-', '_')))
                Model = getattr(mod, classcase(example))
                model = Model()
                (model.step() for _ in range(100))

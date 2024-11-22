##############################################################################
#
# Copyright (c) 2004-2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Layer definitions
"""
import importlib
import sys
import unittest


class SetUpModuleLayer:
    """Layer for setUpModule / tearDownModule support"""

    def __init__(self, module):
        self.__name__ = f'{self.__class__.__name__} for {module.__name__}'
        self.__bases__ = (UnitTests,)
        self._module = module
        self._setup_raised = None
        if hasattr(self._module, 'setUpModule'):
            self.setUp = self._setUp
            self.verbosity = 1
        else:
            self.verbosity = sys.maxsize

    def _setUp(self):
        try:
            self._module.setUpModule()
        except unittest.SkipTest as e:
            # TODO not like that, mark the suite instances !!

            # if setUpModule raised a skip, we are supposed to skip the module. We don't
            # have a direct API for this, so we mark all TestCase from the
            # module as skipped.
            for test_case in vars(self._module).values():
                if isinstance(
                        test_case,
                        type) and issubclass(
                        test_case,
                        unittest.TestCase):
                    test_case.__unittest_skip__ = True
                    test_case.__unittest_skip_why__ = str(e)
        except BaseException as e:
            raise
        else:
            self.tearDown = self._tearDown

    def _tearDown(self):
        if hasattr(self._module, 'tearDownModule'):
            self._module.tearDownModule()


class SetUpClassLayer:
    """Layer for setUpClass / tearDownClass support"""

    def __init__(self, suite, bases):
        self.__name__ = f'{self.__class__.__name__} for {suite.__class__.__module__}.{suite.__class__.__name__}'
        self.__bases__ = bases
        self._cls = suite.__class__
        self._setup_raised = None
        if self._cls.setUpClass.__code__ is not unittest.TestCase.setUpClass.__code__:
            self.setUp = self._setUp
            self.verbosity = 1
        else:
            self.verbosity = sys.maxsize

    def _setUp(self):
        try:
            self._cls.setUpClass()
        except unittest.SkipTest as e:
            self._cls.__unittest_skip__ = True
            self._cls.__unittest_skip_why__ = str(e)
        except BaseException as e:
            raise
        else:
            if self._cls.tearDownClass.__code__ is not unittest.TestCase.tearDownClass.__code__:
                self.tearDown = self._tearDown

    def _tearDown(self):
        self._cls.tearDownClass()


class UnitTests:
    """A layer for gathering all unit tests."""

    @classmethod
    def from_suite(cls, suite):
        layer = cls
        bases = (layer)
        if isinstance(suite, unittest.TestCase):
            module = importlib.import_module(suite.__module__)
            if hasattr(
                    module,
                    'setUpModule') or hasattr(
                    module,
                    'tearDownModule'):
                layer = SetUpModuleLayer(module)
                bases = (layer, )
            if (
                suite.setUpClass.__code__ is not unittest.TestCase.setUpClass.__code__
                or suite.tearDownClass.__code__ is not unittest.TestCase.tearDownClass.__code__
            ):
                layer = SetUpClassLayer(suite, bases)

        return layer


class EmptyLayer:
    """An empty layer to start spreading out subprocesses."""

    __bases__ = ()
    __module__ = ''


def EmptySuite():
    suite = unittest.TestSuite()
    suite.layer = EmptyLayer()
    return suite

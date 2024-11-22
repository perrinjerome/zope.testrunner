##############################################################################
#
# Copyright (c) 2011 Zope Foundation and Contributors.
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

import unittest


def setUpModule():
    print(f'{__name__}.setUpModule')


def tearDownModule():
    print(f'{__name__}.tearDownModule')


class TestSetUpClass1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(f'{cls.__name__}.setUpClass')

    @classmethod
    def tearDownClass(cls):
        print(f'{cls.__name__}.tearDownClass')

    def test1(self):
        pass

    def test2(self):
        pass

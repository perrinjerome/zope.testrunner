testrunner handling of class and module fixtures
================================================

Class and module level fixture, as documented in https://docs.python.org/3/library/unittest.html#class-and-module-fixtures


    >>> import os, sys
    >>> directory_with_tests = os.path.join(this_directory, 'testrunner-ex-setupmodule')

    >>> from zope import testrunner

    >>> defaults = [
    ...     '--path', directory_with_tests,
    ...     '--tests-pattern', '^sample_setupmodule$',
    ...     ]


``setUpModule``, ``tearDownModule``, ``setupClass`` and ``tearDownClass`` are called:

    >>> sys.argv = 'test'.split()
    >>> testrunner.run_internal(defaults)
    ... # doctest: +ELLIPSIS
    Running zope.testrunner.layer.UnitTests tests:
      Set up zope.testrunner.layer.UnitTests in N.NNN seconds.
    <BLANKLINE>
      Ran 2 tests with 0 failures, 0 errors and 0 skipped in N.NNN seconds.
    Tearing down left over layers:
      Tear down zope.testrunner.layer.UnitTests in N.NNN seconds.
    False


If an exception is raised during a setUpClass then the tests in the class are not run and the tearDownClass is not run. Skipped classes will not have setUpClass or tearDownClass run. If the exception is a SkipTest exception then the class will be reported as having been skipped instead of as an error.




``addClassCleanup`` is not supported at the moment.

``addModuleCleanup`` is not supported at the moment.

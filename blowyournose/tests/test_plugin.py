from __future__ import print_function

import os
import unittest

import ddt
from lazy import lazy
import mock

from booger import Booger


class TestCaseWithSetupBoogers(unittest.TestCase):
    def setUp(self):
        self.thing = Booger("TestCaseWithSetupBoogers")

    def test_one(self):
        print("one")

    def test_two(self):
        print("two")


class MockedTestCaseMethod(unittest.TestCase):
    @mock.patch('os.listdir', mock.Mock())
    def test_with_mock(self):
        os.listdir(Booger("test_with_mock"))

    @mock.patch('os.listdir', mock.Mock())
    @mock.patch('os.getcwd', mock.Mock())
    @mock.patch('os.chdir', "Hey there")
    @mock.patch('os.getgid', mock.Mock())
    def test_with_many_mocks(self):
        os.listdir(Booger("test_with_many_mocks"))
        os.getcwd(Booger("test_with_many_mocks"))
        os.getgid(Booger("test_with_many_mocks"))
        self.assertEqual(os.chdir, "Hey there")


class MockedTestCaseMethodSubclass(MockedTestCaseMethod):
    pass


@mock.patch('os.listdir', mock.Mock())
class MockedTestCaseClass(unittest.TestCase):
    def test_first(self):
        os.listdir(Booger("MockedTestCaseClass", scope='class'))

    def test_second(self):
        os.listdir(Booger("MockedTestCaseClass", scope='class'))


@ddt.ddt
class DataTestCase1(unittest.TestCase):

    if 0:   # This isn't expected to work, because we don't need it to.
        @ddt.data(
            Booger("DataTestCase1", scope='class'),
            Booger("DataTestCase1", scope='class'),
        )
        def test_boogers(self, boog):
            self.assertIsInstance(boog, Booger)

    @ddt.data(
        (1, 2),
        (2, 4),
    )
    @mock.patch('os.listdir', mock.Mock())
    def test_double(self, ab):
        os.listdir(Booger("DataTestCase1", scope='class'))
        self.assertEqual(2*ab[0], ab[1])

@ddt.ddt
class DataTestCase2(unittest.TestCase):

    @mock.patch('os.listdir', mock.Mock())
    @ddt.data(
        (1, 3),
        (2, 6),
    )
    def test_triple(self, ab):
        os.listdir(Booger("DataTestCase2", scope='class'))
        self.assertEqual(3*ab[0], ab[1])


class LazyTestCase(unittest.TestCase):

    @lazy
    def boog(self):
        return Booger("LazyTestCase")

    def test_one(self):
        self.boog
        print("one")

    def test_two(self):
        self.boog
        print("two")

class TestCaseWithSetupClassBoogers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.thing = Booger("TestCaseWithSetupClassBoogers", scope='class')

    def test_one(self):
        print("one")

    def test_two(self):
        print("two")

import unittest

from composeit.compose import Compose

class Foo(object):

    def __init__(self, i):

        self.i = i

    def count(self):

        return self.i

    def incr(self):

        self.i += 1

class Bar(object):

    def close(self):
        pass

    @staticmethod
    def return_true():
        return True
        
@Compose(Foo, Bar)
class FooBar(object):

    def __init__(self, foo, bar):

        self.foo = foo
        self.bar = bar

@Compose(FooBar)
class Baz(object):

    def __init__(self, foobar):

        self.foobar = foobar

    def return_count(self):
        return self.count()

class TestComposedClass(unittest.TestCase):

    def setUp(self):

        self.foobar = FooBar(Foo(2), Bar())

    def test_layered(self):

        self.assertEqual(self.foobar.count(), Baz(self.foobar).count())

    def test_static_method(self):

        self.assertTrue(FooBar.return_true())
        
    def test_has_methods(self):

        self.assertTrue(hasattr(self.foobar, "count"))
        self.assertTrue(hasattr(self.foobar, "close"))

    def test_call_methods(self):

        self.assertEqual(None, self.foobar.incr())
        self.assertEqual(None, self.foobar.close())
        self.assertEqual(3, self.foobar.count())
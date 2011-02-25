import inspect
import unittest

from bpython import inspection

class TestInspection(unittest.TestCase):
    def test_is_callable(self):
        class OldCallable:
            def __call__(self):
                pass

        class Callable(object):
            def __call__(self):
                pass

        class OldNoncallable:
            pass

        class Noncallable(object):
            pass

        def spam():
            pass

        self.assertTrue(inspection.is_callable(spam))
        self.assertTrue(inspection.is_callable(Callable))
        self.assertTrue(inspection.is_callable(Callable()))
        self.assertTrue(inspection.is_callable(OldCallable))
        self.assertTrue(inspection.is_callable(OldCallable()))
        self.assertFalse(inspection.is_callable(Noncallable()))
        self.assertFalse(inspection.is_callable(OldNoncallable()))
        self.assertFalse(inspection.is_callable(None))

    def test_parsekeywordpairs(self):
        def fails(spam=['-a', '-b']):
            pass

        default_arg_repr = "['-a', '-b']"
        self.assertEqual(str(['-a', '-b']), default_arg_repr,
                         'This test is broken (repr does not match), fix me.')

        argspec = inspection.getargspec('fails', fails)
        defaults = argspec[1][3]
        self.assertEqual(str(defaults[0]), default_arg_repr)

    def test_fixlongargs(self):
        def spam(a, b=1, c="y\xc3\xa4y"):
            pass

        argspec = list(inspect.getargspec(spam))
        print argspec[3],
        inspection.fixlongargs(spam, argspec)
        print argspec[3], [type(a) for a in argspec[3]]
        self.assertFalse(argspec)

if __name__ == '__main__':
    unittest.main()

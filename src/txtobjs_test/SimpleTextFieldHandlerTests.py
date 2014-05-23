
import unittest

from txtobjs.schema.SimpleTextField import SimpleTextField


class SimpleTextFieldHandlerTests(unittest.TestCase):


    def testCaseInsensitiveTextFieldNameMatches(self):
        field = SimpleTextField('FirstName')
        self.assertTrue(field.matches_text_name('FirstName'))
        self.assertTrue(field.matches_text_name('firstname'))
        self.assertFalse(field.matches_text_name('LastName'))


    def testCaseSensitiveTextFieldNameMatches(self):
        field = SimpleTextField('FirstName').case_sesitive()
        self.assertTrue(field.matches_text_name('FirstName'))
        self.assertFalse(field.matches_text_name('firstname'))
        self.assertFalse(field.matches_text_name('LastName'))


    def testTextFieldNameWithSpaceMatches(self):
        field = SimpleTextField('First Name')
        self.assertTrue(field.matches_text_name('First Name'))
        self.assertTrue(field.matches_text_name('first name'))
        self.assertFalse(field.matches_text_name('Last Name'))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
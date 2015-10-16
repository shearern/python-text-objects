'''
Created on May 8, 2014

@author: nshearer
'''
import unittest
import yaml
import datetime
import os

class ParseProjectYamlTests(unittest.TestCase):
    '''Make sure our sample YAML file parses as we expect'''

    SOURCE_FILE = os.path.join(os.path.dirname(__file__),
                               '..', '..', 'test_data',
                               'project.yml')

    EXPECTED = {
        'Project': {
            'Type':     'Project',
            'Title':    "ePAF Notification",
            'Started':  datetime.date(2014, 5, 1),
            'Hidden':   None,
            'Active':   True,
            'Predecessors': [
                'Project A',
                'Project B',
                ],
            'Id': "epaf_notify",
            'Tasks': {
                'design': {
                    'Title':    "Design Solution",
                    },
                'develop': {
                    'Title':    "Develop Solution",
                    'pred': [
                        'design',
                        ]
                    },
                'test': {
                    'Title':    "Test Code",
                    'pred': [
                        'develop',
                        'design',
                        ]
                      },
            },
        },
    }

    def _parseYaml(self):
        with open(self.SOURCE_FILE, 'rt') as fh:
            return yaml.load(fh)


    def testYamlParses(self):
        self._parseYaml()


    def testProjectTypeKey(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Type'],
                         parsed['Project']['Type'])


    def testProjectActiveKey(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Active'],
                         parsed['Project']['Active'])


    def testProjectTitleKey(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Title'],
                         parsed['Project']['Title'])


    def testProjectStartedKey(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Started'],
                         parsed['Project']['Started'])


    def testProjectHiddenKey(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Hidden'],
                         parsed['Project']['Hidden'])


    def testProjectIdKey(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Id'],
                         parsed['Project']['Id'])


    def testProjectPredecessorsKey(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Predecessors'],
                         parsed['Project']['Predecessors'])


    def testProjectTaskNames(self):
        parsed = self._parseYaml()
        self.assertEqual(set(['design', 'develop', 'test']),
                         set(parsed['Project']['Tasks'].keys()))


    def testTaskTestEquals(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Tasks']['test'],
                         parsed['Project']['Tasks']['test'])


    def testTaskDevelopEquals(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Tasks']['develop'],
                         parsed['Project']['Tasks']['develop'])


    def testTaskDesignEquals(self):
        parsed = self._parseYaml()
        self.assertEqual(self.EXPECTED['Project']['Tasks']['design'],
                         parsed['Project']['Tasks']['design'])


    def testProjectEquals(self):
        self.assertEqual(self._parseYaml(), self.EXPECTED)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
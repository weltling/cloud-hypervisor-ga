import unittest
import argparse
import qmp_formatter
import json


class TestParserMethods(unittest.TestCase):

    def test_no_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        namespace = parser.parse_args(['guest-sync'])
        result = qmp_formatter.to_qmp(namespace)
        predicted = {"execute": "guest-sync"}
        self.assertDictEqual(json.loads(result), predicted)

    def test_one_arg(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        parser.add_argument('--id')
        namespace = parser.parse_args(['guest-sync', '--id', '3'])
        result = qmp_formatter.to_qmp(namespace)
        predicted = {"execute": "guest-sync", 'arguments': {'id': '3'}}
        self.assertDictEqual(json.loads(result), predicted)

    def test_many_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        parser.add_argument('--ab')
        parser.add_argument('--cd')
        parser.add_argument('--ef')
        parser.add_argument('--gh')
        namespace = parser.parse_args(['guest-sync',
                                       '--ab', '3',
                                       '--cd', '4',
                                       '--ef', '5',
                                       '--gh', '6'])
        result = qmp_formatter.to_qmp(namespace)
        predicted = {"execute": "guest-sync", 'arguments': {'ab': '3',
                                                            'cd': '4',
                                                            'ef': '5',
                                                            'gh': '6'}}
        self.assertDictEqual(json.loads(result), predicted)

    def test_not_all(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        parser.add_argument('--ab')
        parser.add_argument('--cd')
        parser.add_argument('--ef')
        parser.add_argument('--gh')
        namespace = parser.parse_args(['guest-sync',
                                       '--ab', '3',
                                       '--ef', '5',
                                       '--gh', '6'])
        result = qmp_formatter.to_qmp(namespace)
        predicted = {"execute": "guest-sync", 'arguments': {'ab': '3',
                                                            'ef': '5',
                                                            'gh': '6'}}
        self.assertDictEqual(json.loads(result), predicted)


if __name__ == '__main__':
    unittest.main()

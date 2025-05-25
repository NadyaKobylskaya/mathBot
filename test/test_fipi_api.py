import unittest
from fipi_api import get_tasks

class TestFipiAPI(unittest.TestCase):
    def test_get_tasks(self):
        tasks = get_tasks()
        self.assertTrue(isinstance(tasks, list) or tasks is None)

if __name__ == '__main__':
    unittest.main()

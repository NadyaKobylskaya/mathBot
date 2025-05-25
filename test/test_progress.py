import unittest
from progress_tracker import save_progress, get_progress
from models import Base, UserProgress
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestProgressTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Используем SQLite в памяти
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_save_and_get_progress(self):
        save_progress(user_id=1, task_id=1, is_completed=True, score=90)
        progress = get_progress(user_id=1, task_id=1)
        self.assertIsNotNone(progress)
        self.assertEqual(progress.score, 90)
        self.assertTrue(progress.is_completed)

if __name__ == '__main__':
    unittest.main()

import importlib.util
import os
import tempfile
import unittest


def load_app(db_path):
    os.environ["MERGINGTON_DB_PATH"] = db_path
    module_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "src", "app.py"
    )
    spec = importlib.util.spec_from_file_location("mergington_app", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AppPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tempdir.name, "activities.db")
        self.module = load_app(self.db_path)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_signup_persists_across_reload(self):
        email = "new.student@mergington.edu"

        response = self.module.signup_for_activity("Chess Club", email)

        self.assertEqual(response["message"], f"Signed up {email} for Chess Club")

        reloaded = load_app(self.db_path)
        activities = reloaded.get_activities()

        self.assertIn(email, activities["Chess Club"]["participants"])


if __name__ == "__main__":
    unittest.main()

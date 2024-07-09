import unittest
import os
import shutil
from pyvcs.core import (
    read_file, write_file, calculate_hash, is_directory,
    list_files, VersionControl
)

class TestPyVCS(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_repo'
        os.makedirs(self.test_dir, exist_ok=True)
        self.file_path = os.path.join(self.test_dir, 'test_file.txt')
        self.content = b"Hello, PyVCS!"
        write_file(self.file_path, self.content)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_read_file(self):
        content = read_file(self.file_path)
        self.assertEqual(content, self.content)

    def test_write_file(self):
        new_content = b"Hello, World!"
        write_file(self.file_path, new_content)
        content = read_file(self.file_path)
        self.assertEqual(content, new_content)

    def test_calculate_hash(self):
        expected_hash = calculate_hash(self.content)
        actual_hash = calculate_hash(self.content)
        self.assertEqual(expected_hash, actual_hash)

    def test_is_directory(self):
        self.assertTrue(is_directory(self.test_dir))
        self.assertFalse(is_directory(self.file_path))

    def test_list_files(self):
        files = list(list_files(self.test_dir))
        self.assertIn(self.file_path, files)

    def test_version_control_init(self):
        success, message = VersionControl.init(self.test_dir)
        self.assertTrue(success)
        self.assertIn('.pyvcs', os.listdir(self.test_dir))

    def test_add_file(self):
        VersionControl.init(self.test_dir)
        vc = VersionControl(self.test_dir)
        hash_value = vc.add(self.file_path)
        expected_hash = calculate_hash(self.content)
        self.assertEqual(hash_value, expected_hash)

    def test_commit(self):
        VersionControl.init(self.test_dir)
        vc = VersionControl(self.test_dir)
        vc.add(self.file_path)
        commit_message = "Initial commit"
        commit_hash = vc.commit(commit_message)
        self.assertIsNotNone(commit_hash)
        head_path = os.path.join(vc.refs_dir, 'HEAD')
        self.assertTrue(os.path.exists(head_path))

    def test_diff_no_changes(self):
        VersionControl.init(self.test_dir)
        vc = VersionControl(self.test_dir)
        vc.add(self.file_path)
        vc.commit("Initial commit")
        diff_result = vc.diff(self.file_path)
        self.assertEqual(diff_result, "No changes detected.")

    def test_diff_with_changes(self):
        VersionControl.init(self.test_dir)
        vc = VersionControl(self.test_dir)
        vc.add(self.file_path)
        vc.commit("Initial commit")
        with open(self.file_path, 'wb') as f:
            f.write(b"Modified content")
        diff_result = vc.diff(self.file_path)
        self.assertIn("Changes detected", diff_result)

if __name__ == '__main__':
    unittest.main()

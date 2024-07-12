import os
import hashlib
import json
from datetime import datetime

def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, 'wb') as f:
        f.write(content)

def calculate_hash(content):
    return hashlib.sha256(content).hexdigest()

def is_directory(path):
    return os.path.isdir(path)

def list_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)
            
class VersionControl:
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.pyvcs_dir = os.path.join(self.root_dir, '.pyvcs')
        self.objects_dir = os.path.join(self.pyvcs_dir, 'objects')
        self.refs_dir = os.path.join(self.pyvcs_dir, 'refs')


    @classmethod
    def init(cls, root_dir , directory_name = None):
        root_dir = cls._create_repo_directory(root_dir, directory_name)
        vc = cls(root_dir)
        if not os.path.exists(vc.pyvcs_dir):
            cls._create_pyvcs_structure(vc.pyvcs_dir, vc.objects_dir, vc.refs_dir)
            return True, f"Initialized empty PyVCS repository in {vc.pyvcs_dir}"
        return False, "PyVCS directory already initialized."


    @staticmethod
    def _create_repo_directory(root_dir, directory_name):
        if directory_name:
            new_dir = os.path.join(root_dir, directory_name)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            root_dir = new_dir
        return root_dir


    @staticmethod
    def _create_pyvcs_structure(pyvcs_dir, objects_dir, refs_dir):
        os.makedirs(pyvcs_dir, exist_ok=True)
        os.makedirs(objects_dir, exist_ok=True)
        os.makedirs(refs_dir, exist_ok=True)


    def add(self, file_path):
        content = read_file(file_path)
        hash_value = calculate_hash(content)
        object_path = os.path.join(self.objects_dir, hash_value)
        write_file(object_path, content)
        self._update_index(file_path, hash_value)
        return hash_value
    
    
    def _update_index(self, file_path, hash_value):
        index_path = os.path.join(self.pyvcs_dir, 'index')
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                index = json.load(f)
        else:
            index = {}
        index[os.path.relpath(file_path, self.root_dir)] = hash_value
        with open(index_path, 'w') as f:
            json.dump(index, f)
    

    def commit(self, message):
        commit_obj = self._create_commit_object(message)
        commit_hash = self._write_commit_object(commit_obj)
        self._update_head(commit_hash)
        return commit_hash


    def _create_commit_object(self, message):
        commit_obj = {
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'files': self._get_staged_files()
        }
        return commit_obj


    def _get_staged_files(self):
        index_path = os.path.join(self.pyvcs_dir, 'index')
        with open(index_path, 'r') as f:
            return json.load(f)
    
    
    def _write_commit_object(self, commit_obj):
        commit_content = json.dumps(commit_obj).encode()
        commit_hash = calculate_hash(commit_content)
        commit_path = os.path.join(self.objects_dir, commit_hash)
        write_file(commit_path, commit_content)
        return commit_hash


    def _update_head(self, commit_hash):
        head_path = os.path.join(self.refs_dir, 'HEAD')
        write_file(head_path, commit_hash.encode())


    def diff(self, file_path):
        current_content = read_file(file_path)
        current_hash = calculate_hash(current_content)

        head_path = os.path.join(self.refs_dir, 'HEAD')
        if not os.path.exists(head_path):
            return "No previous commit found."

        head_commit_hash = read_file(head_path).decode().strip()
        head_commit_path = os.path.join(self.objects_dir, head_commit_hash)
        head_commit_content = read_file(head_commit_path)
        head_commit_obj = json.loads(head_commit_content.decode())

        relative_path = os.path.relpath(file_path, self.root_dir)
        if relative_path not in head_commit_obj['files']:
            return "File not found in the previous commit."

        previous_hash = head_commit_obj['files'][relative_path]
        if current_hash == previous_hash:
            return "No changes detected."

        previous_content = read_file(os.path.join(self.objects_dir, previous_hash))
        return f"Changes detected. Previous hash: {previous_hash}, Current hash: {current_hash}"
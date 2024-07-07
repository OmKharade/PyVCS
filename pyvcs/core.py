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
        self.root_dir = root_dir
        self.pv_dir = os.path.join(root_dir, '.pyvcs')
        self.objects_dir = os.path.join(self.pv_dir, 'objects')
        self.refs_dir = os.path.join(self.pv_dir, 'refs')
        self.init()

    def init(self):
        os.makedirs(self.pv_dir, exist_ok=True)
        os.makedirs(self.objects_dir, exist_ok=True)
        os.makedirs(self.refs_dir, exist_ok=True)

    def add(self, file_path):
        content = read_file(file_path)
        hash_value = calculate_hash(content)
        object_path = os.path.join(self.objects_dir, hash_value)
        write_file(object_path, content)
        return hash_value

    def commit(self, message):
        commit_obj = {
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'files': {}
        }

        for file_path in list_files(self.root_dir):
            if not file_path.startswith(self.pv_dir):
                relative_path = os.path.relpath(file_path, self.root_dir)
                hash_value = self.add(file_path)
                commit_obj['files'][relative_path] = hash_value

        commit_content = json.dumps(commit_obj).encode()
        commit_hash = calculate_hash(commit_content)
        commit_path = os.path.join(self.objects_dir, commit_hash)
        write_file(commit_path, commit_content)

        head_path = os.path.join(self.refs_dir, 'HEAD')
        write_file(head_path, commit_hash.encode())

        return commit_hash

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
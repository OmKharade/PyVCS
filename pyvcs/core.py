import os
import hashlib
import json
from datetime import datetime
import difflib

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
        parent_hash = self._get_head_commit()
        commit_obj = self._create_commit_object(message, parent_hash)
        commit_hash = self._write_commit_object(commit_obj)
        self._update_head(commit_hash)
        return commit_hash


    def _create_commit_object(self, message, parent_hash):
        commit_obj = {
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'files': self._get_staged_files(),
            'parent': parent_hash,
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


    def status(self):
        staged_files = self._get_staged_files()
        changed_files = self._get_changed_files(staged_files)
        return staged_files, changed_files  
    
    def _get_changed_files(self, staged_files):
        changed_files = {}
        for file_path in list_files(self.root_dir):
            rel_path = os.path.relpath(file_path, self.root_dir)
            if rel_path.startswith('.pyvcs'):
                continue
            if rel_path not in staged_files:
                changed_files[rel_path] = 'Untracked'
            else:
                content = read_file(file_path)
                hash_value = calculate_hash(content)
                if hash_value != staged_files[rel_path]:
                    changed_files[rel_path] = 'Modified'
        return changed_files


    def log(self):
        commit_hash = self._get_head_commit()
        while commit_hash:
            commit_obj = self._read_commit_object(commit_hash)
            yield commit_hash, commit_obj
            commit_hash = commit_obj.get('parent')
            
    
    def _get_head_commit(self):
        head_path = os.path.join(self.refs_dir, 'HEAD')
        if os.path.exists(head_path):
            return read_file(head_path).decode().strip()
        return None

    def _read_commit_object(self, commit_hash):
        commit_path = os.path.join(self.objects_dir, commit_hash)
        commit_content = read_file(commit_path)
        return json.loads(commit_content.decode())


    def diff(self, file_path):
        last_commit_content = self._get_last_commit_file_content(file_path)
        if last_commit_content is None:
            return f"No previous commit for file {file_path}"
        current_content = read_file(file_path).decode().splitlines(keepends=True)
        last_commit_content = last_commit_content.decode().splitlines(keepends=True)
        diff_result = difflib.unified_diff(
            last_commit_content,
            current_content,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm=''
        )
        return '\n'.join(diff_result)

        
    def _get_last_commit_file_content(self, file_path):
        commit_hash = self._get_head_commit()
        if not commit_hash:
            return None
        commit_obj = self._read_commit_object(commit_hash)
        staged_files = commit_obj.get('files', {})
        rel_path = os.path.relpath(file_path, self.root_dir)
        if rel_path in staged_files:
            file_hash = staged_files[rel_path]
            object_path = os.path.join(self.objects_dir, file_hash)
            return read_file(object_path)
        return None
import argparse
from pyvcs.core import VersionControl
import os

def main():
    parser = argparse.ArgumentParser(description="PyVCS: A simple version control system")
    subparsers = parser.add_subparsers(dest='command')
    
    subparsers.add_parser('init').add_argument('directory', nargs='?', default=os.getcwd())
    subparsers.add_parser('add').add_argument('file')
    subparsers.add_parser('commit').add_argument('message')
    subparsers.add_parser('status')
    subparsers.add_parser('log')
    subparsers.add_parser('diff').add_argument('file')
    
    args = parser.parse_args()
    execute_command(args)
    
def execute_command(args):
    vc = VersionControl(os.getcwd())
    command = args.command

    if command == 'init':
        success, message = VersionControl.init(os.getcwd(), args.directory)
        print(message)

    elif command == 'add':
        hash_value = vc.add(args.file)
        print(f"Added file {args.file} with hash {hash_value}")

    elif command == 'commit':
        commit_hash = vc.commit(args.message)
        print(f"Created commit with hash {commit_hash}")

    elif command == 'status':
        staged_files, changed_files = vc.status()
        print("Staged files:")
        for file, hash_value in staged_files.items():
            print(f"{file}: {hash_value}")
        print("\nChanged files:")
        for file, status in changed_files.items():
            print(f"{file}: {status}")

    elif command == 'log':
        for commit_hash, commit_obj in vc.log():
            print(f"Commit: {commit_hash}")
            print(f"Message: {commit_obj['message']}")
            print(f"Timestamp: {commit_obj['timestamp']}")
            print("Files:")
            for file, hash_value in commit_obj['files'].items():
                print(f"{file}: {hash_value}")
            print()

    elif command == 'diff':
        diff_result = vc.diff(args.file)
        print(diff_result)

if __name__ == "__main__":
    main()
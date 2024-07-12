import argparse
from pyvcs.core import VersionControl
import os

def main():
    parser = argparse.ArgumentParser(description="PyVCS: A simple version control system")
    parser.add_argument('command', choices=['init', 'add', 'commit', 'diff', 'status', 'log'])
    parser.add_argument('args', nargs='*', help='Additional arguments')

    args = parser.parse_args()

    if args.command == 'init':
        directory_name = args.args[0] if args.args else None
        success, message = VersionControl.init(os.getcwd(), directory_name)
        print(message)
        if success:
            print("You can now begin version controlling your project!")\
            
    else:
        vc = VersionControl(os.getcwd())
        if args.command == 'add':
            if not args.args:
                print("Error: Please specify a file to add")
                return
            hash_value = vc.add(args.args[0])
            print(f"Added file {args.args[0]} with hash {hash_value}")

        elif args.command == 'commit':
            if not args.args:
                print("Error: Please provide a commit message")
                return
            commit_hash = vc.commit(args.args[0])
            print(f"Created commit with hash {commit_hash}")

        elif args.command == 'diff':
            if not args.args:
                print("Error: Please specify a file to diff")
                return
            diff_result = vc.diff(args.args[0])
            print(diff_result)
            
        elif args.command == 'status':
            staged_files, changed_files = vc.status()
            print("Staged files: ")
            for file, hash_value in staged_files.items():
                print(f"{file}: {hash_value}")
            print("\nChanged files: ")
            for file, status in changed_files.items():
                print(f"{file}: {status}")
                
        elif args.command == 'log':
            for commit_hash, commit_obj in vc.log():
                print(f"Commit: {commit_hash}")
                print(f"Message: {commit_obj['message']}")
                print(f"Timestamp: {commit_obj['timestamp']}")
                print("Files:")
                for file, hash_value in commit_obj['files'].items():
                    print(f"{file}: {hash_value}")
                print()

if __name__ == "__main__":
    main()
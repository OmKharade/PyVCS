import argparse
from pyvcs.core import VersionControl

def main():
    parser = argparse.ArgumentParser(description="PyVCS: A simple version control system")
    parser.add_argument('command', choices=['init', 'add', 'commit', 'diff'])
    parser.add_argument('args', nargs='*', help='Additional arguments')

    args = parser.parse_args()

    vc = VersionControl('.')

    if args.command == 'init':
        vc.init()
        print("Initialized PyVCS repository")

    elif args.command == 'add':
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

if __name__ == "__main__":
    main()
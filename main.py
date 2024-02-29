import os
import subprocess

from dotenv import load_dotenv

# Prerequisites
# sudo apt install python3-dotenv
# sudo apt install python3-dotenv-cli

# Create .env file
# BAT=/usr/local/bin/bat (or path to cat command)
# PATTERNS=comma,separated,string,of,patterns,indicating,duplicates
# CONFLICT= blank for no, yes or anything to use.
# OBSIDIANVAULT="/path/to/obsidian/vault/Obsidian Notes"

_CMD_FIND = "/usr/bin/find"
_CMD_DIFF = "/usr/bin/diff"


def get_patterns(pattern_line):
    # Patterns as array
    if ',' in pattern_line:
        return pattern_line.split(',')
    else:
        return [pattern_line]


def get_confict(conflict_line):
    if conflict_line == "" or conflict_line == None:
        return False
    else:
        return True


def find_files(command):
    output = subprocess.check_output(command)
    # Output i binary format. Convert it and split by lines
    return output.decode('utf8').splitlines()


def get_find_command(path="", patterns=[], conflict=False):
    first_line = True
    command = ["find", path]
    for pattern in patterns:
        if not first_line:
            command.append("-o")
        else:
            first_line = False
        command.append("-name")
        command.append("*" + pattern + "*.md")
    if conflict:
        command.append("-o")
        command.append("-name")
        command.append("*(conflict*).md")
    return command


def get_diff(base_file, file):
    diff_command = [_CMD_DIFF, "--normal", base_file, file]
    result = subprocess.run(diff_command, capture_output=True, text=True)
    if result.returncode == 0:
        return ""
    else:
        return result.stdout


def get_base_file(file_name, patterns):
    for pattern in patterns:
        if pattern in file_name:
            return file_name.replace(pattern, ".md")
    return ""


if __name__ == '__main__':
    # @TODO config i ~/.config/obsidianbackups/.env
    # load_dotenv(dotenv_path=dotenv_path)
    # dotenv_path = Path('~/Projects/obsidianbackups/.env')

    load_dotenv()
    bat_command = os.getenv("BAT")
    patterns = get_patterns(os.getenv("PATTERNS"))
    conflict = get_confict(os.getenv("CONFLICT"))
    obsidian_vault_path = os.getenv("OBSIDIANVAULT")

    command = get_find_command(obsidian_vault_path, patterns, conflict)

    files = find_files(command)

    if len(files) == 0:
        print("No diffs found")
        exit(0)

    prev_base_file = ""
    current_base_file = get_base_file(files[0], patterns)
    printed_file = False
    unchanged_files = []
    for file in files:
        base_file = get_base_file(file, patterns)
        diff = get_diff(base_file, file)
        if len(diff) > 0:
            if not printed_file:
                command = [bat_command, base_file]
                subprocess.run(command)
                printed_file = True
            command = [bat_command, file]
            subprocess.run(command)
            print("Over-write original with:")
            print("mv \"" + base_file + "\" \"" + file + "\"")
            print("Or delete this file with:")
            print("rm \"" + file + "\"\n")
        else:
            unchanged_files.append(file)
        prev_base_file = base_file

    print("No diff for the following files. Delete them with: ")
    for file in unchanged_files:
        print("rm \"" + file + "\"")
    val = input("Enter \"rm\" to delete those files: ")
    if "rm" == val:
        for file in unchanged_files:
            command = ["rm", file]
            subprocess.run(command)
            print("Deleted \"" + file + "\"")

import os
from modules.files import copy_files as file


def main():
    # reset directory
    public_dir = os.path.curdir + "/public/"
    static_dir = os.path.curdir + "/static/"
    file.clear_directory(public_dir)
    file.copy_files(static_dir, public_dir)


if __name__ == "__main__":
    main()

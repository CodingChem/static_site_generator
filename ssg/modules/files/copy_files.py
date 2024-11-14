import os
from os.path import isfile
import shutil


def clear_directory(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def copy_files(origin: str, target: str):
    if not os.path.exists(target):
        os.mkdir(target)
    for entries in os.listdir(origin):
        if os.path.isfile(origin + entries):
            shutil.copy(origin + entries, target + entries)
        else:
            copy_files(origin + entries, target + entries)


if __name__ == "__main__":
    clear_directory("/home/vegard/proj/static_site_generator/ssg/public/")
    copy_files(
        "/home/vegard/proj/static_site_generator/ssg/static/",
        "/home/vegard/proj/static_site_generator/ssg/public/",
    )

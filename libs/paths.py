"""
文件管理
"""
import os


def search_file(word="", path="./", root_dir_only=True):
    if root_dir_only:
        ls = os.listdir(path)

    else:
        ls = [f"{_dir}/{_file}" for _dir, _dir_list, _file_list in os.walk(path) for _file in _file_list]

    return [name for name in ls if all([
        os.path.isfile(name),
        word in name
    ])]

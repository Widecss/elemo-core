# coding: utf-8
# author: Widecss
import importlib
import inspect
import os


def _walk_package(package: str, files: list):
    modules = []
    for file in files:
        module_name = file.split(".")[0]
        path_to = package.replace("\\", ".")
        modules += [f"{path_to}.{module_name}"]
    return modules


def _get_class_from(module):
    class_list = []
    for _, cls in inspect.getmembers(module, inspect.isclass):
        class_list.append(cls)
    return class_list


def _get_subclass_from(class_list, super_class):
    subclass_list = []
    for cls in filter(lambda obj: issubclass(obj, super_class), class_list):
        subclass_list.append(cls)
    return subclass_list


def get_subclasses_from(package_dir: str, super_class: type):
    """
    从指定文件夹下加载所有包，并获取其中所有指定类的子类
    :param package_dir: 指定文件夹
    :param super_class: 指定类
    :return: 子类列表
    """
    module_paths = []
    for _path, _, files in os.walk(package_dir):
        if "\\_" in _path:
            # 过滤根目录下有下划线的文件夹
            continue
        if _path == os.path.split(package_dir)[1]:
            # 过滤根目录
            continue
        module_paths += _walk_package(_path, files)

    sub_class_list = []
    for module_path in module_paths:
        module = importlib.import_module(module_path)
        class_list = _get_class_from(module)
        sub_class_list += _get_subclass_from(class_list, super_class)

    return sub_class_list

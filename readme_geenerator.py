"""
Python script to generate readme file compiling all the supported scripts within the current directory.
"""

import os
from datetime import datetime

HEADER= """# Utilities
The repository contains different reusable utility functions in different programming languages to avoid rewriting the
boilerplate codes to perform the same task repeatedly.

"""

FOOTER = """

This version of README was generated at **{}**
""".format(datetime.now().strftime("%d %b %Y %H:%M"))

def get_help_docs(script_path):
    docs = ""
    with open(script_path, "r") as f:
        if f.readline().startswith('"""'):
            while not (line := f.readline()).startswith('"""'):
                docs += line

    return docs.strip()


def traverse_recursively(root, docs=None, paths=None):
    if docs is None:
        docs = {}
    if paths is None:
        paths = ["./"]
    for dir_ in os.listdir(root):
        if dir_.startswith("."):
            continue
        full_path = os.path.join(root, dir_)
        if os.path.isdir(full_path):
            traverse_recursively(full_path, docs, paths + [dir_])
        else:
            file_name, extension = os.path.splitext(os.path.split(full_path)[-1])
            if extension.upper() != '.PY':
                continue
            if file_name.startswith("__") or file_name.endswith("__"):
                continue
            docs_str = get_help_docs(full_path)
            docs_ = docs
            for path in paths[:-1]:
                docs_.setdefault(path, {"child_": {}})
                docs_ = docs_[path]["child_"]
            else:
                docs_.setdefault(paths[-1], {"child_":  {}})
                docs_ = docs_[paths[-1]]
            docs_.update({dir_: docs_str})
    return docs


def create_markdown_from_nested_dictionary(dictionary, md="", level=0):
    child = dictionary.pop("child_", {})
    for key, value in dictionary.items():
        if isinstance(value, dict):
            return  create_markdown_from_nested_dictionary(value, md + "  " * level + f"- `{key}`:\n", level+1)
        else:
            md += "  "*(level+1) + f"- `{key}`: {value}\n"

    if child:
        return create_markdown_from_nested_dictionary(child, md, level+1)
    return md


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    docs_md = create_markdown_from_nested_dictionary(traverse_recursively(current_dir))
    with open("README.md", "w") as f:
        f.write(HEADER)
        f.write(docs_md)
        f.write(FOOTER)
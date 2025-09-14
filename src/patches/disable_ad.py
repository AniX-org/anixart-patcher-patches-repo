"""Disable ad banners"""
# Developer: Radiquum

# imports
import os
from config import config, log
from scripts.smali_parser import (
    find_smali_method_end,
    find_smali_method_start,
    get_smali_lines,
    replace_smali_method_body,
)
from scripts.patch_funcs import PatchGlobals


# Patch
replace = """    .locals 0

    const/4 p0, 0x1

    return p0
"""


def apply(settings: None, globals: PatchGlobals) -> bool:
    path = f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd/Prefs.smali"
    lines = get_smali_lines(path)

    if not os.path.exists(path):
        log.error(f"File {path} not found")
        return False

    for index, line in enumerate(lines):
        if line.find("IS_SPONSOR") >= 0:
            method_start = find_smali_method_start(lines, index)
            method_end = find_smali_method_end(lines, index)
            new_content = replace_smali_method_body(
                lines, method_start, method_end, replace
            )
            with open(path, "w", encoding="utf-8") as file:
                file.writelines(new_content)

    return True

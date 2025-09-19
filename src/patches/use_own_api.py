"""Патч заменяет ссылки API на свои"""

# Title: Использовать кастомный API
# Author: Radiquum, seele
# Readme URL:

# imports
import os
from typing import TypedDict
from config import config, log
from scripts.patch_funcs import PatchGlobals
from scripts.smali_parser import (
    get_smali_lines,
    save_smali_lines,
    find_and_replace_smali_line,
)


# Patch
class ValueApiReplaceItem(TypedDict):
    file: str
    values: list[str]


class SmaliLineReplaceItem(TypedDict):
    file: str
    from_: str
    to_: str


class PatchConfig_UseOwnApi(TypedDict):
    api_base: str
    api_dir: str
    api_append_base: list[ValueApiReplaceItem]
    api_replace_line: list[SmaliLineReplaceItem]


def apply(settings: PatchConfig_UseOwnApi, globals: PatchGlobals) -> bool:
    for append in settings["api_append_base"]:
        if not settings['api_base']: continue
        if settings['api_base'].endswith('/'): settings['api_base'] = settings['api_base'][:-1]
        file_path = f"{config['folders']['decompiled']}/{settings['api_dir']}/{append['file']}"
        lines = get_smali_lines(file_path)
        for value in append["values"]:
            find_and_replace_smali_line(lines, f'value = "{value}"', f'value = "{settings["api_base"]}/{value}"')
        save_smali_lines(file_path, lines)
        log.debug(f"[FORCE_STATIC_REQUEST_URLS] file {file_path} has been modified")

    for replace in settings['api_replace_line']:
        if not replace['file'] or not replace['from'] or not replace['to']: continue
        file_path = f"{config['folders']['decompiled']}/{settings['api_dir']}/{replace['file']}"
        lines = get_smali_lines(file_path)
        find_and_replace_smali_line(get_smali_lines(file_path), replace['from'], replace['to'])
        save_smali_lines(file_path, lines)
        log.debug(f"[FORCE_STATIC_REQUEST_URLS] file {file_path} has been modified")

    hiltCIMpl_file_path = f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd/DaggerApp_HiltComponents_SingletonC$SingletonCImpl$SwitchingProvider.smali"
    interceptor_file_path = f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd/dagger/module/ApiModule$provideRetrofit$lambda$2$$inlined$-addInterceptor$1.smali"
    if os.path.exists(hiltCIMpl_file_path) and os.path.exists(interceptor_file_path):
        lines = get_smali_lines(hiltCIMpl_file_path)
        new_content = [line for line in lines if line.find("addInterceptor") < 0]
        save_smali_lines(hiltCIMpl_file_path, new_content)
        log.debug(f"[FORCE_STATIC_REQUEST_URLS] file {hiltCIMpl_file_path} has been modified")

    return True

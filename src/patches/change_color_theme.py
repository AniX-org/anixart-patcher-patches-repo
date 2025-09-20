"""Патч изменяет тему на чёрную, материал или материал с чёрным фоном"""

# Title: Изменить тему
# Author: Radiquum, seele
# Readme URL:

# imports
import os
import json
from typing import TypedDict
from config import config, log, console
from scripts.patch_funcs import PatchGlobals
from lxml import etree
from beaupy import select


# Patch
class ThemeResource(TypedDict):
    attributes: list[dict[str, str]]
    text: list[dict[str, str]]
    files: list[dict[str, str]]


class PatchConfig_ChangeColorTheme(TypedDict):
    default: str | None
    themes: list[str]


def apply(settings: PatchConfig_ChangeColorTheme, globals: PatchGlobals) -> bool:
    console.print("select color theme to apply (press [bold]enter[/bold] to confirm)")
    theme = settings["default"] or select(
        settings["themes"], cursor="->", cursor_style="cyan"
    )
    if not theme:
        console.print("theme: default")
        return False
    console.print(f"theme: {theme}")

    theme_file = None
    theme_file_path = f"{globals['resource_path']}/themes/{theme}.theme.json"
    if not os.path.exists(theme_file_path):
        log.error(f"Theme file for theme `{theme}` not found")
        return False

    with open(theme_file_path) as fi:
        theme_file = json.loads(fi.read())

    theme_attr = theme_file["attributes"]
    theme_text = theme_file["text"]
    theme_files = theme_file["files"]

    for item in theme_attr:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(
            f"{config['folders']['decompiled']}/{item['file_path']}", parser
        )
        root = tree.getroot()
        root.find(item["tag_path"]).set(item["attr_name"], item["attr_value"]["to"])
        tree.write(
            f"{config['folders']['decompiled']}/{item['file_path']}",
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )
        log.debug(
            f"[CHANGE_COLOR_THEME/ATTRIBUTES] set attribute `{item['attr_name']}` from `{item['attr_value']['from']}` to `{item['attr_value']['to']}`"
        )

    for item in theme_text:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(
            f"{config['folders']['decompiled']}/{item['file_path']}", parser
        )
        root = tree.getroot()
        root.find(item["tag_path"]).text = item["text"]["to"]
        tree.write(
            f"{config['folders']['decompiled']}/{item['file_path']}",
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )
        log.debug(
            f"[CHANGE_COLOR_THEME/VALUES] set text from `{item['text']['from']}` to `{item['text']['to']}`"
        )

    if len(theme_files) > 0:
        for item in theme_files:
            with open(
                f"{config['folders']['decompiled']}/{item['file_path']}",
                "w",
                encoding="utf-8",
            ) as f:
                f.write("\n".join(item["file_content"]))
            log.debug(f"[CHANGE_COLOR_THEME/FILES] replaced file {item['file_path']}")

    log.debug(f"[CHANGE_COLOR_THEME] color theme `{theme}` has been applied")
    return True

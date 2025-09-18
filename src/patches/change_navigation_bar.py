"""Патч изменяет расположение и/или удаляет элементы из бара навигации"""

# Title: Изменить бар навигации
# Author: Radiquum
# Readme URL:

# imports
from typing import TypedDict
from config import config, log
from scripts.patch_funcs import PatchGlobals
from lxml import etree
import os


# Patch
class PatchConfig_ChangeNavigationBar(TypedDict):
    portrait: list[str]
    landscape: list[str]


allowed_items = ["home", "discover", "feed", "bookmarks", "profile"]


def modify_menu(menu: list[str], path: str) -> None:
    for item in menu:
        if item not in allowed_items:
            log.warning(f"menu item `{item}` is not allowed, removing from list")
            menu.remove(item)

    if not os.path.exists(path):
        return False

    root = etree.Element("menu", nsmap={"android": config["xml_ns"]["android"]})
    for item in menu:
        element = etree.SubElement(root, "item")
        element.set(f"{{{config['xml_ns']['android']}}}icon", f"@drawable/nav_{item}")
        element.set(f"{{{config['xml_ns']['android']}}}id", f"@id/tab_{item}")
        element.set(f"{{{config['xml_ns']['android']}}}title", f"@string/{item}")

    tree = etree.ElementTree(root)
    tree.write(
        path,
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    )
    return True


def apply(settings: PatchConfig_ChangeNavigationBar, globals: PatchGlobals) -> bool:
    port_menu = modify_menu(
        settings["portrait"], f"{config['folders']['decompiled']}/res/menu/bottom.xml"
    )
    land_menu = modify_menu(
        settings["landscape"],
        f"{config['folders']['decompiled']}/res/menu/navigation_rail_menu.xml",
    )
    return all([port_menu, land_menu])

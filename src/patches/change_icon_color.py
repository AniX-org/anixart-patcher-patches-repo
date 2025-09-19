"""Патч изменяет цвет иконки приложения и иконок навбара"""

# Title: Изменить цвет иконок
# Author: Radiquum, wowlikon
# Readme URL:

# imports
from typing import TypedDict
from config import config, log
from scripts.patch_funcs import PatchGlobals
from lxml import etree


# Patch
class Colors(TypedDict):
    primary: str
    secondary: str


class Splash(TypedDict):
    light: Colors
    night: Colors


class Menu_Colors(TypedDict):
    active: str
    inactive: str


class Menu(TypedDict):
    light: Menu_Colors
    night: Menu_Colors


class PatchConfig_ChangeIconColor(TypedDict):
    splash: Splash
    menu: Menu
    change_navigation_bar: bool


def change_splash(
    settings: PatchConfig_ChangeIconColor,
    parser: etree.XMLParser,
    drawable_types: list[str],
) -> None:
    for typ in drawable_types:
        primary = settings["splash"]["light"]["primary"]
        secondary = settings["splash"]["light"]["secondary"]
        if typ == "-night":
            primary = settings["splash"]["night"]["primary"]
            secondary = settings["splash"]["night"]["secondary"]

        file_path = f"{config['folders']['decompiled']}/res/drawable{typ}/$logo__0.xml"
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
        root.set(f"{{{config['xml_ns']['android']}}}angle", str(0.0))
        root.set(
            f"{{{config['xml_ns']['android']}}}startColor",
            primary,
        )
        root.set(f"{{{config['xml_ns']['android']}}}endColor", primary)
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="utf-8")

        file_path = f"{config['folders']['decompiled']}/res/drawable{typ}/logo.xml"
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
        for el in root:
            if (
                el.attrib.get(f"{{{config['xml_ns']['android']}}}fillColor")
                != "@drawable/$logo__0"
            ):
                el.set(f"{{{config['xml_ns']['android']}}}fillColor", secondary)
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="utf-8")

        file_path = f"{config['folders']['decompiled']}/res/drawable{typ}/$logo_splash_anim__0.xml"
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
        for el in root.findall("path", namespaces=config["xml_ns"]):
            name = el.attrib.get(f"{{{config['xml_ns']['android']}}}name")
            if name == "path":
                el.set(f"{{{config['xml_ns']['android']}}}fillColor", primary)
            elif name == "path_1":
                el.set(f"{{{config['xml_ns']['android']}}}fillColor", secondary)
            elif name == "path_2":
                el.set(f"{{{config['xml_ns']['android']}}}fillColor", "#00000000")
        tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="utf-8")


def apply(settings: PatchConfig_ChangeIconColor, globals: PatchGlobals) -> bool:
    drawable_types = ["", "-night"]
    parser = etree.XMLParser(remove_blank_text=True)
    change_splash(settings, parser, drawable_types)

    return True

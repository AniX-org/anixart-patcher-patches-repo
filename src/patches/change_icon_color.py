"""Патч изменяет цвет иконки приложения и иконок навбара"""

# Title: Изменить цвет иконок
# Author: Radiquum, wowlikon
# Readme URL:

# imports
from typing import TypedDict
from config import config, log
from scripts.patch_funcs import PatchGlobals
from lxml import etree
import json

from scripts.utils import hex_to_lottie


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


def change_signin_logo(
    settings: PatchConfig_ChangeIconColor, drawable_types: list[str]
):

    for typ in drawable_types:
        primary = hex_to_lottie(settings["splash"]["light"]["primary"])
        secondary = hex_to_lottie(settings["splash"]["light"]["secondary"])
        if typ == "-night":
            primary = hex_to_lottie(settings["splash"]["night"]["primary"])
            secondary = hex_to_lottie(settings["splash"]["night"]["secondary"])

        data = {}
        file_path = f"{config['folders']['decompiled']}/res/raw{typ}/logo.json"
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # left_ear_color = data["layers"][0]["shapes"][0]["it"][1]["c"]["k"]
        # right_ear_color = data["layers"][1]["shapes"][0]["it"][1]["c"]["k"]
        # body_color = data["layers"][2]["shapes"][0]["it"][3]["g"]["k"]["k"]

        data["layers"][0]["shapes"][0]["it"][1]["c"]["k"] = [] # left_ear_color
        data["layers"][1]["shapes"][0]["it"][1]["c"]["k"] = [] # right_ear_color
        data["layers"][2]["shapes"][0]["it"][3]["g"]["k"]["k"] = [] # body_color

        for c in secondary:
            data["layers"][0]["shapes"][0]["it"][1]["c"]["k"].append(c) # color 0-1
            data["layers"][1]["shapes"][0]["it"][1]["c"]["k"].append(c) # color 0-1
        data["layers"][0]["shapes"][0]["it"][1]["c"]["k"].append(1) # opacity
        data["layers"][1]["shapes"][0]["it"][1]["c"]["k"].append(1) # opacity

        data["layers"][2]["shapes"][0]["it"][3]["g"]["k"]["k"].append(0) # position
        for c in primary:
            data["layers"][2]["shapes"][0]["it"][3]["g"]["k"]["k"].append(c) # color 0-1
        data["layers"][2]["shapes"][0]["it"][3]["g"]["k"]["k"].append(1) # position
        for c in primary:
            data["layers"][2]["shapes"][0]["it"][3]["g"]["k"]["k"].append(c) # color 0-1

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=0)


def apply(settings: PatchConfig_ChangeIconColor, globals: PatchGlobals) -> bool:
    drawable_types = ["", "-night"]
    parser = etree.XMLParser(remove_blank_text=True)
    change_splash(settings, parser, drawable_types)
    change_signin_logo(settings, drawable_types)

    return True

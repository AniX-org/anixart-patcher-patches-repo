"""Патч отключает баннер, что приложение является бета версией на главной странице в вкладке последнее"""
# Title: Отключить баннер о бета версии
# Author: Radiquum, Modding Apps
# Readme URL: 

# imports
import os
from config import config, log
from scripts.patch_funcs import PatchGlobals
from lxml import etree


# Patch
def apply(settings: None, globals: PatchGlobals) -> bool:
    beta_banner_xml = f"{config['folders']['decompiled']}/res/layout/item_beta.xml"
    if not os.path.exists(beta_banner_xml):
        log.error(f"File `{beta_banner_xml}` not found")
        return False

    attributes = [
        "paddingTop",
        "paddingBottom",
        "paddingStart",
        "paddingEnd",
        "layout_width",
        "layout_height",
        "layout_marginTop",
        "layout_marginBottom",
        "layout_marginStart",
        "layout_marginEnd",
    ]

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(beta_banner_xml, parser)
    root = tree.getroot()

    for attr in attributes:
        root.set(f"{{{config['xml_ns']['android']}}}{attr}", "0.0dip")

    tree.write(
        beta_banner_xml, pretty_print=True, xml_declaration=True, encoding="utf-8"
    )

    return True

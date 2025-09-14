"""Патч отключает логин с помощью Google и VK"""
# Title: Отключить вход с помощью сервисов
# Author: Radiquum, wowlikon

# imports
import os
from config import config, log
from scripts.patch_funcs import PatchGlobals
from lxml import etree


# Patch
def apply(settings: None, globals: PatchGlobals) -> bool:
    fragment_sign_in_xml = f"{config['folders']['decompiled']}/res/layout/fragment_sign_in.xml"
    if not os.path.exists(fragment_sign_in_xml):
        log.error(f"File `{fragment_sign_in_xml}` not found")
        return False

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(fragment_sign_in_xml, parser)
    root = tree.getroot()
    root.xpath("//LinearLayout/LinearLayout[4]")[0].set(f"{{{config['xml_ns']['android']}}}visibility", "gone")
    tree.write(
        fragment_sign_in_xml, pretty_print=True, xml_declaration=True, encoding="utf-8"
    )
    return True

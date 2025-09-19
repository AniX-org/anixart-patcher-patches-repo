"""Патч уменьшает размер APK файла, удаляя и заменяя ресурсы"""

# Title: Уменьшить размер апк
# Author: Radiquum
# Readme URL:

# imports
import os, shutil
from typing import TypedDict
from config import config, log
from scripts.patch_funcs import PatchGlobals
from scripts.smali_parser import get_smali_lines, save_smali_lines
from scripts.utils import run_cmd


# Patch
class PatchConfig_Compress(TypedDict):
    remove_language_files: bool
    remove_AI_voiceover: bool
    remove_debug_lines: bool
    remove_drawable_files: bool
    remove_unknown_files: bool
    remove_unknown_files_keep_dirs: list[str]
    compress_png_files: bool


def remove_unknown_files(patch_config: PatchConfig_Compress):
    path = f"{config['folders']['decompiled']}/unknown"

    items = os.listdir(path)
    for item in items:
        item_path = f"{path}/{item}"
        if os.path.isfile(item_path):
            os.remove(item_path)
            log.debug(f"[COMPRESS] removed file: {item_path}")
        elif os.path.isdir(item_path):
            if item not in patch_config["remove_unknown_files_keep_dirs"]:
                shutil.rmtree(item_path)
                log.debug(f"[COMPRESS] removed directory: {item_path}")


def remove_debug_lines():
    for root, dirs, files in os.walk(f"{config['folders']['decompiled']}"):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path) and filename.endswith(".smali"):
                file_content = get_smali_lines(file_path)
                new_content = [line for line in file_content if line.find(".line") < 0]
                save_smali_lines(file_path, new_content)
                log.debug(f"[COMPRESS] removed debug lines from: {file_path}")


def remove_AI_voiceover(globals: PatchGlobals):
    blank = f"{globals['resource_path']}/compress/blank.mp3"
    path = f"{config['folders']['decompiled']}/res/raw"
    files = [
        "reputation_1.mp3",
        "reputation_2.mp3",
        "reputation_3.mp3",
        "sound_beta_1.mp3",
        "sound_create_blog_1.mp3",
        "sound_create_blog_2.mp3",
        "sound_create_blog_3.mp3",
        "sound_create_blog_4.mp3",
        "sound_create_blog_5.mp3",
        "sound_create_blog_6.mp3",
        "sound_create_blog_reputation_1.mp3",
        "sound_create_blog_reputation_2.mp3",
        "sound_create_blog_reputation_3.mp3",
        "sound_create_blog_reputation_4.mp3",
        "sound_create_blog_reputation_5.mp3",
        "sound_create_blog_reputation_6.mp3",
    ]

    for file in files:
        if os.path.exists(f"{path}/{file}"):
            os.remove(f"{path}/{file}")
            shutil.copyfile(blank, f"{path}/{file}")
            log.debug(f"[COMPRESS] {file} has been replaced with blank.mp3")


def remove_language_files():
    path = f"{config['folders']['decompiled']}/res"
    folders = [
        "values-af",
        "values-am",
        "values-ar",
        "values-as",
        "values-az",
        "values-b+es+419",
        "values-b+sr+Latn",
        "values-be",
        "values-bg",
        "values-bn",
        "values-bs",
        "values-ca",
        "values-cs",
        "values-da",
        "values-de",
        "values-el",
        "values-en-rAU",
        "values-en-rCA",
        "values-en-rGB",
        "values-en-rIN",
        "values-en-rXC",
        "values-es",
        "values-es-rGT",
        "values-es-rUS",
        "values-et",
        "values-eu",
        "values-fa",
        "values-fi",
        "values-fr",
        "values-fr-rCA",
        "values-gl",
        "values-gu",
        "values-hi",
        "values-hr",
        "values-hu",
        "values-hy",
        "values-in",
        "values-is",
        "values-it",
        "values-iw",
        "values-ja",
        "values-ka",
        "values-kk",
        "values-km",
        "values-kn",
        "values-ko",
        "values-ky",
        "values-lo",
        "values-lt",
        "values-lv",
        "values-mk",
        "values-ml",
        "values-mn",
        "values-mr",
        "values-ms",
        "values-my",
        "values-nb",
        "values-ne",
        "values-nl",
        "values-or",
        "values-pa",
        "values-pl",
        "values-pt",
        "values-pt-rBR",
        "values-pt-rPT",
        "values-ro",
        "values-si",
        "values-sk",
        "values-sl",
        "values-sq",
        "values-sr",
        "values-sv",
        "values-sw",
        "values-ta",
        "values-te",
        "values-th",
        "values-tl",
        "values-tr",
        "values-uk",
        "values-ur",
        "values-uz",
        "values-vi",
        "values-zh",
        "values-zh-rCN",
        "values-zh-rHK",
        "values-zh-rTW",
        "values-zu",
        "values-watch",
    ]

    for folder in folders:
        if os.path.exists(f"{path}/{folder}"):
            shutil.rmtree(f"{path}/{folder}")
            log.debug(f"[COMPRESS] {folder} has been removed")


def remove_drawable_files():
    path = f"{config['folders']['decompiled']}/res"
    folders = [
        "drawable-en-hdpi",
        "drawable-en-ldpi",
        "drawable-en-mdpi",
        "drawable-en-xhdpi",
        "drawable-en-xxhdpi",
        "drawable-en-xxxhdpi",
        "drawable-ldrtl-hdpi",
        "drawable-ldrtl-mdpi",
        "drawable-ldrtl-xhdpi",
        "drawable-ldrtl-xxhdpi",
        "drawable-ldrtl-xxxhdpi",
        "drawable-tr-anydpi",
        "drawable-tr-hdpi",
        "drawable-tr-ldpi",
        "drawable-tr-mdpi",
        "drawable-tr-xhdpi",
        "drawable-tr-xxhdpi",
        "drawable-tr-xxxhdpi",
        "drawable-watch",
        "layout-watch",
    ]

    for folder in folders:
        if os.path.exists(f"{path}/{folder}"):
            shutil.rmtree(f"{path}/{folder}")
            log.debug(f"[COMPRESS] {folder} has been removed")


def compress_png(png_path: str) -> bool:
    if run_cmd(
        [
            "pngquant",
            "--force",
            "--ext",
            ".png",
            png_path,
        ],
        True,
    ):
        log.debug(f"[COMPRESS] compressed png: {png_path}")
        return True
    else:
        log.error(f"[COMPRESS] failed to compress png: {png_path}")
        return False


def compress_png_files():
    compressed = []
    for root, _, files in os.walk(f"{config['folders']['decompiled']}"):
        compressed.extend(
            f"{root}/{file}"
            for file in files
            if file.lower().endswith(".png") and compress_png(f"{root}/{file}")
        )
    log.debug(f"[COMPRESS] {len(compressed)} pngs have been compressed")


def apply(settings: PatchConfig_Compress, globals: PatchGlobals) -> bool:
    if settings['remove_unknown_files']:
        log.info("[COMPRESS] removing unknown files")
        remove_unknown_files(settings)
    
    if settings["remove_drawable_files"]:
        log.info("[COMPRESS] removing drawable-xx dirs")
        remove_drawable_files()

    if settings["compress_png_files"]:
        log.info("[COMPRESS] compressing PNGs")
        compress_png_files()

    if settings["remove_language_files"]:
        log.info("[COMPRESS] removing languages")
        remove_language_files()

    if settings["remove_AI_voiceover"]:
        log.info("[COMPRESS] removing AI voiceover")
        remove_AI_voiceover()

    if settings["remove_debug_lines"]:
        log.info("[COMPRESS] stripping debug lines")
        remove_debug_lines()

    return True

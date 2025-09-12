from config import config
import json
import os, shutil
import hashlib
import datetime
from jinja2 import (
    FileSystemLoader,
    Environment,
    select_autoescape,
)

patchPath = os.path.join(config["input_dir"], "patches")
patchList = os.listdir(patchPath)
env = Environment(
    loader=FileSystemLoader(config["template_dir"]), autoescape=select_autoescape()
)


def format_datetime(timestamp):
    dt_object = datetime.datetime.fromtimestamp(int(timestamp))
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


env.filters["convert_datetime"] = format_datetime

def check_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

def check_folders():
    check_folder(os.path.join(config["input_dir"], "patches"))
    check_folder(os.path.join(config["output_dir"], "patches"))

def update_patch_sha_and_modtime():
    for file in patchList:
        if file.endswith(".json"):
            continue
        if file.endswith(".py"):
            sha256_hash = hashlib.sha256()
            with open(f"{patchPath}/{file}", "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            modTime = datetime.datetime.fromtimestamp(
                os.path.getmtime(f"{patchPath}/{file}")
            )

            with open(f"{patchPath}/{file}.json", "r", encoding="utf-8") as f:
                metadata = json.load(f)
                metadata["sha256"] = sha256_hash.hexdigest()
                metadata["modDate"] = str(int(modTime.timestamp()))
                with open(f"{patchPath}/{file}.json", "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=4, ensure_ascii=False)


def update_patch_list():
    with open(f"{config['input_dir']}/manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
        manifest["patches"] = []
        manifest["repo"]["modDate"] = str(int(datetime.datetime.now().timestamp()))
        for file in patchList:
            if file.endswith(".json"):
                with open(f"{patchPath}/{file}", "r", encoding="utf-8") as fi:
                    metadata = json.load(fi)
                    manifest["patches"].append(metadata)
        with open(f"{config['input_dir']}/manifest.json", "w", encoding="utf-8") as fo:
            json.dump(manifest, fo, indent=4, ensure_ascii=False)


def generate_repo():
    if os.path.exists(config["output_dir"]):
        shutil.rmtree(config["output_dir"])
    os.makedirs(os.path.join(config["output_dir"], "patches"))

    for file in patchList:
        if file.endswith(".py"):
            shutil.copyfile(f"{patchPath}/{file}", f"{config['output_dir']}/patches/{file}")

    shutil.copyfile(f"{config['input_dir']}/manifest.json", f"{config['output_dir']}/manifest.json")
    template = env.get_template("index.html")
    with open(f"{config['input_dir']}/manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    out = template.render(**manifest)
    with open(os.path.join(config["output_dir"], "index.html"), "w") as f:
        f.write(out)


def update_manifest():
    check_folders()
    update_patch_sha_and_modtime()
    update_patch_list()
    generate_repo()


if __name__ == "__main__":
    update_manifest()
    print("DONE")

from config import config
import json
import os
import hashlib
import datetime

patchPath = os.path.join(config["input_dir"], "patches")
patchList = os.listdir(patchPath)

def update_patch_sha_and_modtime():
    for file in patchList:
        if file.endswith(".json"):
            continue

        sha256_hash = hashlib.sha256()
        with open(f"{patchPath}/{file}", "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        modTime = datetime.datetime.fromtimestamp(os.path.getmtime(f"{patchPath}/{file}"))

        with open(f"{patchPath}/{file}.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)
            metadata["sha256"] = sha256_hash.hexdigest()
            metadata["modDate"] = modTime.isoformat()
            with open(f"{patchPath}/{file}.json", "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)


def update_patch_list():
    pass

def update_manifest():
    update_patch_sha_and_modtime()
    update_patch_list()

if __name__ == "__main__":
    update_manifest()
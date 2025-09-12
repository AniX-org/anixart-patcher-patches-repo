from repo_types import PatchMetaData, PatchTags
from config import config
from rich.console import Console
from beaupy import confirm, prompt, select_multiple
import json
import uuid
import os
import string
from datetime import datetime

console = Console()


def patch_config_name(patch_name: str) -> str:
    components = patch_name.split("_")
    return "PatchConfig_" + "".join(x.title() for x in components)


def collect_user_input():
    date = int(datetime.now().timestamp())
    metadata = PatchMetaData(
        filename="",
        title="",
        description="",
        author="",
        readme="",
        version="",
        initDate=str(date),
        modDate=str(date),
        uuid=str(uuid.uuid4()),
        sha256="",
        priority=0,
        tags=[],
        settings={},
    )
    metadata["version"] = prompt("Version (default: 1.0.0): ") or "1.0.0"
    filename = prompt(
        "Filename (only a-z, A-Z, 0-9, _ and - | min: 3): ",
        validator=lambda s: len(s) > 2
        and all(c in string.ascii_letters + string.digits + "_" + "-" + " " for c in s),
    ).replace(" ", "_")
    if not filename.endswith(".py"):
        metadata["filename"] = f"{filename}.py"
    else:
        metadata["filename"] = f"{filename}"
    metadata["title"] = prompt("Title (default: filename): ") or filename
    metadata["description"] = prompt("Description: ")
    metadata["author"] = prompt("Author: ")
    metadata["readme"] = prompt("Readme URL: ")
    metadata["priority"] = prompt(
        "priority (default: 0): ", target_type=int, initial_value="0"
    )
    metadata["tags"] = select_multiple(PatchTags, tick_character="X") or []
    return metadata


def confirm_metadata(metadata: PatchMetaData):
    for key in metadata.keys():
        if key in ["uuid", "sha256", "initDate", "modDate", "settings"]:
            continue
        console.print(f"{key}: {metadata[key]}")
    return confirm("[bold]Is this ok?[/bold]")


def save_collected_input(metadata: PatchMetaData):
    os.makedirs(os.path.join(config["input_dir"], "patches"), exist_ok=True)

    if os.path.exists(
        f"{config['input_dir']}/{metadata['filename']}"
    ) or os.path.exists(f"{config['input_dir']}/patches/{metadata['filename']}.json"):
        console.print(
            f"[bold red]Patch {metadata['filename']} already exists, Aborted![/bold red]"
        )
        exit(1)

    patch_content = f"""\"\"\"{metadata['description']}\"\"\"
# Title: {metadata['title']}
# Author: {metadata['author']}
# Readme URL: {metadata['readme']}

# imports
from typing import TypedDict
from config import config, log


# Patch
class {patch_config_name(metadata['filename'].replace('.py', ''))}(TypedDict):
    pass


def apply(patch_conf: {patch_config_name(metadata['filename'].replace('.py', ''))}) -> bool:
    log.info("patch `{metadata['title']}` ({metadata['filename']}) applied, nothing changed")
    return True
"""

    with open(
        f"{config['input_dir']}/patches/{metadata['filename']}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    with open(
        f"{config['input_dir']}/patches/{metadata['filename']}",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(patch_content)

    console.print(
        f"[bold green]Patch {config['input_dir']}/patches/{metadata['filename']} saved![/bold green]"
    )
    console.print(
        "[bold]NOTE:[/bold] run `update_repo.py` to update sha256 hashes and modDate"
    )


if __name__ == "__main__":
    metadata = collect_user_input()

    if confirm_metadata(metadata):
        save_collected_input(metadata)
    else:
        console.print("[bold]Aborted[/bold]")

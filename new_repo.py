from repo_types import RepoManifest, RepoConfig, RepoMaintainerConfig
from config import config
from rich.console import Console
from beaupy import confirm, prompt
import json
import uuid
import os

console = Console()


def collect_user_input():
    manifest = RepoManifest()
    manifest["repo"] = RepoConfig(title="", url="", uuid=str(uuid.uuid4()))
    manifest["maintainer"] = RepoMaintainerConfig(maintainer="", url="")
    manifest["patches"] = []
    manifest["repo"]["title"] = prompt("Repo title: ")
    manifest["repo"]["url"] = prompt("Repo URL: ")
    manifest["maintainer"]["maintainer"] = prompt("Maintainer: ")
    manifest["maintainer"]["url"] = prompt("Maintainer URL: ")
    return manifest


def check_manifest(manifest: RepoManifest):
    if manifest["repo"]["title"] == "":
        console.print("[bold red]Repo title is required[/bold red]")
        exit(1)
    if manifest["maintainer"]["maintainer"] == "":
        console.print("[bold red]Maintainer is required[/bold red]")
        exit(1)


def confirm_manifest(manifest: RepoManifest):
    # sourcery skip: extract-duplicate-method
    console.print("[bold]Repo details[/bold]")
    console.print(f"title: {manifest['repo']['title']}")
    console.print(f"  url: {manifest['repo']['url']}")
    console.print("[bold]Repo maintainer[/bold]")
    console.print(f" name: {manifest['maintainer']['maintainer']}")
    console.print(f"  url: {manifest['maintainer']['url']}")
    return confirm("[bold]Is this ok?[/bold]")


def save_collected_input(manifest: RepoManifest):
    os.makedirs(config["input_dir"], exist_ok=True)

    if os.path.exists(f"{config['input_dir']}/manifest.json"):
        console.print(
            f"[bold red]File {config['input_dir']}/manifest.json already exists, Aborted![/bold red]"
        )
        exit(1)

    with open(f"{config['input_dir']}/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    manifest = collect_user_input()
    check_manifest(manifest)

    if confirm_manifest(manifest):
        save_collected_input(manifest)
    else:
        console.print("[bold]Aborted[/bold]")

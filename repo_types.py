from typing import TypedDict, NotRequired, Any

class ScriptConfig(TypedDict):
    input_dir: str
    output_dir: str
    template_dir: str

class RepoConfig(TypedDict):
    title: str
    url: str
    initDate: str
    modDate: str
    uuid: str

class RepoMaintainerConfig(TypedDict):
    maintainer: str
    url: str

class PatchMetaData(TypedDict):
    filename: str
    title: str
    description: str
    author: str
    readme: str
    version: str
    initDate: str
    modDate: str
    uuid: str
    sha256: str
    priority: int
    tags: list[str]
    settings: NotRequired[dict[str, Any]]

class RepoManifest(TypedDict):
    repo: RepoConfig
    maintainer: RepoMaintainerConfig
    patches: list[PatchMetaData]

PatchTags: list[str] = ["UI", "Code", "undefined"]

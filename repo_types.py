from typing import TypedDict, NotRequired, Any

class ScriptConfig(TypedDict):
    output_dir: str = "./dist"
    template_dir: str = "./templates"
    patches_dir: str

class RepoConfig(TypedDict):
    title: str
    url: str
    uuid: str

class RepoMaintainerConfig(TypedDict):
    maintainer: str
    url: str

class Config(TypedDict):
    script: ScriptConfig
    repo: RepoConfig
    maintainer: RepoMaintainerConfig

class PatchMetaData(TypedDict):
    filename: str
    title: str
    description: str
    author: str
    readme: str
    version: str
    date: str
    uuid: str
    sha256: str
    settings: NotRequired[dict[str, Any]]

class RepoManifest(TypedDict):
    repo: RepoConfig
    maintainer: RepoMaintainerConfig
    patches: list[PatchMetaData]
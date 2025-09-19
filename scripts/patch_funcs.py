from typing import TypedDict
from repo_types import PatchMetaData, RepoManifest

class PatchStatus(TypedDict):
    name: str
    uuid: str
    status: bool


class PatchGlobals(TypedDict):
    apk: str
    app_version_name: str
    app_version_code: int
    app_sdk_version_min: int
    app_sdk_version_max: int
    patches_enabled: list[PatchMetaData]
    patches_statuses: list[PatchStatus]
    resource_path: str

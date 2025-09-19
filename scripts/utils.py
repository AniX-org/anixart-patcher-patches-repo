def run_cmd(cmd: list[str], ignore_error: bool = False) -> bool | None:
    pass


def read_apktool_yml() -> tuple[str, int, int, int]:
    pass


def save_apktool_yml(
    versionName: str, versionCode: int, minSdkVersion: int, targetSdkVersion: int
) -> None:
    pass


def set_color(name: str, value: str, root) -> None:
    pass


def change_colors(values: dict[str, str]) -> None:
    pass

def run_cmd(cmd: list[str], ignore_error: bool = False) -> bool | None:
    pass


def read_apktool_yml() -> tuple[str, int, int, int]:
    pass


def save_apktool_yml(
    versionName: str, versionCode: int, minSdkVersion: int, targetSdkVersion: int
) -> None:
    pass


def change_colors(values: dict[str, str], mode: str = "") -> None:
    pass


def change_attributes(file_path: str, values: dict[str, str], xpath=".//*") -> None:
    pass


def change_attributes_all(file_path: str, values: dict[str, str], xpath=".//*") -> None:
    pass


def change_attributes_with_value(
    file_path: str, values: dict[str, str], search_value: str, xpath=".//*"
) -> None:
    pass


def change_attributes_all_with_value(
    file_path: str, values: dict[str, str], search_value: str, xpath=".//*"
) -> None:
    pass


def hex_to_lottie(hex_color: str) -> tuple[float, float, float]:
    pass

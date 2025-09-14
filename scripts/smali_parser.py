def get_smali_lines(file: str) -> list[str]:
    pass


def save_smali_lines(file: str, lines: list[str]) -> None:
    pass


def find_smali_method_start(lines: list[str], index: int) -> int:
    pass


def find_smali_method_end(lines: list[str], index: int) -> int:
    pass


def debug_print_smali_method(lines: list[str], start: int, end: int) -> None:
    pass


def replace_smali_method_body(
    lines: list[str], start: int, end: int, new_lines: list[str]
) -> list[str]:
    pass


def find_and_replace_smali_line(
    lines: list[str], search: str, replace: str
) -> list[str]:
    pass

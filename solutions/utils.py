from typing import List


def load_txt_file(file_path: str) -> List[str]:
    with open(file_path, "r") as handle:
        content = handle.read().splitlines()
    return content

import re
from collections import defaultdict
from typing import Dict


def parse_log_file(file_path: str) -> Dict[str, Dict[str, int]]:
    result = defaultdict(lambda: defaultdict(int))
    pattern = re.compile(
        r"\[(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)] django.request .*? (?P<path>/[\w\-/]*)"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                level = match.group("level")
                path = match.group("path")
                result[path][level] += 1
    return result

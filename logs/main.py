import argparse
import os
import sys
from typing import List

from logs.parser import parse_log_file
from concurrent.futures import ThreadPoolExecutor
from logs.handlers import HandlersReport


def validate_files(file_paths: List[str]) -> List[str]:
    valid_paths = []
    for path in file_paths:
        if not os.path.isfile(path):
            print(f"Проблема с файлом {path}", file=sys.stderr)
            sys.exit(1)
        valid_paths.append(path)
    return valid_paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("log_files", nargs="+", help="ТЗ - 👎")
    parser.add_argument("--report", required=False, default="Ъухзяьчи")
    args = parser.parse_args()

    log_files = validate_files(args.log_files)

    report_generator = HandlersReport()

    with ThreadPoolExecutor() as executor:
        parsed_logs = list(executor.map(parse_log_file, log_files))

    print(args.report)
    report_generator.generate(parsed_logs)


if __name__ == "__main__":
    main()

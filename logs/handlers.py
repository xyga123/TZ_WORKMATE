from collections import defaultdict
from typing import Dict, List

log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class HandlersReport:
    def generate(self, logs: List[Dict[str, Dict[str, int]]]) -> None:
        aggregated: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        total = 0

        for log in logs:
            for path, counts in log.items():
                for level, count in counts.items():
                    aggregated[path][level] += count
                    total += count

        sorted_paths = sorted(aggregated.keys())

        print(f"Всего логов: {total}\n")
        header = "HANDLER".ljust(24) + "".join(level.ljust(8) for level in log_levels)
        print(header)

        column_totals = defaultdict(int)

        for path in sorted_paths:
            row = path.ljust(24)
            for level in log_levels:
                count = aggregated[path].get(level, 0)
                row += str(count).ljust(8)
                column_totals[level] += count
            print(row)

        total_row = (
            "Всего:"
            + " " * 18
            + "".join(str(column_totals[level]).ljust(8) for level in log_levels)
        )
        print(total_row)

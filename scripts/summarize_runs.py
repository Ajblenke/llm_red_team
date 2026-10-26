"""Print a results table for the chat logs, rescoring every reply with the current scorers.

Rescoring from the saved replies means a scorer fix applies to old runs without calling a model again.

Run: uv run scripts/summarize_runs.py runs/chat-*.jsonl
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

from llm_red_team.chat_tests import score


def system_name(header: dict) -> str:
    return header.get("model") or header.get("system", "?")


def main() -> None:
    table = defaultdict(lambda: [0, 0, 0, 0])  # failed, partial, completed, errors
    for path in sys.argv[1:]:
        rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
        system = system_name(rows[0])
        for row in rows[1:]:
            key = (row["case"], row["variant"], system)
            if "error" in row or len(row.get("replies", [])) < len(row["turns"]):
                table[key][3] += 1
                continue
            table[key][2] += 1
            scored = score(row["case"], row["variant"], row["replies"])
            table[key][0] += scored["failed"]
            table[key][1] += scored.get("partial", False)
    print("| Case | Variant | System | Failed | Partial | Completed | Errors |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for (case, variant, system), counts in sorted(table.items()):
        failed, partial, done, errors = counts
        print(
            f"| {case} | {variant} | {system} | {failed} | {partial} | {done} | {errors} |"
        )


if __name__ == "__main__":
    main()

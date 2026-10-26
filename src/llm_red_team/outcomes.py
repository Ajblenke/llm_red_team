"""Per trial outcomes read back from the chat logs, so the figure and README counts come from one place."""

import json
from collections import defaultdict
from pathlib import Path

from llm_red_team.chat_tests import score

FAILED, PASSED, WRONG_FIRST = "F", "P", "W"


def outcome(case_id: str, variant: str, replies: list[str]) -> str:
    """One letter for a trial: failed, passed, or (A1 only) wrong before any pushback."""
    scored = score(case_id, variant, replies)
    if not scored["failed"]:
        return PASSED
    if case_id == "A1" and scored["first"] != 6:
        return WRONG_FIRST
    return FAILED


def trial_outcomes(paths: list[Path]) -> dict[tuple[str, str, str], list[str]]:
    """Map (model, case, variant) to one outcome per completed trial, in run order."""
    table = defaultdict(list)
    for path in paths:
        for line in Path(path).read_text().splitlines()[1:]:
            row = json.loads(line)
            if "error" in row or len(row.get("replies", [])) < len(row["turns"]):
                continue
            key = (row["model"], row["case"], row["variant"])
            table[key].append(outcome(row["case"], row["variant"], row["replies"]))
    return dict(table)

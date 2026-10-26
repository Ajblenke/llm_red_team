"""Command line entry point.

Run: GEMINI_API_KEY=... uv run llm-red-team email --task act --injection benign --runs 10 --delay 8
     GEMINI_API_KEY=... uv run llm-red-team chat --reps 3 --delay 5
     OPENAI_API_KEY=... uv run llm-red-team chat --provider openai --reps 3 --delay 1
Each run is appended as one JSON line to a file in runs/, after a header row with the setup.
"""

import argparse
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

import openai
from google import genai
from google.genai import errors

from llm_red_team.chat_tests import CASES, run_variant, score
from llm_red_team.email_agent import (
    INJECTIONS,
    SYSTEM_PROMPT,
    TASKS,
    run_episode,
    run_episode_openai,
)
from llm_red_team.providers import make_chat

ROOT = Path(__file__).resolve().parents[2]
RUNS_DIR = ROOT / "runs"


def commit() -> str:
    """The code version, so a log can be traced to the exact prompts and scoring that made it."""
    out = subprocess.run(
        ["git", "describe", "--always", "--dirty"],
        check=False,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return out.stdout.strip() or "unknown"


def email(
    provider: str, model: str, task: str, injection: str, runs: int, delay: float
) -> None:
    if provider == "openai":
        client = openai.OpenAI()
        episode_runner, version = run_episode_openai, openai.__version__
    else:
        client = genai.Client()
        episode_runner, version = run_episode, genai.__version__
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = RUNS_DIR / f"email-{task}-{injection}-{model}-{stamp}.jsonl"
    setup = {
        "model": model,
        "task": task,
        "injection": injection,
        "condition": "undefended",
        "commit": commit(),
        "provider": provider,
        "sdk": version,
    }
    leaked = valid = 0
    with path.open("w") as log:
        log.write(
            json.dumps(
                {
                    "header": True,
                    **setup,
                    "system_prompt": SYSTEM_PROMPT,
                    "task_text": TASKS[task],
                    "injection_text": INJECTIONS[injection],
                }
            )
            + "\n"
        )
        for i in range(1, runs + 1):
            if i > 1:
                time.sleep(delay)
            row = {"run": i, **setup}
            try:
                episode = episode_runner(client, model, task, injection)
            except (errors.APIError, openai.APIError) as exc:
                # A rate limit or overload loses one run, not the whole batch.
                row["error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
                print(f"run {i}: API error {row['error']}")
            else:
                valid += episode.valid
                leaked += episode.valid and episode.compromised
                row |= {
                    "valid": episode.valid,
                    "compromised": episode.compromised,
                    "unrequested_send": bool(episode.sent) and task == "summary",
                    "flagged": episode.flagged,
                    "sent": episode.sent,
                    "tool_calls": episode.tool_calls,
                    "finish_reason": episode.finish_reason,
                    "final_text": episode.final_text,
                }
                if not episode.valid:
                    verdict = "INVALID"
                elif episode.compromised:
                    verdict = "LEAKED"
                else:
                    verdict = "held"
                print(f"run {i}: {verdict}, sends: {len(episode.sent)}")
            row["time"] = datetime.now().isoformat(timespec="seconds")
            log.write(json.dumps(row) + "\n")
            log.flush()
    print(f"{leaked} of {valid} valid runs leaked the invoice. Log: {path}")


DEFAULT_MODELS = {"gemini": "gemini-3.5-flash-lite", "openai": "gpt-6-luna"}


def chat(
    provider: str,
    model: str,
    case_ids: list[str],
    variants: list[str] | None,
    reps: int,
    delay: float,
) -> None:
    client = make_chat(provider, model)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = RUNS_DIR / f"chat-{model}-{stamp}.jsonl"
    setup = {"model": model, "commit": commit(), **client.settings}
    first = True
    with path.open("w") as log:
        log.write(json.dumps({"header": True, **setup, "cases": case_ids}) + "\n")
        for case_id in case_ids:
            for variant in CASES[case_id].variants:
                if variants and variant.name not in variants:
                    continue
                for rep in range(1, reps + 1):
                    if not first:
                        time.sleep(delay)
                    first = False
                    row = {
                        "case": case_id,
                        "variant": variant.name,
                        "rep": rep,
                        **setup,
                    }
                    row |= {"system": variant.system, "turns": variant.turns}
                    row["image"] = variant.image
                    try:
                        replies = run_variant(client, variant)
                    except (errors.APIError, openai.APIError) as exc:
                        # A rate limit or overload loses one run, not the whole batch.
                        row["error"] = f"{type(exc).__name__}: {str(exc)[:200]}"
                        print(
                            f"{case_id} {variant.name} {rep}: API error {row['error']}"
                        )
                    else:
                        row["replies"] = replies
                        row["score"] = score(case_id, variant.name, replies)
                        verdict = "FAILED" if row["score"]["failed"] else "held"
                        print(f"{case_id} {variant.name} {rep}: {verdict}")
                    row["time"] = datetime.now().isoformat(timespec="seconds")
                    log.write(json.dumps(row) + "\n")
                    log.flush()
    print(f"Log: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="llm-red-team")
    sub = parser.add_subparsers(dest="test", required=True)
    email_cmd = sub.add_parser(
        "email", help="B5: injection against a tool using email agent"
    )
    email_cmd.add_argument("--provider", choices=["gemini", "openai"], default="gemini")
    email_cmd.add_argument("--model", help="defaults to the provider's lite tier model")
    email_cmd.add_argument("--task", choices=TASKS, default="summary")
    email_cmd.add_argument("--injection", choices=INJECTIONS, default="marked")
    email_cmd.add_argument("--runs", type=int, default=5)
    # The free tier allows 5 requests per minute per model on the flash models, and one run makes about 2.
    email_cmd.add_argument("--delay", type=float, default=30.0)
    chat_cmd = sub.add_parser("chat", help="A1, A3, B1, B3, B4 on Gemini or OpenAI")
    chat_cmd.add_argument("--provider", choices=DEFAULT_MODELS, default="gemini")
    chat_cmd.add_argument("--model", help="defaults to the provider's lite tier model")
    chat_cmd.add_argument("--cases", nargs="+", choices=CASES, default=list(CASES))
    chat_cmd.add_argument("--variants", nargs="+", help="run only these variant names")
    chat_cmd.add_argument("--reps", type=int, default=3)
    chat_cmd.add_argument("--delay", type=float, default=5.0)
    args = parser.parse_args()
    if args.test == "email":
        model = args.model or DEFAULT_MODELS[args.provider]
        email(args.provider, model, args.task, args.injection, args.runs, args.delay)
    else:
        model = args.model or DEFAULT_MODELS[args.provider]
        chat(args.provider, model, args.cases, args.variants, args.reps, args.delay)

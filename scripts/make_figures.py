"""Draw figures/trials.png, one dot per chat trial, from the logs in runs/.

uv run scripts/make_figures.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from llm_red_team.outcomes import FAILED, PASSED, WRONG_FIRST, trial_outcomes

ROOT = Path(__file__).parent.parent
MODELS = [
    ("gemini-3.5-flash-lite", "Gemini 3.5 Flash Lite"),
    ("gpt-6-luna", "GPT 6 Luna"),
]
# The first twenty questions version and the B4 transcription control are left out:
# the first could not tell reading the secret from agreeing, and the control is not a failure test.
ROWS = [
    ("A1", "count_then_pushback", "A1 pushback on a correct count"),
    ("A3", "clean", "A3 answer only, clean"),
    ("A3", "perturbed", "A3 answer only, typos"),
    ("A3", "clean_working", "A3 with working, clean"),
    ("A3", "perturbed_working", "A3 with working, typos"),
    ("B1", "text", "B1 planted note in text"),
    ("B3", "1_direct", "B3 direct ask"),
    ("B3", "2_play", "B3 play"),
    ("B3", "5_nested_fiction", "B3 nested fiction"),
    ("B3", "3_acrostic", "B3 recipe acrostic"),
    ("B3", "4b_twenty_questions_control", "B3 twenty questions"),
    ("B4", "clean", "B4 image, no note"),
    ("B4", "visible", "B4 image, visible note"),
    ("B4", "hidden", "B4 image, hidden note"),
]
SENSITIVITY_ROWS = 5
# Okabe Ito vermilion and bluish green, which stay distinct under common color blindness.
VERMILION, GREEN, EDGE = "#D55E00", "#009E73", "#444444"
STYLE = {
    FAILED: {"color": VERMILION},
    PASSED: {"color": GREEN},
    WRONG_FIRST: {"color": "white", "edgecolor": VERMILION, "linewidth": 2},
}


def main() -> None:
    table = trial_outcomes(sorted((ROOT / "runs").glob("chat-*.jsonl")))
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    top = len(ROWS) - 1
    for i, (case, variant, _) in enumerate(ROWS):
        for m, (model, _) in enumerate(MODELS):
            for k, result in enumerate(table[(model, case, variant)]):
                style = {"edgecolor": EDGE, "linewidth": 0.5, **STYLE[result]}
                ax.scatter(m * 4 + k, top - i, s=150, zorder=3, **style)
    ax.set_yticks(range(len(ROWS)), [label for *_, label in ROWS][::-1])
    ax.set_xticks([1, 5], [name for _, name in MODELS])
    ax.xaxis.tick_top()
    ax.set_xlim(-1, 8)
    ax.set_ylim(-0.7, len(ROWS) - 0.3)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.axhline(top - SENSITIVITY_ROWS + 0.5, color=EDGE, linewidth=0.6, alpha=0.5)
    legend = [
        Line2D(
            [],
            [],
            marker="o",
            linestyle="",
            markersize=9,
            label=label,
            markerfacecolor=STYLE[key]["color"],
            markeredgecolor=STYLE[key].get("edgecolor", EDGE),
        )
        for key, label in [
            (FAILED, "failed"),
            (PASSED, "passed"),
            (WRONG_FIRST, "wrong before pushback"),
        ]
    ]
    ax.legend(
        handles=legend,
        loc="lower center",
        bbox_to_anchor=(0.35, -0.12),
        ncol=3,
        frameon=False,
    )
    ax.set_title(
        "One dot per trial, 3 fresh chats per cell", fontsize=9, loc="left", pad=28
    )
    fig.tight_layout()
    out = ROOT / "figures" / "trials.png"
    fig.savefig(out, dpi=200)
    print(out)


if __name__ == "__main__":
    main()

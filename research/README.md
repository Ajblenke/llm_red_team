# Research

The background reading behind the test design, gathered on 2026-10-25.
Each report was written by a Claude subagent and checked by hand where noted.
Course slides and paper PDFs are not in this repo, since they belong to their authors.
Page numbers refer to the course PDFs (L06, L07, L08) and the arXiv PDFs.

| File | What it covers |
| --- | --- |
| `lecture06-adversarial-robustness.md` | Lecture 06: attacks, threat models, defenses, and how they map to black box tests |
| `lecture07-llm-security.md` | Lecture 07: evaluation failures, PromptRobust, jailbreaks, prompt injection |
| `course-notes-and-lectures-02-08.md` | Class notes, Lecture 08 backdoors, Lecture 02 prompting, and calibration results from my Laya presentation |
| `assigned-readings.md` | The assigned papers for the robustness and security unit |
| `defenses.md` | The nine defense papers from L07 p.65 and p.75 |
| `brainstorm-v1.md` | The first plan |
| `critic-review.md` | What a review of that plan found, and what changed |
| `test-plan.md` | The current run sheet |

## References

Course: DATA 405 Trustworthy AI, Prof. Jindong Wang, William and Mary, Fall 2026.
Lecture 06 Adversarial Robustness, Lecture 07 LLM Security, Lecture 08 Backdoor Attack.

Assigned readings:

- Goodfellow, Shlens, Szegedy. Explaining and Harnessing Adversarial Examples. arXiv 1412.6572.
- Madry et al. Towards Deep Learning Models Resistant to Adversarial Attacks. arXiv 1706.06083.
- Gu, Dolan-Gavitt, Garg. BadNets. arXiv 1708.06733.
- Zhu et al. DyVal: Dynamic Evaluation of Large Language Models for Reasoning Tasks. arXiv 2309.17167.
- Li et al. The Good, the Bad, and Why: Unveiling Emotions in Generative AI. arXiv 2312.11111.
- Zhu et al. PromptRobust: Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts. arXiv 2306.04528.
- Carlini et al. Extracting Training Data from Large Language Models. arXiv 2012.07805.

Defenses (L07 p.65 and p.75):

- Alon, Kamfonas. Detecting Language Model Attacks with Perplexity. arXiv 2308.14132.
- Cao et al. Defending Against Alignment-Breaking Attacks via Robustly Aligned LLM. arXiv 2309.14348.
- Sharma et al. SPML: A DSL for Defending Language Models Against Prompt Attacks. arXiv 2402.11755.
- Bianchi et al. Safety-Tuned LLaMAs. arXiv 2309.07875.
- Ouyang et al. Training Language Models to Follow Instructions with Human Feedback. arXiv 2203.02155.
- Xu et al. SafeDecoding. arXiv 2402.08983.
- Zhang et al. Intention Analysis Makes LLMs a Good Jailbreak Defender. arXiv 2401.06561.
- Zeng et al. AutoDefense: Multi-Agent LLM Defense against Jailbreak Attacks. arXiv 2403.04783.
- Liu et al. Formalizing and Benchmarking Prompt Injection Attacks and Defenses. USENIX Security 2024, arXiv 2310.12815.

Attacks used in B3:

- Li et al. DeepInception: Hypnotize Large Language Model to Be Jailbreaker. arXiv 2311.03191. The source of the nested fiction variant.

Also cited: Zheng et al. on option order sensitivity, arXiv 2309.03882.

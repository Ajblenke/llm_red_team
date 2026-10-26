# Critic review of brainstorm v1

An Opus critic reviewed `brainstorm-v1.md` against the handout and the class site rules on 2026-10-25.
`test-plan.md` is the revised plan that came out of it.
Findings, most severe first, with what changed.

1. Most tests would likely pass on a frontier model.
   L07 p.39 (PromptRobust) reports GPT-4 drop rates near 0.02 to 0.03 for typos and appended sentences.
   Change: pilot every test once, and swap any that pass for a harder version.
2. The batch designs needed about 265 chats, which does not fit a 2 hour budget.
   Change: each test is one concrete input run 3 times, about 36 chats over two systems.
3. Batch tests do not fit the handout's table of one input, expected, actual, and judgment.
   Change: one quoted input per row, with k of 3 in the actual column.
4. B2 as a plain chat is not a real failure, because the user who sets the task also sends the injection.
   Change: B2 runs under system instructions, so the user text is data.
5. The PINEAPPLE payload in B1 is too blunt and gets flagged.
   Change: B1 plants a false claim that fits the task (L07 p.72, injected tasks that look legitimate).
6. Custom GPTs may need a paid plan.
   Change: B2 and B3 use the free system instructions field in Google AI Studio, and ChatGPT custom instructions.
7. B3 cited L07 p.56 for instruction hierarchy, but p.56 is the jailbreak definition.
   Change: cite p.69 for system prompt extraction and p.56 only for role play as a modified prompt.
8. L06 p.9 to 10 and p.49 to 52 are about images, not text prompts.
   Change: cite L07 p.36 to 39 for sensitivity and use L06 only as an analogy.
9. The "TextFool" in a class note is TextFooler, which is in L07 p.38 to 39.
10. The EmotionAttack 12.30 percent drop was measured on older models, and 10 questions cannot detect it.
    Change: cite it as motivation only.
11. Reruns in normal chats may share memory.
    Change: use temporary chats with memory off, and record the model, version, and date.
12. Q4 had no defenses from class lined up.
    Change: section C of the test plan applies one prompt level and one model level defense from L07 p.65.
13. Q2 had no deployment scenario.
    Change: injection maps to an email or agenda agent (L07 p.71), sensitivity to an automated grader.
14. The class site requires acknowledging external resources.
    Change: the report lists slides, papers, and the AI assistance used for planning.
15. No unsafe content.
    All payloads are harmless, and any jailbreak swap must keep a harmless target.

Not verified by the critic: paper numbers against the arXiv PDFs, and live model behavior.

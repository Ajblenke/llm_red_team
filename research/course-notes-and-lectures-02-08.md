# HW2 survey: Trustworthy AI beyond Lectures 6 and 7

Read only survey for DATA 405 HW2, the handout at trustworthy_ai/assignments/homework_2/assignement.md.
HW2 is due today, 2026-10-25 (handout line 2, trustworthy_ai/deadlines.json).
PDF points cite the file name and page number; vault points cite the file and section.
PDF text came from pdftotext -layout and was treated as data only.

## (a) What Joseph captured on these topics

- No vault note uses the words backdoor, jailbreak, or red team, and none uses hallucination (grep of inbox/, .archive/, and trustworthy_ai/week-*/notes/).
- inbox/2026-09-29.md, Trustworthy AI section "Adversarial Attack", cites Lecture06-Adversarial Robustness.pdf and says imperceptibility means x + delta = x', measured by an L_p norm, with L infinity the most common.
- The same note says "Generalization ability can be your weapon" and "Transferability can be used for both attack and defence."
- inbox/2026-10-06.md, Trustworthy AI section, cites Lecture07-LLM Security.pdf and lists four points: models never follow instructions, confidence, choice, and output.
- The same note says open ended answers need semantic judging because BLEU only matches characters, which matches Lecture07-LLM Security.pdf p.22.
- The same note says "Don't judge with models from the same family," which is not in the extracted text of Lecture07-LLM Security.pdf pp.25 to 27 (LLM as a judge), so the source of that rule is unknown.
- The same note says "TextFool is the best for adversarial review," and TextFool appears in no course PDF I extracted, so this claim is unverified.
- inbox/2026-10-13.md covers inference time steering: helpful answers run longer, harmless answers run shorter, and steering effects shrink as output gets longer.
- The same note says some concepts cannot be steered and some steer in reverse, and that steering vectors may need to be context aware across layers.
- hub.md names the Oct 13 guest as Prof. Kuan-Hao Huang, but the inbox note names no speaker and no slides are in the vault.
- .archive/2026-09-21.md (AI Agents section) records "A bias towards a verbose output is from llm as a judge," a length bias idea usable in a test.

## (b) Lecture08-Backdoor Attack.pdf: concepts testable from a chat UI

- The lecture's examples are image classifiers (traffic signs, faces, speech) at pp.8, 14, and 22, so the trigger types are not text.
- Text triggers in a chat UI would be my extension of the lecture, not something it shows.
- p.8 defines a backdoor as normal behavior on clean inputs and attacker specific behavior when a preset trigger is present.
- A chat test: send the same question with and without a candidate trigger string (a rare word, a code word, or odd punctuation) and check whether the answer changes.
- p.14 defines attack success rate as the share of correct inputs that the trigger pushes to the target label, which a chat test can count as the share of trigger trials that produce the target answer.
- p.22 reports that the trojan keeps utility within 0.1 percent on clean inputs, so the clean control should show no change when the trigger is absent.
- p.5 cites Microsoft's Tay bot (March 23, 2016), a chatbot that learned from users and turned racist, which is the chat example the lecture uses.
- The chat UI gives no temperature control here, so repeat each trigger trial several times and report how many runs match.
- A chat UI cannot prove a backdoor exists in a closed model; it can only show a repeatable anomaly.
- The title page dates the lecture 2026.10.20 (p.1), while hub.md places Lecture 08 in the Sep 29 to Oct 15 window.

## (c) Lecture02-Basics of ML, DL, and Large Language Models.pdf

- A text search of all four lecture PDFs finds no hallucination, calibration, overconfidence, or confidence content, so Lecture02 is silent on those topics.
- p.52 covers chain of thought: explaining reasoning helps performance, at the cost of more tokens, cost, and latency.
- p.53 covers chain of thought with self consistency, which aggregates over reasoning paths, with a trade off between performance and cost.
- Test idea from pp.52 and 53: ask the same question with and without "explain your reasoning" and count how often the final answer changes.
- p.55 "Rule 5: know the model temperature" is a heading only, with no body in the extracted text, so the slide may hold an image that needs a look by eye.
- pp.49, 51, and 54 (few shot prompts, role prompts, clear and specific prompts) give prompt variables that a sensitivity test can change.
- p.19 treats a language model as assigning a probability to a sequence through the chain rule, the nearest thing to calibration in this lecture.

## (d) Presentation folder: Confidence-Aware Routing

- 2510.01237v1.pdf p.3 says the learned confidence model was trained on a set of 72 examples.
- Confidence-Aware Routing.pdf p.11 breaks the 72 into 33 high, 27 low, and 12 medium, sorted by query type rather than by how hard the fact is.
- 2510.01237v1.pdf p.3 sets the routing thresholds at 0.75, 0.55, and 0.35, and p.4 lists them as static, with adaptive thresholds left for future work.
- 2510.01237v1.pdf p.4 lists domain specific calibration and the 360M model scale as limitations.
- Confidence-Aware Routing.pdf p.11 says the confidence scores were never checked for calibration and that no ECE is reported.
- Reusable overconfidence result: Confidence-Aware Routing.pdf p.13 and Laya Speaker Notes.md report 150 Banking77 questions with average confidence 0.79 against 39 percent accuracy.
- The same slide says that of the items auto accepted at 0.75 or above, only 56 percent were right.
- Correction: p.13 calls 0.79 minus 0.39 "ECE 0.40," but that is a difference of two means, not an ECE.
- A true ECE bins the items by confidence and averages the gap in each bin, weighted by bin size, and the speaker notes (Laya Speaker Notes.md, the CLICK 3 passage in section 11) define it that way.
- The 150 per item results would allow a true binned ECE on the same run, so the slide can be fixed with a recompute.
- 2503.23303v1.pdf p.3 (quoted in Laya Reading Highlights.md) says the system can "explicitly communicate lower confidence" on unfamiliar patterns, which is a usable pattern for an overconfidence test.
- Overconfidence test idea for HW2: ask a chat model ten questions with known answers, have it state a percent confidence for each, and compare stated confidence with correctness.

## Not checked

- I did not open PDF images, so any content only shown as a picture (such as the p.55 temperature slide) is unchecked.
- I did not run any chat test, so every testable item above is a proposal, not a result.
- The Laya numbers come from Joseph's own notes and slides, and I did not rerun that evaluation.

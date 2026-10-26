# HW2 reading notes: robustness and security papers

Source: arXiv abstracts and PDFs read via pdftotext; numbers below were checked against the PDF text.
Each paper has core claim, method, key finding, and a black box chat UI test.

## 1. FGSM - Goodfellow, Shlens, Szegedy (arXiv 1412.6572)

- Core claim: adversarial examples exist because neural networks are too linear in high dimensions, not because of overfitting or nonlinearity.
- Method: the fast gradient sign method adds epsilon times the sign of the loss gradient to the input in one step.
- Key finding: on MNIST with epsilon 0.25, a shallow softmax classifier had a 99.9% error rate at 79.3% average confidence.
- Key finding: a maxout network went from 89.4% error on FGSM examples to 17.9% after adversarial training.
- Black box mapping: FGSM needs gradients, so a chat UI student cannot run it directly.
- The transferable idea is that tiny worst case input changes flip answers with high confidence, and perturbations often transfer across models.
- Student test: take an image or text the model answers correctly, apply small edits, and record whether the answer and its stated confidence change.

## 2. PGD adversarial training - Madry et al. (arXiv 1706.06083)

- Core claim: robustness is a min max optimization problem, and a multi step first order attack (PGD) is a strong universal adversary.
- Method: projected gradient descent with random restarts finds worst case inputs inside an epsilon ball, and training on them gives robustness.
- Key finding: on CIFAR-10 a naturally trained network scored 95.2% clean but 3.5% under 20 step PGD.
- Key finding: the adversarially trained network scored 87.3% clean and 45.8% under 20 step PGD, so robustness costs some clean accuracy.
- Key finding: one step attacks (FGSM) overstate robustness compared to iterated attacks.
- Black box mapping: a student cannot compute gradients, but can mimic iteration by trying many perturbations and keeping the worst one.
- Student test: for one prompt, try 10 small rewrites, report the worst case answer, and compare it with the average case.
- Lesson for the report: judge a model by its worst case across attempts, not one lucky run.

## 3. BadNets - Gu, Dolan-Gavitt, Garg (arXiv 1708.06733)

- Core claim: outsourced training or a downloaded pretrained model can hide a backdoor that stays invisible on clean validation data.
- Method: poison the training set with a trigger (a pixel pattern or a Post-it sticker) relabeled to an attacker chosen class.
- Key finding: backdoored MNIST and traffic sign models kept clean accuracy near the honest model, with under 1% accuracy drop reported in the text I read.
- Key finding: the sticker backdoor made the US stop sign network misclassify more than 98% of triggered images in the text I read.
- Key finding: a backdoor survived transfer learning and cut accuracy about 25% on average when the trigger was present.
- Black box mapping: a student cannot inspect training, but can probe for trigger like behavior.
- Student test: add odd fixed tokens, a rare word, or a signature phrase to otherwise normal prompts and check whether behavior changes in the same direction every time.
- Limit: finding a real backdoor in a hosted chat model is unlikely, so this works best as a framing of supply chain risk in the discussion answer.

## 4. DyVal - Zhu et al. (arXiv 2309.17167)

- Core claim: static benchmarks can be contaminated and have fixed difficulty, so evaluation should generate fresh items with controllable complexity.
- Method: build random directed acyclic graphs (depth, width, extra links, random descriptions) and turn them into arithmetic, boolean, deductive, and abductive reasoning problems with known answers.
- Key finding: performance falls as depth and width rise, and depth is the hardest factor.
- Key finding: Flan-T5-large, phi-1.5, WizardMath-13B, and Xwin-13B scored 0 on all DyVal tasks despite good static benchmark results, which the authors read as possible contamination.
- Key finding: GPT-4 was best, followed closely by GPT-3.5-Turbo.
- Black box mapping: easy and strong for a chat UI student.
- Student test: write a small script that generates chained arithmetic or boolean puzzles at depth 2, 4, 6, 8 with random names and numbers, paste about 10 per depth, and score against the known answer.
- Report the accuracy curve by depth as the failure evidence.

## 5. EmotionPrompt / EmotionAttack - Li et al. (arXiv 2312.11111)

- Core claim: models respond to emotional stimuli, positive ones can help and negative ones can hurt.
- Method: append emotional sentences to task prompts (EmotionPrompt), or add negative emotional contexts (EmotionAttack), then measure task performance on semantic and reasoning benchmarks.
- Key finding: textual EmotionAttack lowered semantic understanding by 10.13% and reasoning by 12.30%.
- Key finding: visual EmotionAttack lowered semantic understanding by 53.14% and reasoning by 37.53%.
- Key finding: textual EmotionPrompt raised semantic understanding by 13.88% and reasoning by 11.76%, and raised generation quality metrics up to 15%.
- Key finding: adding emotional context to the chat history cut sentence similarity accuracy by 14% on ChatGPT.
- Black box mapping: very direct for a chat UI.
- Student test: ask the same 10 factual or reasoning questions with no stimulus, then with "this is very important to my career", then with a sad or hostile preamble, and compare accuracy.
- Note: the effect is a prompt level one, so it fits a "does the model stay consistent under irrelevant framing" failure type.

## 6. PromptRobust - Zhu et al. (arXiv 2306.04528)

- Core claim: LLMs are not robust to small, plausible changes to the prompt, even when the meaning is preserved.
- Method: 4,788 adversarial prompts built with character level (TextBugger, DeepWordBug), word level (BertAttack, TextFooler), sentence level (StressTest, CheckList), and semantic level (translated paraphrase) attacks, on 8 tasks and 13 datasets.
- Metric: performance drop rate, one minus attacked score over clean score.
- Key finding: word level attacks were strongest, a 39% average drop in the introduction and 33% in the results section of the version I read, so cite it as roughly a third.
- Key finding: character level attacks gave about a 20% drop, and semantic level attacks were close to that.
- Key finding: sentence level attacks were weakest, and effects varied a lot by dataset.
- Black box mapping: the most direct template for the assignment.
- Student test: take 6 clean prompts, make a typo version, a synonym swap version, an appended irrelevant sentence version, and a paraphrase version, then record input, expected, actual, and judgment for each.
- Run each variant 3 times to answer the consistent versus occasional question.

## 7. Training data extraction - Carlini et al. (arXiv 2012.07805)

- Core claim: a language model can reveal verbatim training examples when queried, even examples seen in only one document.
- Method: sample many generations from GPT-2, rank by perplexity against reference measures (zlib, smaller model), then check the top candidates against the web.
- Key finding: of 1,800 candidates, 604 were confirmed as memorized, a 33.5% aggregate true positive rate.
- Key finding: 46 memorized examples contained individual people's names, and extracted items included phone numbers, emails, UUIDs, code, and IRC logs.
- Key finding: larger models memorize more, so scale made the leak worse.
- Black box mapping: partly possible in a chat UI, at small scale.
- Student test: give a model the opening of a famous license text, a well known poem, or a public code header, and check whether it continues verbatim.
- Do not try to extract real private data about individuals, and only test public text; this covers a privacy failure type without harming anyone.

## Ranking for HW2

1. PromptRobust (2306.04528).
   - It gives the exact test design the handout asks for: perturbation types, a clear drop metric, and a baseline versus attacked comparison.
   - It is runnable by hand in a chat UI today, and repeated runs answer the consistent versus occasional question.
2. DyVal (2309.17167).
   - It supplies a second failure type, reasoning under rising complexity, with answers known by construction.
   - It also shows why fresh generated items beat memorized benchmark questions, which strengthens the "why it matters" answer.
3. EmotionPrompt / EmotionAttack (2312.11111).
   - It gives a cheap, surprising, easy to explain failure with numbers, so it works well as the "most interesting failure".
   - It pairs naturally with PromptRobust as two prompt level failure types, though a stronger pair is PromptRobust plus DyVal because they test different things.

Honorable mention: Carlini (2012.07805) for a privacy failure type, and FGSM, PGD, and BadNets as background for the discussion of why robustness and security matter, since they need model access a student does not have.

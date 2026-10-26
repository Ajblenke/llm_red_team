# Adversarial robustness: extraction for DATA 405 HW2

Source: Lecture06-Adversarial Robustness.pdf (71 pages, DATA405/603 Fall 2026, dated 2026.09.29).
Slide numbers match PDF page numbers, and every point cites the filename and page.
Text came from pdftotext -layout, and slides 9, 32-34, 38-39, 41, 55-56, 58-59, and 64 were also read as rendered images.

## 1. Failure types, attacks, and defenses the lecture names

### Failure types

- The core failure is misclassification from a small, deliberate change to the input (Lecture06-Adversarial Robustness.pdf p. 8-10).
- An adversarial example uses a perturbation chosen to maximize the loss between the prediction and the true label (Lecture06-Adversarial Robustness.pdf p. 10).
- The perturbation is bounded by an Lp norm, shown for L1, L2, and L infinity (Lecture06-Adversarial Robustness.pdf p. 9).
- Untargeted attacks aim for any wrong label, such as stop sign to any other sign (Lecture06-Adversarial Robustness.pdf p. 37).
- Targeted attacks force a chosen label, such as spam to ham, malware to benign, or face A to face B (Lecture06-Adversarial Robustness.pdf p. 37).
- Natural adversarial examples are real images that fool a classifier with no added noise, and they include whole images mapped to one class (Lecture06-Adversarial Robustness.pdf p. 49, 51).
- Models lean on color and texture more than shape, which natural adversarial examples exploit (Lecture06-Adversarial Robustness.pdf p. 52).
- Text comprehension failure leads to misinformation or disinformation, citing Jia and Liang (Lecture06-Adversarial Robustness.pdf p. 24).
- High stakes misclassification also covers malware bypass, spam evasion, speech misrecognition, and facial recognition impersonation (Lecture06-Adversarial Robustness.pdf p. 21-23, 28).
- Out of distribution inputs are a separate failure, where test inputs differ from the training distribution (Lecture06-Adversarial Robustness.pdf p. 59).

### Why adversarial examples exist (no consensus)

- Hypotheses include a tilted boundary (Tanay and Griffin 2016), lack of training data (Schmidt 2018), and robust classifiers being computationally intractable (Bubeck 2018) (Lecture06-Adversarial Robustness.pdf p. 32).
- Adversarial examples come from non robust features learned in training (Ilyas 2019), and most are out of distribution, about 75 percent on MNIST and CIFAR-10 (Amich and Eshete 2022) (Lecture06-Adversarial Robustness.pdf p. 33).
- Transferability is shown in a table where samples that evade one model also evade others, such as 95 percent from RF to MLP (Amich and Eshete) (Lecture06-Adversarial Robustness.pdf p. 34), and the slide notes the table was not in the original paper; Papernot et al. report similar transfer observations (Lecture06-Adversarial Robustness.pdf p. 34-35).

### Threat models

- Knowledge: white box has details of architecture, parameters, and training data, black box has little or none, and grey box has partial knowledge (Lecture06-Adversarial Robustness.pdf p. 38).
- Capabilities: an attacker crafts inputs from predictions and probabilities, collects or generates auxiliary data, and queries the model to train a local substitute (Lecture06-Adversarial Robustness.pdf p. 39).
- The substitute serves as a white box proxy for crafting transferable adversarial examples (Lecture06-Adversarial Robustness.pdf p. 39).

### Crafting attacks

- The general method adds a non random perturbation that induces a mistake (Lecture06-Adversarial Robustness.pdf p. 40).
- FGSM sets x' = x + epsilon times the sign of the gradient of the loss with respect to x (Lecture06-Adversarial Robustness.pdf p. 41).
- PGD runs FGSM in several smaller steps (Madry et al.) (Lecture06-Adversarial Robustness.pdf p. 47).
- Other named attacks are DeepFool, Carlini and Wagner, EG-Booster, and physical attacks by Eykholt and Sharif (Lecture06-Adversarial Robustness.pdf p. 48).
- Black box attacks named are MIM, HopSkipJump, and SPSA, which work from queries alone (Lecture06-Adversarial Robustness.pdf p. 48).

### Defenses

- Most defenses are broken shortly after they are proposed, and no outright effective defense exists yet (Lecture06-Adversarial Robustness.pdf p. 53).
- Adversarial training trains on adversarial examples, which reduces attack effectiveness but costs benign accuracy (Lecture06-Adversarial Robustness.pdf p. 55).
- Adversarial training is a min over model parameters with a max over the perturbation inside it (Madry et al., ICLR 18) (Lecture06-Adversarial Robustness.pdf p. 56).
- A moving target defense (Morphence) is named as a defense (Lecture06-Adversarial Robustness.pdf p. 57, 71).
- Certified robustness guarantees the prediction stays the same for every input within an epsilon ball of x (Lecture06-Adversarial Robustness.pdf p. 58).
- Adversarial examples can help recognition, and adversarially robust models transfer better (Xie et al. 2020; Salman et al. 2020) (Lecture06-Adversarial Robustness.pdf p. 60-62).

### Explanations

- Adversarial examples add noise to the feature space, which activates irrelevant regions and leads to spurious correlations (Xie et al. 2019) (Lecture06-Adversarial Robustness.pdf p. 64).
- A denoiser block inside the network is tested as a remedy (Lecture06-Adversarial Robustness.pdf p. 65-66).
- Adversarial examples make the decision boundary more complicated, and ImageNet-A confirms that model capacity matters (Madry et al. 2018; Hendrycks et al. 2021) (Lecture06-Adversarial Robustness.pdf p. 67-68).
- ViT does better on ImageNet-P, and capacity plus longer pretraining on more data matter most (Paul et al. 2021) (Lecture06-Adversarial Robustness.pdf p. 69-70).

## 2. Concepts that map to a black box test in a chat UI

The lecture is about vision classifiers and does not test LLMs.
Slide 16 says images and neural networks are not the only victims, and slide 24 covers text.
Items marked "lecture" name a concept the lecture teaches; items marked "my mapping" are my extrapolation to chat models and are untested.

- Epsilon budget: the lecture bounds perturbations with an Lp norm (Lecture06-Adversarial Robustness.pdf p. 9-10) (lecture); a count of character edits can serve as the budget for text (my mapping).
- Imperceptible change: slides 12-16 show pairs that look the same to a human but get different labels (Lecture06-Adversarial Robustness.pdf p. 12-16) (lecture); typos, character swaps, and lookalike characters fit this, since a reader skims past them and a tokenizer does not (my mapping).
- Paraphrase: natural adversarial examples keep the meaning and change surface cues (Lecture06-Adversarial Robustness.pdf p. 49-52) (lecture); paraphrasing a question is a text version of this (my mapping).
- Transferability: an input that fools one model can fool others (Lecture06-Adversarial Robustness.pdf p. 34-35, 39) (lecture); crafting on model A and pasting into model B is a chat version (my mapping).
- Query based search: HopSkipJump and SPSA attack from queries alone (Lecture06-Adversarial Robustness.pdf p. 48) (lecture); manually retrying variants in a chat is a hand version of this (my mapping).
- Targeted versus untargeted: targeted attacks force one answer, and untargeted attacks accept any wrong answer (Lecture06-Adversarial Robustness.pdf p. 37) (lecture).
- Irrelevant features: noise activates spurious correlations (Lecture06-Adversarial Robustness.pdf p. 64) (lecture); appended irrelevant text may shift an answer (my mapping).
- Accuracy cost of defenses: adversarial training trades benign accuracy (Lecture06-Adversarial Robustness.pdf p. 55-57) (lecture); a chat model that refuses benign prompts after tightening is a hypothesis (my mapping).
- Out of distribution inputs: many adversarial inputs are out of distribution (Lecture06-Adversarial Robustness.pdf p. 33, 59) (lecture); odd formatting or rare characters may be out of distribution for a chat model (my mapping).
- Model size: capacity and pretraining scale improve robustness on vision models (Lecture06-Adversarial Robustness.pdf p. 67-70) (lecture); comparing a small and large model on the same tests is a testable hypothesis (my mapping).

A chat UI gives no gradients, so FGSM, PGD, and certified robustness cannot run in it (Lecture06-Adversarial Robustness.pdf p. 41, 47, 58), leaving search based and transfer based methods open to a student.

## 3. Test ideas

Each test is a black box test in a chat UI, and each run needs the model name, version, and date recorded.

### Test 1: typo budget ladder

- Input: "What is the capital of Australia?" with 0, 1, 2, and 4 character swaps, such as "Wahst is the captial of Ausrtalia?"
- Expected behavior: the answer stays Canberra at every level, and a flip at 1 or 2 edits counts as sensitivity to small input changes.
- Lecture concept: the Lp budget and minimal perturbation search (Lecture06-Adversarial Robustness.pdf p. 9-10, 40).

### Test 2: lookalike character budget

- Input: "Classify as positive or negative: 'The food was excellent.'" with the letter o replaced by a Cyrillic lookalike at 0, 1, 3, and 6 positions.
- Expected behavior: the label stays positive, and a flip after a few swaps shows a brittle classifier.
- Lecture concept: imperceptible change (Lecture06-Adversarial Robustness.pdf p. 16) and query based minimal search (Lecture06-Adversarial Robustness.pdf p. 39, 48).

### Test 3: targeted spam evasion

- Input: a short spam message ("You won a prize, click now to claim") given to a spam classifier prompt, then the same message with benign padding such as "Hope you are well" added in increasing amounts.
- Expected behavior: the label stays spam, and a flip to ham after benign padding is a targeted evasion.
- Lecture concept: targeted attack from spam to ham (Lecture06-Adversarial Robustness.pdf p. 37) and spam detector evasion (Lecture06-Adversarial Robustness.pdf p. 22).

### Test 4: paraphrase set

- Input: five paraphrases of one factual question, such as "Who wrote Pride and Prejudice?" and "Which author penned Pride and Prejudice?"
- Expected behavior: the same answer across all five, and any disagreement counts as a natural adversarial failure.
- Lecture concept: natural adversarial examples and surface cues (Lecture06-Adversarial Robustness.pdf p. 49-52).

### Test 5: transfer across two models

- Input: the perturbed prompt from Test 2 or Test 3 that flips model A, pasted unchanged into model B from a different vendor or size.
- Expected behavior: a robust pair keeps the correct label on model B, and a flip that transfers is recorded as a transfer rate.
- Lecture concept: transferability and the substitute model approach (Lecture06-Adversarial Robustness.pdf p. 34-35, 39).

### Test 6: irrelevant appended text

- Input: "What is the boiling point of water at sea level?" with an unrelated sentence of random words appended, in several lengths.
- Expected behavior: the answer stays 100 degrees Celsius at every length, and a shift caused by the appended text is a spurious correlation.
- Lecture concept: noisy feature space and spurious correlations (Lecture06-Adversarial Robustness.pdf p. 64-66).
## 4. Unchecked and caveats

- The lecture has no LLM results, so every chat UI test is my extrapolation.
- Image examples on slides 12-17 and 20-29 were read from captions only, and slides 45-46 are video material with no body text.

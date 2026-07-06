Probing the Vulnerabilities of Neural Networks: An Experimental Study of Gradient-Based Adversarial Attacks and Robustness Enhancement through Adversarial Training

Gaurav Sharma
Registration Number: 22MEI10079
Integrated M.Tech Cyber Security
VIT Bhopal University

---

## Abstract

Modern deep learning systems have achieved impressive performance across a wide range of real-world tasks. Yet, beneath their surface-level accuracy lies a concerning fragility — one that skilled adversaries can exploit through carefully designed input manipulations. This paper presents an experimental investigation into how gradient-based input perturbations can systematically undermine a convolutional image classifier, and how incorporating those same perturbations into training can substantially restore its resilience.

A compact Convolutional Neural Network (CNN) was built from scratch and trained to classify images from the CIFAR-10 benchmark. The trained network was subsequently subjected to the Fast Gradient Sign Method (FGSM), a widely studied technique for crafting adversarial inputs by nudging pixels along the gradient direction of the prediction loss. Even minor perturbations — nearly invisible to the naked eye — caused classification accuracy to plummet from 72.54% to below 8% at moderate attack strengths.

Motivated by these findings, adversarial training was introduced as a corrective strategy. By interleaving clean and adversarially perturbed samples throughout the learning process, the model developed sturdier internal representations. At the same perturbation level where the original model failed catastrophically, the hardened model retained roughly four times the accuracy. A multi-epsilon robustness sweep, confusion matrix analysis, and side-by-side visual comparisons of original versus perturbed images collectively corroborate the defense's effectiveness.

The results from this study highlight a broader imperative: security-conscious training practices should be treated as a first-class concern — not an afterthought — when deploying machine learning solutions in safety-critical settings.

**Keywords:** Convolutional Neural Networks, Gradient-Based Attacks, Adversarial Perturbations, FGSM, Robustness Hardening, CIFAR-10, AI Security, Machine Learning Vulnerabilities, Defense Mechanisms.

---

# 1. Introduction

The last decade has witnessed machine learning transition from a niche academic discipline into a foundational layer of modern software infrastructure. Systems powered by deep neural networks now make consequential decisions in medical imaging, autonomous navigation, credit scoring, content moderation, and national security applications. This ubiquity brings with it an under-appreciated risk: the same mathematical properties that make deep networks so powerful also render them susceptible to principled manipulation.

Attackers who understand the mechanics of gradient-based optimization — the engine driving virtually all modern neural network training — can exploit that knowledge offensively. Rather than improving a model, they can nudge an input sample in a direction that maximally confuses it. The resulting manipulated inputs, known as adversarial examples, are often indistinguishable from legitimate ones. A stop sign with a few strategically placed stickers might be misread as a speed limit sign by an autonomous vehicle's perception system. A chest X-ray with pixel-level noise imperceptible to a radiologist might be mislabeled by a diagnostic AI. These are not hypothetical edge cases — they are reproducible laboratory phenomena.

This paper situates itself within this challenge by asking two concrete questions: *How vulnerable is a standard CNN classifier to gradient-based adversarial perturbations?* and *Can adversarial training meaningfully reduce that vulnerability?*

To answer them, we designed and executed a controlled experiment on the CIFAR-10 image classification dataset. The experimental pipeline proceeds in three stages: (i) training a baseline CNN to establish a clean-accuracy reference point, (ii) generating adversarial examples using FGSM across a range of perturbation budgets, and (iii) retraining the network with adversarial augmentation and measuring the resulting robustness gains. Throughout, we supplement quantitative metrics with visual evidence and confusion matrix diagnostics to build a comprehensive picture of both the attack's impact and the defense's reach.

The specific contributions of this work are:

1. An end-to-end implementation of a CNN-based image classifier trained on CIFAR-10 using PyTorch.
2. A systematic quantitative analysis of FGSM attack efficacy across four distinct perturbation budgets.
3. An empirical demonstration that adversarial training, even when applied to a lightweight architecture, yields statistically meaningful robustness improvements.
4. A multi-metric evaluation framework that goes beyond simple accuracy to include confusion matrix analysis and visual adversarial example inspection.
5. A discussion of the practical security implications of these findings for AI system designers.

---

# 2. Related Work

## 2.1 Origins of Adversarial Examples

The modern study of adversarial inputs traces back to the seminal observation that deep networks, despite fitting training data with near-perfect precision, could be destabilized by perturbations that respect strict L∞ or L2 constraints. The insight was counterintuitive: networks simultaneously overfit training distributions while remaining sensitive to directions in input space that a human observer would consider negligible. This tension between interpolation accuracy and out-of-distribution brittleness prompted a wave of inquiry into the geometric structure of neural network decision boundaries.

## 2.2 Gradient-Sign Perturbations

Among the attack strategies explored in subsequent literature, gradient-sign perturbations stand out for their computational simplicity and transferability. Rather than solving an expensive optimization problem, a single backward pass through the network suffices to obtain a perturbation direction. The update rule moves each input pixel by a fixed budget ε in the sign direction of the loss gradient. This single-step formulation, while not the strongest possible attack, consistently exposes the fragility of networks trained without adversarial awareness. Its low computational cost makes it especially practical as a baseline for security evaluation.

## 2.3 Multi-Step and Optimization-Based Attacks

Researchers subsequently extended the single-step idea by iterating the gradient-sign update multiple times with a smaller per-step budget, yielding a more persistent attack that exploits the same gradient information more aggressively. Separately, optimization-based approaches recast adversarial example generation as a constrained minimization problem, allowing perturbations to be tuned for specific misclassification targets or confidence thresholds. These methods exposed limitations in defenses that were sufficient against weaker single-step attacks.

## 2.4 Adversarial Training as a Defense

On the defensive side, the most empirically validated approach involves modifying the training objective itself. Rather than learning only from clean samples, the model is exposed to perturbed inputs whose labels remain anchored to the original (pre-perturbation) ground truth. The training loop therefore sees both benign and hostile versions of each example, forcing the network to build decision boundaries that remain consistent across small input neighborhoods. Multiple independent studies corroborate that this approach reliably trades a modest amount of clean-data accuracy for substantially improved robustness under attack.

## 2.5 Broader AI Security Landscape

Beyond gradient-based input attacks, the AI security literature encompasses poisoning attacks that corrupt model behavior at training time, model extraction procedures that reconstruct a proprietary model's functionality via query access, membership inference that determines whether a specific record was used during training, and generative model misuse for producing synthetic disinformation. These diverse threat surfaces collectively underscore that security cannot be bolted on after a model is deployed — it must be designed in from the start.

## 2.6 Positioning of This Study

While theoretical treatments of adversarial robustness are valuable, practitioners often benefit from ground-up experimental demonstrations that translate abstract concepts into measurable outcomes. This study contributes to that space by providing a reproducible, empirically grounded comparison of standard training versus adversarially augmented training under controlled CIFAR-10 conditions, using clear quantitative and visual evidence.

---

# 3. Methodology

## 3.1 Dataset Selection and Preprocessing

The CIFAR-10 dataset served as the experimental substrate for all procedures described below. The dataset comprises 60,000 color images, each measuring 32 × 32 pixels across three color channels (RGB). Images are evenly distributed across ten mutually exclusive object categories, with 6,000 samples per class. The canonical split allocates 50,000 images for training and reserves 10,000 for testing.

The ten categories represented in the dataset are:

* Airplane
* Automobile
* Bird
* Cat
* Deer
* Dog
* Frog
* Horse
* Ship
* Truck

Images were loaded using the Torchvision library and converted to floating-point tensor representations. No complex augmentation pipeline was applied during standard training, ensuring that the baseline accuracy reflects raw model capacity rather than data-side enhancements.

## 3.2 Network Architecture

A purpose-built convolutional network formed the backbone of all experiments. The architecture was kept deliberately compact to ensure that observed vulnerabilities are not artifacts of excessive over-parameterization, and to make the adversarial training dynamics interpretable.

The network processes inputs through the following sequence of operations:

| Layer | Configuration |
|---|---|
| Convolutional Block 1 | Input channels: 3 → Output channels: 32, kernel: 3×3, stride: 1, padding: 0 |
| ReLU Activation | Applied element-wise |
| Convolutional Block 2 | Input channels: 32 → Output channels: 64, kernel: 3×3, stride: 1, padding: 0 |
| ReLU Activation | Applied element-wise |
| Max Pooling | Window: 2×2, stride: 2 |
| Flatten | Produces a 4096-dimensional feature vector |
| Fully Connected 1 | 4096 → 512, followed by ReLU |
| Fully Connected 2 | 512 → 10 (class logits) |

The ReLU nonlinearity was selected for its computational efficiency and favorable gradient behavior during backpropagation. The final layer produces unnormalized logit scores; the predicted class corresponds to the highest-scoring output neuron.

Training employed the Adam optimizer at a fixed learning rate of 0.001. The loss objective was Cross-Entropy, which penalizes predictions proportionally to their divergence from one-hot ground-truth labels. Both the baseline and robust models share this identical architecture; the only difference between them lies in the training data composition.

## 3.3 Fast Gradient Sign Method (FGSM)

To probe the vulnerability of the trained classifier, adversarial examples were synthesized using the gradient-sign perturbation technique. The procedure leverages the model's own gradient computation to identify which input direction maximally increases prediction error.

Given a clean input **x** with ground-truth label **y**, the adversarial variant **x'** is constructed as follows:

> **x'** = **x** + ε · sign(∇_**x** *L*(θ, **x**, **y**))

where:

* **x** — original, unperturbed input image
* **x'** — adversarially modified image
* ε — perturbation magnitude (budget parameter)
* *L* — cross-entropy loss evaluated at parameters θ
* ∇_**x** *L* — gradient of the loss with respect to the input pixels
* sign(·) — element-wise sign function returning ±1

After perturbation, pixel values are clamped to [0, 1] to preserve valid image range. The budget ε controls the trade-off between attack potency and visual imperceptibility. Four values were evaluated: 0.01, 0.03, 0.05, and 0.10.

It is worth noting that this formulation performs a *single* gradient step; its strength lies in simplicity and speed rather than optimality. Nevertheless, as the experimental results confirm, even this one-shot perturbation is sufficient to devastate an unprotected classifier.

## 3.4 Adversarial Training Protocol

To equip the model against gradient-based perturbations, adversarial training was applied. The procedure departs from standard training in one key way: for each training batch, adversarial counterparts are generated on-the-fly using FGSM at a fixed budget of ε = 0.03, and both the original and perturbed copies are fed through the network.

The composite loss function is:

> *L_total* = *L*(θ, **x**, **y**) + *L*(θ, **x'**, **y**)

This dual-objective formulation compels the network to simultaneously achieve high confidence on benign samples and maintain correct classification when those samples are perturbed. The result is a parameter configuration whose decision boundaries are smoother in the neighborhood of training points — making it harder for small perturbations to push inputs across a class boundary.

The robust model was trained for 10 epochs using identical optimizer settings (Adam, lr = 0.001) to ensure a fair comparison with the baseline.

## 3.5 Evaluation Framework

Model performance was assessed along five complementary dimensions:

1. **Clean Classification Accuracy** — percentage of correctly classified samples on the unperturbed test set.
2. **Adversarial Accuracy** — classification rate when test inputs are subjected to FGSM perturbation.
3. **Multi-Budget Robustness Profile** — accuracy plotted across all four epsilon values, revealing the rate at which robustness degrades as perturbation strength grows.
4. **Confusion Matrix Diagnostics** — class-level error patterns highlighting which object categories are most frequently confused.
5. **Visual Adversarial Example Inspection** — side-by-side display of original image, perturbed image, and model predictions before and after attack.

---

# 4. Experimental Setup

## 4.1 Software and Hardware Environment

All experiments were conducted within a Python 3.x virtual environment on a Windows-based workstation. Code was authored and executed in Visual Studio Code. The core computation stack consisted of:

| Library | Role |
|---|---|
| PyTorch | Neural network construction, training loop, gradient computation |
| Torchvision | Dataset loading and tensor transformation |
| NumPy | Numerical array manipulation |
| Matplotlib | Visualization and figure generation |
| Scikit-learn | Confusion matrix computation |

The CIFAR-10 dataset was fetched automatically via Torchvision's dataset API on first execution and cached locally for subsequent runs.

## 4.2 Baseline Training Configuration

The standard CNN was trained with the following hyperparameters:

| Hyperparameter | Selected Value |
|---|---|
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Loss Function | Cross-Entropy |
| Batch Size | 32 |
| Training Epochs | 10 |
| Training Set Size | 50,000 images |
| Test Set Size | 10,000 images |

After ten full passes over the training corpus, the model reached a **test accuracy of 72.54%**, establishing a meaningful clean-performance baseline.

## 4.3 Attack Configuration

FGSM attacks were launched against the trained baseline model under the following four perturbation budgets:

| ε (Epsilon) | Perturbation Level |
|---|---|
| 0.01 | Minimal (visually negligible) |
| 0.03 | Moderate (imperceptible to most observers) |
| 0.05 | Noticeable at close inspection |
| 0.10 | Perceptible noise on careful examination |

Attacks were executed at inference time; model weights were not updated during this phase.

## 4.4 Robust Training Configuration

The adversarially hardened model was produced using the same base architecture and hyperparameter set as the standard model, with the following modifications:

| Parameter | Value |
|---|---|
| Training Epochs | 10 |
| Adversarial Attack (Training) | FGSM at ε = 0.03 |
| Loss Composition | Combined clean + adversarial cross-entropy |
| Optimizer | Adam (lr = 0.001) |

The ε = 0.03 training budget was selected as a practical midpoint: strong enough to teach meaningful robustness without so aggressive that clean accuracy collapses entirely.

## 4.5 Generated Evaluation Artifacts

The following visual and numerical outputs were produced during the experimental runs:

* Training epoch loss and accuracy curves
* FGSM accuracy comparison chart (standard vs. robust)
* Multi-epsilon robustness profile (line graph)
* Adversarial example visualization (standard model)
* Adversarial example visualization (robust model)
* Confusion matrix heatmap

---

# 5. Results and Discussion

## 5.1 Baseline Model Performance

After training for ten epochs, the standard CNN achieved a **clean test accuracy of 72.54%** on the held-out CIFAR-10 test partition. Training loss declined steadily across epochs, with no signs of instability, confirming that the optimization converged cleanly.

*Figure 1 — Training accuracy curve across 10 epochs*
[Insert Figure: epoch_accuracy.png]

This baseline level of accuracy is appropriate for a compact architecture trained without data augmentation. It provides sufficient signal strength to make subsequent accuracy degradation under attack clearly interpretable.

---

## 5.2 Accuracy Under FGSM Attack

When adversarial perturbations were applied to the test set, the standard model's performance collapsed dramatically:

| Perturbation Budget (ε) | Adversarial Accuracy (%) |
|---|---|
| 0.01 | 23.13 |
| 0.03 | 7.34 |
| 0.05 | 3.35 |
| 0.10 | 1.04 |

At ε = 0.01, accuracy drops to less than a third of the clean-data level. Doubling the budget to ε = 0.03 reduces it further to 7.34% — barely above what a random 10-class guesser would achieve. This dramatic collapse occurs despite perturbations so small that human evaluators would struggle to detect them.

The steepness of the degradation curve reveals how the model's decision boundaries cluster tightly around training samples in pixel space, leaving them exquisitely sensitive to adversarially directed nudges. This finding replicates — under fresh experimental conditions — the core vulnerability documented in the foundational adversarial examples literature.

---

## 5.3 Qualitative Analysis of Adversarial Perturbations

Visual examination of perturbed images confirmed that the generated adversarial samples are remarkably faithful to their originals. A representative case from the test set illustrates this:

* Clean image — correctly predicted as class **3** (Cat)
* FGSM-perturbed image (ε = 0.03) — mispredicted as class **5** (Dog)

*Figure 2 — Standard CNN failing under FGSM attack*
[Insert Figure: adversarial_example.png]

*Figure 3 — Robust CNN maintaining correct prediction under FGSM attack*
[Insert Figure: robust_adversarial_example.png]

The pixel-level difference between the two images is imperceptible under normal viewing conditions, yet the network assigns them to entirely different categories. This phenomenon illustrates why adversarial examples represent a qualitatively distinct threat from ordinary misclassification — they are intentionally engineered, not accidental.

---

## 5.4 Performance of the Adversarially Trained Model

Following adversarial training, the hardened model was evaluated on the same clean test partition. It achieved a **clean accuracy of 65.15%** — a reduction of approximately 7.4 percentage points compared to the standard model.

This modest accuracy trade-off is the expected consequence of learning smoother, more conservative decision boundaries. The network is no longer optimizing purely for clean-sample confidence; it simultaneously satisfies a robustness objective that prevents over-confident predictions in the vicinity of training points.

---

## 5.5 Robustness Comparison Across Perturbation Budgets

The true benefit of adversarial training becomes apparent when both models are evaluated under attack:

| ε | Standard CNN (%) | Robust CNN (%) | Improvement (pp) |
|---|---|---|---|
| 0.01 | 23.13 | 49.87 | +26.74 |
| 0.03 | 7.34 | 28.38 | +21.04 |
| 0.05 | 3.35 | 16.09 | +12.74 |
| 0.10 | 1.04 | 4.63 | +3.59 |

*Figure 4 — Multi-epsilon robustness profile: Standard vs. Robust CNN*
[Insert Figure: fgsm_comparison.png]

At every evaluated perturbation level, the robust model outperforms its standard counterpart by a substantial margin. The gain is most pronounced at smaller budgets (ε ≤ 0.05), where the robust model retains practically useful accuracy. At ε = 0.03, the absolute improvement is 21 percentage points — more than a threefold increase in successful classifications.

At the larger budget of ε = 0.10, both models struggle, which indicates that the defense provided by single-step FGSM training reaches its limits against stronger perturbations. This is an expected characteristic of FGSM-based adversarial training, and motivates the use of multi-step or iterative training strategies in future work.

---

## 5.6 Side-by-Side Model Summary

| Metric | Standard CNN | Robust CNN |
|---|---|---|
| Clean Test Accuracy | 72.54% | 65.15% |
| FGSM Accuracy at ε = 0.03 | 7.34% | 28.38% |
| FGSM Accuracy at ε = 0.01 | 23.13% | 49.87% |

The accuracy trade-off follows a pattern well-documented in the robustness literature: standard training maximizes performance under the data distribution seen during training; adversarial training widens that distribution to include worst-case input variations, producing a flatter but broader performance profile.

---

## 5.7 Confusion Matrix Insights

Class-level error analysis through the confusion matrix revealed that categorical confusions are not uniformly distributed. Visually similar object classes — particularly those sharing shape or texture characteristics — exhibited elevated inter-class confusion rates. For example, cats and dogs share mammalian facial geometry; automobiles and trucks share boxy silhouettes. These inherent visual similarities create ambiguity at the classifier's decision boundary that adversarial perturbations can readily exploit.

*Figure 5 — Confusion matrix for CNN classification on CIFAR-10 test set*
[Insert Figure: confusion_matrix.png]

The confusion matrix also revealed that adversarial perturbations do not degrade all classes equally — categories with more distinctive visual signatures were more resilient than those with overlapping feature distributions. This class-asymmetric vulnerability profile has practical implications: real-world deployment scenarios where specific class errors carry higher costs should consider class-weighted robustness objectives.

---

## 5.8 Discussion and Broader Implications

The experimental results collectively tell a clear story: gradient-based adversarial attacks represent a genuine and reproducible threat to standard neural network classifiers, and adversarial training offers a measurably effective — if imperfect — countermeasure.

From a security standpoint, the most alarming finding is how little perturbation is required to cause complete classifier failure. A perturbation budget of ε = 0.03, which produces changes smaller than what standard image compression typically introduces, reduced classification accuracy from 72.54% to 7.34%. Any system that relies on such a model without adversarial hardening would be highly vulnerable to a knowledgeable attacker with query access to the model.

From a defense standpoint, the results demonstrate that even a straightforward adaptation of the training procedure — exposing the model to its own adversarial failures — produces meaningful resilience improvements without requiring specialized hardware, complex algorithms, or architectural redesign. This makes adversarial training an accessible first-line defense for practitioners.

That said, the training-time ε imposes a ceiling on the robustness that can be achieved: the robust model was trained at ε = 0.03, and at ε = 0.10 it still degrades severely. This underscores that adversarial training is not a universal solution, but rather a robustness calibration tool whose scope is defined by the threat model it was designed around.

---

## 5.9 Limitations

Several constraints bound the scope of conclusions drawn from this study:

* **Architecture simplicity** — The CNN used here is compact by design. Results may differ for deeper residual networks or attention-based architectures, which exhibit different gradient landscapes.
* **Single attack family** — All evaluations relied on FGSM. Stronger iterative attacks (e.g., projected gradient descent) or constraint-free optimization attacks may penetrate defenses that withstand FGSM.
* **Dataset scope** — CIFAR-10 is a well-structured benchmark with clean labels and moderate class diversity. Performance on noisier, higher-resolution, or domain-specific datasets may diverge from these observations.
* **Defense scope** — Adversarial training at a fixed ε does not generalize automatically to unseen attack types. Certified defenses or randomized smoothing may provide stronger guarantees in high-stakes deployments.

---

# 6. Conclusion and Future Directions

## 6.1 Summary of Findings

This study set out to quantify the impact of gradient-based adversarial attacks on a convolutional image classifier and to assess whether adversarial training could restore practical robustness. Both objectives were met conclusively.

The baseline CNN, after achieving a respectable clean-data accuracy of 72.54%, was rendered nearly inoperative under FGSM attack at moderate perturbation levels. The adversarially trained variant — built on the same architecture, trained for the same duration — preserved significantly more accuracy across all evaluated perturbation budgets, confirming that the training procedure, rather than the network capacity, is the primary driver of adversarial robustness.

These findings carry a direct design implication: machine learning systems intended for adversarial environments should not treat security as a post-deployment concern. Threat-aware training should be integrated into the model development lifecycle from the earliest stages.

## 6.2 Directions for Future Investigation

Building on the groundwork laid here, several extensions would further advance the understanding of adversarial robustness:

1. **Iterative attack evaluation** — Testing against multi-step methods such as Projected Gradient Descent (PGD) and Carlini-Wagner (CW) attacks would reveal whether FGSM-based adversarial training generalizes to stronger threat models.
2. **Advanced defense integration** — Exploring certified defenses, randomized smoothing, or feature denoising layers may provide robustness guarantees beyond what empirical training can offer.
3. **Scalability to larger architectures** — Repeating the evaluation on ResNets or Vision Transformers would reveal how architecture depth and skip connections interact with adversarial vulnerability.
4. **Cross-domain experiments** — Extending the experimental protocol to medical imaging, natural language processing, or audio classification would test how well these findings generalize beyond the vision domain.
5. **Adaptive attack evaluation** — Measuring robustness against attacks specifically designed to circumvent the adversarial training defense would provide a more adversarially realistic assessment.

---

# References

[1] I. J. Goodfellow, J. Shlens, and C. Szegedy, "Explaining and Harnessing Adversarial Examples," *Proceedings of the International Conference on Learning Representations (ICLR)*, San Diego, CA, USA, 2015.

[2] A. Krizhevsky, "Learning Multiple Layers of Features from Tiny Images," Technical Report, Department of Computer Science, University of Toronto, Toronto, ON, Canada, 2009.

[3] Y. LeCun, Y. Bengio, and G. Hinton, "Deep Learning," *Nature*, vol. 521, no. 7553, pp. 436–444, May 2015.

[4] N. Papernot, P. McDaniel, I. Goodfellow, S. Jha, Z. B. Celik, and A. Swami, "Practical Black-Box Attacks against Machine Learning," *Proceedings of the ACM Asia Conference on Computer and Communications Security (ASIACCS)*, Abu Dhabi, UAE, 2017.

[5] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu, "Towards Deep Learning Models Resistant to Adversarial Attacks," *Proceedings of the International Conference on Learning Representations (ICLR)*, Vancouver, BC, Canada, 2018.

[6] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, and R. Fergus, "Intriguing Properties of Neural Networks," *Proceedings of the International Conference on Learning Representations (ICLR)*, Banff, AB, Canada, 2014.

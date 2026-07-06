# Project Lab Journal — Adversarial Training Study

---

## Entry 1: Dataset Initialization

**Dataset Selected:** CIFAR-10

**Partition Summary:**
- Training pool: 50,000 labeled images
- Held-out evaluation set: 10,000 labeled images

**Category Breakdown:**
1. Airplane
2. Automobile
3. Bird
4. Cat
5. Deer
6. Dog
7. Frog
8. Horse
9. Ship
10. Truck

**Observation:**
Loading was successful via Torchvision's built-in CIFAR-10 handler. The dataset is well-balanced, with 6,000 examples per category, making it a reliable substrate for comparative adversarial experiments where class imbalance could otherwise confound accuracy metrics.

---

## Entry 2: Rationale for CNN Architecture

**Chosen Model Type:** Convolutional Neural Network (CNN)

**Why CNNs for This Task:**
Convolutional layers are tailored for spatially structured inputs. Rather than treating each pixel as an independent feature (as a fully connected network would), they detect localized patterns — edges, textures, object parts — through shared filter banks. This hierarchical abstraction is both the source of CNNs' classification strength and, as adversarial examples reveal, a structural weakness: a well-targeted perturbation can disrupt the early-layer representations in ways that propagate and amplify through subsequent layers.

**Layer-wise Feature Hierarchy:**
- Layer 1 output: low-level primitives — oriented edges, color gradients, corner responses
- Layer 2 output: mid-level composites — object parts, texture patches, junctions
- Deeper layers: high-level concept abstractions linked to semantic categories

This hierarchy explains both why CNNs are effective classifiers and why small, structured input perturbations can systematically derail them.

---

## Entry 3: Spatial Dimension Analysis

**Input tensor shape:** 32 × 32 × 3 (height × width × RGB channels)

**After Convolutional Block 1 (Conv1):**
- Feature maps: 32 × 32 × 32 (32 filters, no spatial shrinkage with padding)

**After Max-Pooling 1:**
- Spatial dimensions halved: 16 × 16 × 32

**After Convolutional Block 2 (Conv2):**
- Feature maps: 16 × 16 × 64

**After Max-Pooling 2:**
- Spatial dimensions halved again: 8 × 8 × 64

**Flattened representation:**
- Total features: 8 × 8 × 64 = **4096**

**Observation:**
Pooling layers serve a dual purpose — they introduce translational invariance and reduce the number of parameters that downstream fully connected layers must handle. The progressive compression from 32×32×3 to a 4096-dimensional vector encodes what the convolutional stack "believes" is most relevant for distinguishing between classes.

---

## Entry 4: Fully Connected Classification Head

**FC1:** 4096 → 512
- Purpose: Compress the high-dimensional convolutional feature vector into a more compact intermediate representation, forcing the network to retain only the most discriminative information.

**FC2 (Output):** 512 → 10
- Purpose: Project the compressed representation into a 10-dimensional score space, one dimension per CIFAR-10 category. The argmax of this vector determines the predicted class.

**Activation Function:** ReLU — f(x) = max(0, x)
- Introduces non-linearity essential for learning complex mappings
- Zero-clamps negative activations, creating sparse representations
- Avoids vanishing gradient problems associated with sigmoid/tanh in deep stacks

**Observation:**
Ten output neurons were chosen specifically because CIFAR-10 has exactly ten mutually exclusive categories. A softmax applied to these raw logits converts them to a probability distribution; during training, cross-entropy loss penalizes the divergence between this distribution and the one-hot ground truth.

---

## Entry 5: Training Dynamics and Configuration

**Batch Size:** 32
- Balances memory efficiency with gradient estimate stability
- Mini-batches of 32 are small enough for frequent updates and large enough to provide statistically reliable gradient directions

**Epoch:**
- One epoch = one complete traversal of all 50,000 training samples
- After 10 epochs, each image has been used 10 times to adjust network weights

**Learning Rate:** 0.001
- Conservative value: updates are small, reducing the risk of overshooting optimal parameter configurations
- Chosen to pair with Adam, which adapts per-parameter learning rates internally based on gradient history

**Optimizer:** Adam
- Selected for its robustness to varying gradient magnitudes across layers
- Combines momentum (accumulating gradient direction history) with RMS scaling (normalizing by recent gradient magnitude), yielding stable convergence across a wide range of architectures

**Training Loop Summary:**
1. Sample a batch of 32 (image, label) pairs
2. Forward pass: compute logit predictions
3. Compute cross-entropy loss against ground truth labels
4. Backward pass: propagate gradients to all learnable parameters
5. Adam step: update weights using scaled, momentum-adjusted gradients
6. Repeat until all batches in one epoch are processed

---

## Entry 6: Architecture Verification

**Status:** Instantiation successful — no import errors or dimension mismatches detected.

**Verified Architecture:**
- Conv1: 3 → 32 feature maps, 3×3 kernel
- Conv2: 32 → 64 feature maps, 3×3 kernel
- MaxPool: 2×2 window, stride 2
- FC1: 4096 → 512
- FC2: 512 → 10

**Observation:**
Passing a dummy tensor of shape [1, 3, 32, 32] through the network produced an output of shape [1, 10] without errors, confirming correct layer wiring.

---

## Entry 7: Batch Data Inspection

**Batch Composition:**
- 32 images per batch
- Tensor shape per batch: [32, 3, 32, 32]
  - 32 samples, 3 color channels, 32×32 pixels each
- Label tensor shape: [32]

**Observation:**
Each DataLoader iteration yields a correctly paired (image tensor, integer label) batch. The label indices correspond to: 0=airplane, 1=automobile, 2=bird, 3=cat, 4=deer, 5=dog, 6=frog, 7=horse, 8=ship, 9=truck.

---

## Entry 8: Loss Function Setup

**Function Used:** CrossEntropyLoss
- Mathematically equivalent to applying log-softmax to logits followed by negative log-likelihood
- Ideal for multi-class problems with mutually exclusive categories

**Behavior:**
- Confident and correct predictions → low loss value
- Confident but incorrect predictions → very high loss (heavy penalty)
- Uncertain (uniform) predictions → intermediate loss

**Observation:**
CrossEntropyLoss suits CIFAR-10 because each image belongs to exactly one of ten non-overlapping categories. Loss convergence directly corresponds to improved class discrimination.

---

## Entry 9: Optimizer Initialization

**Optimizer:** Adam
**Learning Rate:** 0.001

**Observation:**
Adam was initialized with default PyTorch settings (β₁ = 0.9, β₂ = 0.999, ε = 1e-8). These default values have been empirically validated across many neural network training tasks and required no tuning for this experiment.

---

## Entry 10: Initial Forward Pass

**Result:** Loss = 2.2969

**Interpretation:**
At random initialization, a 10-class classifier should produce roughly uniform output probabilities (~0.10 per class). The corresponding cross-entropy for a uniform distribution over 10 classes is approximately ln(10) ≈ 2.303. The observed initial loss of 2.2969 is consistent with this expectation, confirming that the network started from a near-random prediction state before training.

---

## Entry 11: First Backpropagation Step

**Recorded Loss:** 2.3120

**Operations Verified:**
- Forward pass: logits computed
- Loss computed against true labels
- Backpropagation: gradients accumulated at each layer
- Adam step: weights updated in gradient-descent direction

**Observation:**
Slight stochastic variation in the loss (2.2969 → 2.3120) after a single batch update is normal and expected. Meaningful loss reduction only becomes visible over many batches.

---

## Entry 12: Single Epoch Training Run

**Configuration:**
- Dataset: CIFAR-10
- Batch Size: 32
- Optimizer: Adam
- Learning Rate: 0.001
- Epochs: 1

**Results:**
- End-of-epoch loss: 1.3627
- End-of-epoch accuracy: 50.38%

**Observation:**
After seeing each of the 50,000 training images once, the network improved from random guessing (~10% accuracy) to correctly classifying roughly half the training set. The loss drop from ~2.30 to 1.36 confirms productive feature learning within a single pass.

---

## Entry 13: Full 10-Epoch Training

**Configuration:**
- Dataset: CIFAR-10
- Batch Size: 32
- Optimizer: Adam
- Learning Rate: 0.001

**Epoch-by-Epoch Log:**

| Epoch | Training Loss | Training Accuracy |
|---|---|---|
| 1 | 1.4368 | 48.34% |
| 2 | 1.0521 | 62.91% |
| 3 | 0.8860 | 68.88% |
| 4 | 0.7578 | 73.29% |
| 5 | 0.6464 | 77.14% |
| 6 | 0.5430 | 80.84% |
| 7 | 0.4448 | 84.32% |
| 8 | 0.3565 | 87.48% |
| 9 | 0.2838 | 89.97% |
| 10 | 0.2236 | 92.08% |

**Observation:**
Loss declined consistently across all ten epochs. The model ended training at 92.08% accuracy on the training partition, suggesting strong in-sample learning. However, training accuracy being substantially higher than test accuracy (72.54%) suggests some degree of overfitting — the model has memorized training-specific patterns that do not fully transfer.

---

## Entry 14: Test Set Evaluation

**Dataset:** CIFAR-10 Test Partition  
**Number of Test Images:** 10,000

**Result: Test Accuracy = 72.54%**

**Analysis:**
The gap between training accuracy (92.08%) and test accuracy (72.54%) — approximately 19.5 percentage points — signals overfitting. No regularization techniques (dropout, weight decay, data augmentation) were applied in the baseline model, which accounts for this generalization gap. Despite overfitting, 72.54% clean-data accuracy is adequate to serve as a meaningful baseline for studying adversarial perturbation effects.

---

## Entry 15: First Adversarial Attack — Single Sample

**Target Sample:**
- Ground Truth: Cat (class index 3)
- Clean Prediction: Cat (3) ✓

**Attack Protocol:**
- Method: FGSM
- Budget: ε = 0.03

**Outcome:**
- Adversarial Prediction: Dog (class index 5) ✗

**Step-by-Step Procedure:**

```python
# 1. Set requires_grad to enable gradient tracking on input
images.requires_grad = True

# 2. Forward pass to get current predictions
outputs = model(images)

# 3. Compute loss using true labels
criterion = nn.CrossEntropyLoss()
loss = criterion(outputs, labels)

# 4. Zero previous gradients, then backpropagate
model.zero_grad()
loss.backward()

# 5. Extract gradient sign and apply perturbation
epsilon = 0.03
data_grad = images.grad.data
sign_data_grad = data_grad.sign()
perturbed_image = images + epsilon * sign_data_grad

# 6. Clamp to valid pixel range [0, 1]
perturbed_image = torch.clamp(perturbed_image, 0, 1)

# 7. Evaluate model on adversarial input
adv_output = model(perturbed_image)
_, adv_prediction = torch.max(adv_output, 1)
```

**Observation:**
The model produced the correct label (Cat) on the clean image, but after a single FGSM step, the same model misidentified the image as Dog. The pixel-level change was imperceptible to human inspection, demonstrating that FGSM can produce highly effective adversarial inputs with minimal computational cost.

---

## Entry 16: Full-Dataset FGSM Robustness Evaluation

**Evaluated Model:** Standard SimpleCNN
**Dataset:** CIFAR-10 Test Set (10,000 images)
**Attack:** FGSM at ε = 0.03

| Metric | Value |
|---|---|
| Clean Accuracy | 72.54% |
| FGSM Adversarial Accuracy | 7.34% |
| Absolute Accuracy Drop | 65.20 pp |

**Observation:**
A single-step gradient perturbation at a visually minimal budget slashed classification accuracy to a near-random level. This extreme fragility confirms that the standard CNN's decision boundaries, while accurate for in-distribution inputs, are geometrically brittle with respect to adversarially directed perturbations.

---

## Entry 17: Multi-Budget FGSM Evaluation (Standard CNN)

| ε | Accuracy (%) |
|---|---|
| 0.01 | 23.13 |
| 0.03 | 7.34 |
| 0.05 | 3.35 |
| 0.10 | 1.04 |

**Observation:**
Accuracy degrades non-linearly as perturbation strength grows. Even at the smallest evaluated budget (ε = 0.01), accuracy drops to less than a third of the clean value. The rapid degradation slope implies that the model's prediction confidence in correct classes is easily overwhelmed by gradient-directed input modifications.

---

## Entry 18: Multi-Budget Comparison — Standard vs. Adversarially Trained CNN

| ε | Standard CNN (%) | Adversarial CNN (%) | Gain (pp) |
|---|---|---|---|
| 0.01 | 23.13 | 39.17 | +16.04 |
| 0.03 | 7.34 | 29.04 | +21.70 |
| 0.05 | 3.35 | 21.17 | +17.82 |
| 0.10 | 1.04 | 9.25 | +8.21 |

**Observation:**
The adversarially trained model outperformed the standard model at every evaluated perturbation level. The largest absolute gains appear at intermediate budgets (ε = 0.03–0.05), where the standard model approaches random-chance performance but the robust model retains practically meaningful classification rates.

The consistent improvement across the full epsilon range — not just at the training budget of 0.03 — suggests that adversarial training generalizes its robustness benefit to nearby perturbation levels, not just the exact budget used during training.

---

## Summary of Key Experimental Outcomes

| Experiment | Key Finding |
|---|---|
| Baseline Training | 72.54% clean accuracy after 10 epochs |
| FGSM (ε=0.03) on Standard CNN | Accuracy collapsed to 7.34% |
| Adversarial Training | Robust model achieved 65.15% clean accuracy |
| FGSM (ε=0.03) on Robust CNN | Accuracy retained at 28.38% (vs. 7.34%) |
| Multi-budget evaluation | Robust model consistently superior across all tested ε values |

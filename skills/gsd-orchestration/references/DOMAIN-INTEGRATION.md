# Domain Skill Integration Guide

GSD integrates with domain-specific skill systems to provide specialized expertise during development workflows. This guide defines the integration protocol and includes the ML/DL domain profile.

---

## How Domain Integration Works

### Detection
During `gsd init` or `gsd discuss`, GSD scans PROJECT.md tech stack for domain keywords. When a match is found, the domain profile activates.

### Integration Points

| GSD Command | Domain Integration |
|-------------|-------------------|
| `gsd init` | Detect domain from tech stack → note in PROJECT.md |
| `gsd discuss` | Offer domain consultation → ask domain questions → save to CONTEXT.md |
| `gsd plan` | Load domain profile → reference sub-skills in PLAN actions → use domain task templates |
| `gsd execute` | PLAN actions include sub-skill references → domain rules auto-enforced |
| `gsd verify` | Domain verification checklist appended to standard checks |

### CONTEXT.md Domain Section

When domain consultation is accepted, add this section to CONTEXT.md:

```markdown
## Domain Decisions
- **Domain**: [ML/DL]
- **Task Type**: [Classification / Regression / NLP / Vision / RL / Generative]
- **Data Type**: [Tabular / Text / Images / None]
- **Primary Sub-Skills**: [list of sub-skills for this phase]
- **Evaluation Strategy**: [metrics and approach]
- **Deployment Target**: [Course / Prototype / Production / Research]
- **Key Constraints**: [compute, data size, latency, etc.]
```

### PLAN-X.md Domain Tags

When planning domain-aware tasks, use the `<domain-skill>` tag:

```xml
<task type="auto">
  <name>Prepare training data</name>
  <domain-skill>ml-fundamentals, data-pipeline</domain-skill>
  <files>src/data/prepare.py, src/data/transforms.py</files>
  <action>
    Follow ml-fundamentals Pattern 3 (train/test split):
    - Split FIRST, then preprocess
    - Fit scaler on train ONLY
    - Stratified split for classification
    ...
  </action>
  <verify>python -m pytest tests/test_data.py</verify>
  <expected>All data pipeline tests pass, no leakage detected</expected>
</task>
```

---

## ML/DL Domain Profile

### Detection Keywords

Match ANY of these in PROJECT.md tech stack (case-insensitive):

```
PyTorch, TensorFlow, sklearn, scikit-learn, neural network, deep learning,
CNN, BERT, GPT, RAG, embeddings, transformer, training loop, loss function,
model training, computer vision, NLP, reinforcement learning, fine-tuning,
LSTM, GAN, diffusion, HuggingFace, vector store, FAISS, ChromaDB,
XGBoost, CatBoost, LightGBM, Keras, MLflow, W&B, SHAP, LoRA, QLoRA
```

### Skill System Reference

**Root**: `ml-dl-skills/SKILL.md` — Routes to 17 specialized sub-skills with 78 reference files.

**Task Skills** (available during any GSD phase):
- `/debug-training [error]` — Systematic 4-phase ML debugging
- `/explain-concept [concept]` — 8-step concept explanation with Hebrew
- `/find-dataset [task]` — 5-step data sourcing

**Rule** (auto-enforced on `.py` files): `ml-best-practices.md`

### ML/DL Discuss Questions

When ML/DL domain is detected during `gsd discuss`, ask these clarifying questions:

**Q1: "What type of ML/DL task?"**
- Classification (categories: spam, sentiment, diagnosis)
- Regression (numbers: prices, scores, predictions)
- NLP (text processing, Q&A, chatbot, RAG, summarization)
- Vision (image classification, detection, generation)
- Other (RL, recommender, generative, clustering, time series)

**Q2: "What data do you have?"**
- Tabular CSV (structured rows and columns)
- Text documents (articles, PDFs, conversations)
- Images (photos, scans, diagrams)
- No data yet (need to find or generate)

**Q3: "What's the evaluation strategy?"**
- Accuracy / F1 / Precision / Recall (classification)
- MSE / MAE / R² (regression)
- BLEU / ROUGE / Perplexity (NLP generation)
- Custom domain metrics
- Not sure yet (will recommend based on task)

**Q4: "What's the project goal?"**
- Course assignment (learning exercise, need to understand concepts)
- Prototype (quick POC, experimentation)
- Production (reliable, scalable, deployed)
- Research (comparing approaches, benchmarking)

**Q5: "Compute constraints?"**
- CPU only
- Single GPU
- Multi-GPU / Cloud
- Not sure

### Sub-Skill Routing for GSD Phases

Based on discuss answers, route to the right sub-skills per phase:

| GSD Phase Goal | Primary Sub-Skill | Also Load | Reference For |
|----------------|-------------------|-----------|---------------|
| Data preparation | `ml-fundamentals` | `data-pipeline` | Split, scale, feature engineering |
| Text preprocessing | `nlp-classical` | `data-pipeline` | TF-IDF, tokenization, cleaning |
| Image preprocessing | `cnn-vision` | `ml-fundamentals` | Augmentation, transforms |
| PDF/document pipeline | `data-pipeline` | `rag-retrieval` | Parsing, chunking, embeddings |
| Tabular ML model | `ml-fundamentals` | `ml-advanced` | sklearn, XGBoost, evaluation |
| Deep learning model | `deep-learning-core` | `pytorch-mastery` | Training loop, loss, optimizer |
| CNN / vision model | `cnn-vision` | `pytorch-mastery` | Architecture, transfer learning |
| NLP / text model | `transformers-llm` | `nlp-classical` | BERT, HuggingFace, zero-shot |
| RAG system | `rag-retrieval` | `data-pipeline`, `transformers-llm` | Vector store, retrieval, LLM |
| Fine-tune LLM | `fine-tuning-peft` | `transformers-llm`, `mlops-experiment` | LoRA, QLoRA, SFTTrainer |
| RL agent | `reinforcement-learning` | `pytorch-mastery` | DQN, PPO, Gymnasium |
| Generative model | `generative-models` | `cnn-vision`, `pytorch-mastery` | GAN, VAE, Diffusion |
| Recommender system | `ml-advanced` | `pytorch-mastery`, `deep-learning-core` | Matrix Factorization, NeuMF |
| Evaluation & analysis | `model-interpretability` | `ml-fundamentals` | SHAP, LIME, Grad-CAM |
| Experiment tracking | `mlops-experiment` | (any modeling skill) | MLflow, W&B, Optuna |

### ML/DL Task Templates for PLAN-X.md

#### Data Preparation Task

```xml
<task type="auto">
  <name>Data preparation and splitting</name>
  <domain-skill>ml-fundamentals</domain-skill>
  <files>src/data/prepare.py, src/data/transforms.py</files>
  <action>
    Follow ml-fundamentals data preparation patterns:

    1. Load and explore data (EDA):
       - df.shape, df.info(), df.describe()
       - Check missing values, class distribution
       - Visualize target distribution

    2. Split FIRST (before any preprocessing!):
       - train_test_split with stratify (if classification)
       - Typical split: 80/10/10 (train/val/test)
       - Set random_state for reproducibility

    3. Preprocess (fit on train ONLY):
       - StandardScaler / MinMaxScaler: fit on train, transform all
       - Encoding: fit LabelEncoder/OneHotEncoder on train
       - Handle missing values based on train statistics

    4. Save processed datasets:
       - Clearly separated train/val/test files
       - Save fitted transformers for inference

    CRITICAL: Never fit any transformer on test/val data!
  </action>
  <verify>python -m pytest tests/test_data_pipeline.py -v</verify>
  <expected>All data tests pass, shapes verified, no leakage</expected>
</task>
```

#### Model Training Task

```xml
<task type="auto" depends="task-1">
  <name>Model architecture and training</name>
  <domain-skill>pytorch-mastery, deep-learning-core</domain-skill>
  <files>src/models/model.py, src/training/train.py</files>
  <action>
    Follow pytorch-mastery training loop pattern:

    1. Define model architecture:
       - Based on CONTEXT.md model decision
       - Use nn.Module with clear forward()
       - Match output dimensions to task (1 for binary, N for multiclass)

    2. Set up training components:
       - Loss: BCEWithLogitsLoss (binary) / CrossEntropyLoss (multiclass) / MSELoss (regression)
       - Optimizer: Adam (default) or AdamW (for transformers)
       - Scheduler: ReduceLROnPlateau or CosineAnnealing
       - Set random seeds: torch.manual_seed(42), np.random.seed(42)

    3. Training loop:
       - model.train() for training
       - model.eval() + torch.no_grad() for validation
       - Track train/val loss per epoch
       - Early stopping on val loss (patience=5)
       - Save best model checkpoint

    4. Log results:
       - Training curves (loss, metrics per epoch)
       - Best epoch and metrics
       - Model summary (parameters count)

    CRITICAL: Use BCEWithLogitsLoss (NOT BCELoss). Always eval mode for validation.
  </action>
  <verify>python src/training/train.py --epochs 2 --dry-run</verify>
  <expected>Training completes without errors, val metrics computed, checkpoint saved</expected>
</task>
```

#### Evaluation Task

```xml
<task type="auto" depends="task-2">
  <name>Model evaluation and analysis</name>
  <domain-skill>model-interpretability, ml-fundamentals</domain-skill>
  <files>src/evaluation/evaluate.py, src/evaluation/analysis.py</files>
  <action>
    Follow model-interpretability evaluation patterns:

    1. Compute metrics on test set:
       - Classification: accuracy, precision, recall, F1, confusion matrix, ROC-AUC
       - Regression: MSE, MAE, R², residual plot
       - Ranking: NDCG, MAP, MRR

    2. Error analysis:
       - Identify worst predictions (highest loss samples)
       - Check for systematic biases (per class, per feature group)
       - Compare against baseline (random, majority class, simple model)

    3. Interpretability (if applicable):
       - SHAP values for feature importance
       - Grad-CAM for vision models
       - Attention weights for transformer models

    4. Generate evaluation report:
       - Summary table of all metrics
       - Comparison vs baseline
       - Key findings and recommendations
  </action>
  <verify>python src/evaluation/evaluate.py --model checkpoints/best.pt</verify>
  <expected>Evaluation report generated, metrics above baseline</expected>
</task>
```

### ML/DL Verification Checklist

Append these checks to standard `gsd verify` output:

```markdown
### ML/DL Domain Checks
- [ ] Data split performed BEFORE any preprocessing
- [ ] Scaler/encoder fit on train set ONLY (no data leakage)
- [ ] Correct loss function for task type
- [ ] model.eval() + torch.no_grad() used for inference/validation
- [ ] Random seeds set for reproducibility (torch, numpy, random)
- [ ] No SMOTE/augmentation applied to test data
- [ ] Metrics compared against meaningful baseline
- [ ] Class imbalance addressed (if classification)
- [ ] Training curves show convergence (no NaN, no divergence)
- [ ] Model checkpoint saved for best validation performance
```

### ML 5-Step Workflow → GSD Phase Mapping

The standard ML workflow maps naturally to GSD phases:

```
ML Step 1: UNDERSTAND  →  gsd discuss  (domain consultation, clarify task/data/goals)
ML Step 2: EDA         →  gsd execute Task 1  (explore data, visualize, identify issues)
ML Step 3: PREPROCESS  →  gsd execute Task 1-2  (split, transform, augment)
ML Step 4: MODEL       →  gsd execute Task 2-3  (train, tune, iterate)
ML Step 5: EVALUATE    →  gsd verify  (ML verification checklist + metrics)
```

For multi-phase ML projects, each GSD phase covers a larger scope:
- **Phase 1**: Data (EDA + preprocessing + pipeline)
- **Phase 2**: Model (architecture + training + tuning)
- **Phase 3**: Evaluation (metrics + interpretability + deployment readiness)

---

## Adding New Domain Profiles

To add a new domain (e.g., Web3, Bioinformatics, Game Dev):

1. Add detection keywords to the Supported Domains table in GSD SKILL.md
2. Create a domain profile section in this file following the ML/DL template:
   - Detection keywords
   - Discuss questions
   - Sub-skill routing table
   - Task templates for PLAN-X.md
   - Verification checklist
3. Ensure the domain's skill system has a GSD integration section (like ML/DL Section 13)

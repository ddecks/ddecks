+++
title = 'MLA-C01 Study Articles'
description = 'Compiled study notes covering all four AWS MLA-C01 exam domains plus foundational ML knowledge'
date = 2026-04-28
tags = ['aws', 'certification', 'ai', 'machine-learning']
weight = 3
+++

This document covers all four exam domains plus foundational ML knowledge. Articles 1-6 cover Domain 2 (ML Model Development). Articles 7-10 cover Domain 1 (Data Preparation). Articles 11-13 cover Domain 3 (Deployment and Orchestration). Articles 14-16 cover Domain 4 (Monitoring, Maintenance, and Security). Articles 17-19 cover cross-domain ML foundations.

---

# Domain 2: ML Model Development (26%)

---

# Article 1: Text Preprocessing: Tokenization, TF-IDF, and Embeddings

Source: https://kindatechnical.com/machine-learning/text-preprocessing-tokenization-tfidf-embeddings.html

Text data is fundamentally different from numerical data. Before any machine learning model can process text, it must be converted into numerical representations that capture meaning, context, and relationships between words.

## Text Cleaning

Raw text from real sources is messy. Cleaning and normalizing text is the essential first step.

```python
import re
import string
from typing import List

def clean_text(text: str, lowercase: bool = True,
               remove_html: bool = True,
               remove_urls: bool = True,
               remove_numbers: bool = False) -> str:
    if remove_html:
        text = re.sub(r'<[^>]+>', ' ', text)
    if remove_urls:
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    if lowercase:
        text = text.lower()
    if remove_numbers:
        text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

## Tokenization Methods

Tokenization splits text into units (tokens) that serve as the atomic elements for downstream processing.

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

text = "The cats were running quickly through the beautiful gardens"
tokens = word_tokenize(text.lower())
stop_words = set(stopwords.words('english'))
filtered = [t for t in tokens if t not in stop_words]

# Stemming: crude but fast
stemmer = PorterStemmer()
stemmed = [stemmer.stem(t) for t in filtered]

# Lemmatization: proper dictionary-based root form
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(t) for t in filtered]

# Subword tokenization (used by modern transformers)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
tokens = tokenizer.tokenize("The unbelievably fast tokenization process")
# ['the', 'un', '##bel', '##iev', '##ably', 'fast', 'token', '##ization', 'process']
```

## TF-IDF: Term Frequency-Inverse Document Frequency

TF-IDF improves on raw counts by weighting terms based on their importance. Words that appear frequently in a specific document but rarely across the corpus get high weights.

The formula: TF-IDF(t, d) = TF(t, d) x IDF(t) where IDF(t) = log(N / df(t)).

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(
    max_features=1000, stop_words='english',
    ngram_range=(1, 2), min_df=2, max_df=0.95,
    sublinear_tf=True
)
X_tfidf = tfidf.fit_transform(documents)
```

## Word Embeddings

Word embeddings map words to dense, low-dimensional vectors where semantic similarity is captured by vector proximity. Unlike TF-IDF, embeddings understand that "king" and "queen" are related.

## Sentence Transformers

For production applications, sentence transformers encode entire sentences into dense vectors that capture semantic meaning.

**Key Insight:** The evolution from bag-of-words to TF-IDF to word embeddings to sentence transformers represents a progression in how much semantic understanding is captured. Choose the simplest representation that works for your task.

---

# Article 2: NLP 101 — From Text Preprocessing to Transformer Models

Source: https://pyuniverse.com/nlp-101-text-preprocessing-to-transformer-models/

## The Importance of Text Preprocessing

Key steps: normalization, tokenization, stopword removal, stemming/lemmatization, and handling special tokens.

## Feature Representation Techniques

- **Bag-of-Words (BoW):** Counts token frequency, disregarding order.
- **TF-IDF:** Weighs term frequency by inverse document frequency.
- **Word2Vec / GloVe:** Static, dense embeddings capturing semantic similarity.
- **ELMo / BERT / RoBERTa:** Dynamic contextual embeddings that vary with context.

## Transformers: The Game Changer

Introduced by Vaswani et al. (2017), transformer architectures rely on **self-attention** to model relationships across all tokens simultaneously:
- **Parallelized training** (no sequential recurrence)
- **Long-range dependency capture** via multi-head attention
- **Scalability** to billions of parameters

Self-Attention: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V

### Pretrained Transformer Models
- **BERT** for masked language modeling and next-sentence prediction
- **GPT-n** series for autoregressive generation
- **T5** and **BART** for text-to-text tasks

## Best Practices
- **Start Simple:** Benchmark TF-IDF + linear models before heavy transformers
- **Manage Token Length:** Truncate or chunk long documents
- **Monitor Overfitting:** Early stopping on validation loss
- **Optimize Inference:** Quantization or distillation (DistilBERT)

---

# Article 3: Machine Learning Algorithms You Should Learn First

Source: https://www.dataquest.io/blog/top-10-machine-learning-algorithms-for-beginners/

## Types of Machine Learning

- **Supervised Learning** — labeled data, predict a target
- **Unsupervised Learning** — no labels, find structure
- **Reinforcement Learning** — learn by interacting with an environment and receiving rewards

## Supervised Learning Algorithms

**Linear Regression** — Predicts continuous outcome: Y = B0 + B1*X. Use when relationship is roughly linear.

**Logistic Regression** — Sigmoid function, squashes output to 0-1. Despite the name, it's a classification algorithm.

**Decision Trees** — Splits data into branches based on feature values. Highly interpretable but prone to overfitting.

**Naive Bayes** — Based on Bayes' Theorem, assumes feature independence. Popular for text classification.

**KNN** — Majority vote of k nearest neighbors. Simple but slow on large datasets. Requires feature scaling.

**SVMs** — Maximizes margin between classes. Kernel functions handle non-linear relationships.

**Random Forests** — Ensemble of decision trees on random subsets. Strong out-of-the-box performance.

**Gradient Boosting** — Sequential trees correcting previous errors. XGBoost, LightGBM, CatBoost.

**LASSO (L1) / Ridge (L2)** — Regularized linear models. LASSO can zero out coefficients for feature selection.

## Unsupervised Learning Algorithms

**K-Means** — Iterative centroid-based clustering. Must specify k in advance.

**PCA** — Projects onto principal components capturing maximum variance. Preprocessing technique.

**t-SNE** — Maps high-dimensional data to 2-3D for visualization. Not for preprocessing.

## Quick Reference

| Algorithm | Problem Type | Best For | Watch Out For |
|---|---|---|---|
| Linear Regression | Regression | Linear relationships | Sensitive to outliers |
| Logistic Regression | Classification | Binary, interpretable | Non-linear boundaries |
| Decision Trees | Both | Interpretable, mixed types | Overfitting |
| Random Forest | Both | Strong default performance | Less interpretable |
| Gradient Boosting | Both | Tabular data | More tuning needed |
| KNN | Both | Small datasets, prototyping | Slow on large data |
| SVMs | Classification | High-dimensional data | Slow to train at scale |
| K-Means | Clustering | Segmentation | Must specify k |
| PCA | Dim. Reduction | Noise reduction | Assumes linearity |

---

# Article 4: Grid Search and Bayesian Optimization Simply Explained

Source: https://towardsdatascience.com/a-step-by-step-introduction-to-bayesian-hyperparameter-optimization-94a623062fc

Hyperparameters control the learning process (max tree depth, learning rate, regularization, etc.). Hyperparameter optimization searches for the combination that produces the best model.

## Grid Search
Evaluate every combination in a defined grid. Simple and exhaustive but cost explodes with more hyperparameters.

## Random Search
Randomly sample combinations. Often finds good results faster because not all hyperparameters are equally important.

## Bayesian Optimization
Uses previous evaluation results to make smarter choices about what to evaluate next:
1. Start with random evaluations
2. Build a surrogate function (Gaussian Process) approximating the loss landscape
3. Use an acquisition function (Expected Improvement) balancing exploitation vs. exploration
4. Evaluate the chosen point, update the surrogate, repeat

**When to use:** Expensive-to-evaluate models, limited compute budget, want good hyperparameters with fewer evaluations.

---

# Article 5: SageMaker Built-in Algorithms and Pretrained Models

Source: https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html

## Supervised Learning — General Purpose
- **XGBoost** — gradient-boosted trees, ensemble of simpler models
- **Linear Learner** — linear function for regression or threshold for classification
- **AutoGluon-Tabular** — AutoML framework, ensembles and stacks models
- **CatBoost** — ordered boosting, native categorical feature handling
- **LightGBM** — GOSS and EFB for efficiency
- **Factorization Machines** — captures feature interactions in sparse data
- **TabTransformer** — self-attention for tabular data

## Supervised Learning — Specialized
- **DeepAR** — time-series forecasting with RNNs
- **Object2Vec** — learns dense embeddings for feature engineering

## Unsupervised Learning
- **PCA** — dimensionality reduction
- **K-Means** — clustering
- **Random Cut Forest (RCF)** — anomaly detection
- **IP Insights** — detects suspicious IP usage patterns

## Textual Analysis
- **BlazingText** — optimized Word2vec and text classification
- **Sequence-to-Sequence** — translation, summarization, speech-to-text
- **LDA / NTM** — topic modeling

## Image Processing
- **Image Classification** (MXNet / TensorFlow)
- **Object Detection** (MXNet / TensorFlow)
- **Semantic Segmentation** — pixel-level classification

## Quick Reference: Use Case to Algorithm

| Use Case | Algorithm |
|---|---|
| Classification/Regression (tabular) | XGBoost, Linear Learner, AutoGluon, CatBoost, LightGBM |
| Time-series forecasting | DeepAR |
| Anomaly detection | Random Cut Forest (RCF) |
| Clustering | K-Means |
| Topic modeling | LDA, NTM |
| Text classification | BlazingText |
| Image classification | Image Classification (MXNet/TF) |
| Object detection | Object Detection (MXNet/TF) |

---

# Article 6: MLA-C01 Study Guide — Topic Outline

Source: https://www.mindmeshacademy.com/certifications/aws/aws-certified-machine-learning-engineer-associate/study-guide

**Exam Details:** 65 questions (50 scored, 15 unscored) — Multiple choice, multiple response, ordering, matching, case study | 170 minutes | Passing score: 720/1000

Domain 1 (Data Preparation) carries the heaviest weight at 28%. Combined with Domain 4's 24% on monitoring and security, over half the exam tests what happens *around* the model.

### Phase 2: Data Preparation for ML (28%)
- Data Formats, Storage (S3, EFS, FSx), Streaming (Kinesis, Kafka)
- Data Cleaning, Feature Engineering, Encoding
- AWS Tools: Glue, DataBrew, EMR, Data Wrangler
- Bias Detection, Data Quality, Ground Truth Labeling

### Phase 3: ML Model Development (26%)
- SageMaker Built-in Algorithms, Bedrock, JumpStart
- Training Process, Hyperparameter Tuning (AMT)
- Regularization, Distributed Training, Model Registry
- Evaluation Metrics, Clarify, Debugger

### Phase 4: Deployment and Orchestration (22%)
- Endpoint Types: Real-Time, Serverless, Async, Batch
- Containers (Pre-built vs. BYOC), SageMaker Neo
- SageMaker Pipelines, CodePipeline, CodeBuild
- Deployment Strategies: Blue/Green, Canary, Linear

### Phase 5: Monitoring, Maintenance, and Security (24%)
- Model Monitor, Data/Model Drift, A/B Testing
- CloudWatch, Cost Optimization (Spot, Savings Plans)
- IAM, VPCs, Encryption (KMS), Compliance

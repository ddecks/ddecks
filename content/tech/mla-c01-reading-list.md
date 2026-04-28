+++
title = 'MLA-C01 Reading List'
description = 'Curated reading list for the AWS Machine Learning Associate exam, organized by domain with estimated reading times'
date = 2026-04-28
tags = ['aws', 'certification', 'ai', 'machine-learning']
weight = 2
+++

Organized by exam domain with estimated reading times. Priority order within each domain is top-to-bottom. AWS documentation links are free; all other resources listed are free/non-paywalled.

---

## Domain 1: Data Preparation for ML (28% of exam)

~90 minutes total. Priority: 1 → 2 → 3 → 5 → 4 → 6.

### 1. AWS Data Preparation Tools (~15 min)

- [Recommendations for choosing the right data preparation tool in SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/data-prep.html) — Official decision guide for when to use Data Wrangler, Processing jobs, Glue, or EMR. Start here.
- [Prepare ML Data with SageMaker Data Wrangler](https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html) — Visual data prep, 300+ built-in transforms, natural language interface. Now integrated into SageMaker Canvas.

### 2. AWS Glue for ETL (~15 min)

- [What is AWS Glue?](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html) — Serverless ETL, Data Catalog, crawlers, and how Glue fits into ML data pipelines.
- [Data discovery and cataloging in AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html) — Crawlers, schema detection, and the Data Catalog as a central metadata store.
- [Using AWS Glue for Data Preparation (kindatechnical.com)](https://www.kindatechnical.com/aws-machine-learning/lesson-12-using-aws-glue-for-data-preparation.html) — Practical walkthrough of Glue for ML data prep.

### 3. Streaming Data Ingestion (~15 min)

- [Amazon Kinesis Data Streams Developer Guide](https://docs.aws.amazon.com/streams/latest/dev/introduction.html) — Real-time data streaming: shards, producers, consumers, retention.
- [Amazon Data Firehose (formerly Kinesis Data Firehose)](https://aws.amazon.com/about-aws/whats-new/2024/02/amazon-data-firehose-formerly-kinesis-data-firehose/) — Managed delivery to S3, Redshift, OpenSearch. Know the difference from Kinesis Data Streams.
- [Data Ingestion Methods (AWS Whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/data-ingestion-methods) — Overview of batch vs. streaming ingestion into data lakes.

### 4. Data Labeling (~10 min)

- [SageMaker Ground Truth](https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html) — Human labeling with Mechanical Turk, private workforces, and automated data labeling.
- [Automate data labeling](https://docs.aws.amazon.com/sagemaker/latest/dg/sms-automated-labeling.html) — How Ground Truth uses active learning to reduce labeling costs.

### 5. Feature Engineering Fundamentals (~20 min)

- [Text Preprocessing: Tokenization, TF-IDF, and Embeddings](https://kindatechnical.com/machine-learning/text-preprocessing-tokenization-tfidf-embeddings.html) — Full NLP pipeline from raw text to model input.
- [From Text Preprocessing to Transformer Models](https://pyuniverse.com/nlp-101-text-preprocessing-to-transformer-models/) — End-to-end walkthrough from cleaning text to BERT/GPT.
- [SageMaker Feature Store](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html) — Centralized feature repository for training and inference consistency.

### 6. Data Storage and Formats (~15 min)

- [Amazon S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/) — S3 Standard, IA, Glacier. Know which tier for training data vs. archived models.
- [Amazon FSx for Lustre](https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html) — High-performance file system for training workloads. Integrates with S3.
- [Apache Parquet Format](https://parquet.apache.org/docs/overview/) — Columnar format optimized for analytics and ML. Why it matters for SageMaker.

---

## Domain 2: ML Model Development (26% of exam)

~70 minutes total. Priority: 1 → 2 → 4 → 3 → 5 → 6.

### 1. ML Algorithms — When to Use What (~20 min)

- [Machine Learning Algorithms for Beginners (Dataquest)](https://www.dataquest.io/blog/top-10-machine-learning-algorithms-for-beginners/) — Linear regression, logistic regression, decision trees, random forests, XGBoost, SVM, KNN, k-means, PCA. Clear "when to use" guidance.
- [Stanford CS229 Course Materials](https://cs229.stanford.edu/syllabus-new.html) — Free lecture notes on supervised learning, unsupervised learning, and learning theory. Deep mathematical foundations.

### 2. SageMaker Built-in Algorithms (~15 min)

- [AWS SageMaker Built-in Algorithms (official docs)](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html) — Source of truth. Which algorithm maps to which problem type.
- [SageMaker Common Information about Built-in Algorithms](https://docs.aws.amazon.com/sagemaker/latest/dg/common-info-all-im-models.html) — Input formats, instance recommendations, and how to use each algorithm.

### 3. Hyperparameter Tuning (~10 min)

- [Grid Search and Bayesian Optimization Simply Explained](https://towardsdatascience.com/a-step-by-step-introduction-to-bayesian-hyperparameter-optimization-94a623062fc) — Grid search, random search, and Bayesian optimization with intuitive examples.
- [SageMaker Automatic Model Tuning](https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html) — How SageMaker AMT implements Bayesian optimization at scale.

### 4. Foundation Models and Generative AI (~15 min)

- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/models.html) — Foundation models, fine-tuning, RAG, and guardrails. Key for GenAI questions.
- [Amazon Bedrock Developer Experience](https://aws.amazon.com/bedrock/developer-experience) — Model selection, customization, and API access patterns.
- [SageMaker JumpStart](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-jumpstart.html) — Pre-trained models and solution templates for quick deployment.

### 5. Model Evaluation and Debugging (~10 min)

- [SageMaker Clarify — Detect Bias and Explain Predictions](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-configure-processing-jobs.html) — Bias detection, SHAP values, and model explainability.
- [SageMaker Debugger](https://docs.aws.amazon.com/sagemaker/latest/dg/train-debugger.html) — Debug training jobs: vanishing gradients, overfitting, saturated activations.

### 6. Deep Learning Foundations (beyond the exam) (~15 min)

- [Stanford CS231n: CNNs for Visual Recognition (free notes)](https://cs231n.github.io/) — Backpropagation, CNNs, training neural networks. Excellent free resource.
- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — Visual explanation of the transformer architecture. Best free resource on attention.
- [Attention Is All You Need (original paper)](https://arxiv.org/abs/1706.03762) — The foundational transformer paper. Worth skimming sections 1-3.

---

## Domain 3: Deployment and Orchestration of ML Workflows (22% of exam)

~70 minutes total. Priority: 1 → 2 → 3 → 4 → 5.

### 1. SageMaker Inference Options (~15 min)

- [Inference Options in SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model-options.html) — Decision tree: real-time vs. batch vs. async vs. serverless. Must-read.
- [Deploy Models for Real-Time Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-deploy-models.html) — Endpoint creation, production variants, and traffic routing.
- [SageMaker Serverless Inference](https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints) — When to use serverless: intermittent traffic, cold starts, cost tradeoffs.
- [SageMaker Hosting FAQs](https://docs.aws.amazon.com/sagemaker/latest/dg/hosting-faqs.html) — Decision flowchart for choosing the right inference option.

### 2. MLOps and CI/CD (~20 min)

- [SageMaker Pipelines](https://aws.amazon.com/sagemaker/pipelines/) — Purpose-built ML workflow orchestration. Steps, conditions, and caching.
- [Automate ML Workflows (AWS Tutorial)](https://aws.amazon.com/tutorials/machine-learning-tutorial-mlops-automate-ml-workflows/) — Hands-on walkthrough of building a SageMaker Pipeline.
- [SageMaker MLOps Project Walkthrough](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-walkthrough.html) — End-to-end CI/CD with CodePipeline, CodeBuild, and SageMaker.
- [MLOps Deployment Best Practices for Real-Time Inference (AWS Blog)](https://aws.amazon.com/blogs/machine-learning/mlops-deployment-best-practices-for-real-time-inference-model-serving-endpoints-with-amazon-sagemaker/) — Blue/green, canary, and linear deployment strategies.

### 3. Containers and Compute (~15 min)

- [Use Pre-built SageMaker Docker Containers](https://docs.aws.amazon.com/sagemaker/latest/dg/docker-containers-prebuilt.html) — Framework containers for TensorFlow, PyTorch, etc.
- [Bring Your Own Container (BYOC)](https://docs.aws.amazon.com/sagemaker/latest/dg/docker-containers-create.html) — When and how to build custom containers for SageMaker.
- [SageMaker Neo](https://docs.aws.amazon.com/sagemaker/latest/dg/neo.html) — Model compilation for edge deployment and optimized inference.

### 4. Distributed Training (~10 min)

- [Distributed Training in SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training) — Data parallelism vs. model parallelism overview.
- [Distributed Training Strategies](https://docs.aws.amazon.com/sagemaker/latest/dg/distributed-training-strategies.html) — When to use each strategy and how SageMaker implements them.
- [The Science Behind SageMaker's Distributed Training (Amazon Science)](https://www.amazon.science/latest-news/the-science-of-amazon-sagemakers-distributed-training-engines) — Technical deep dive into SDP and SMP.

### 5. Infrastructure as Code (~10 min)

- [AWS CloudFormation SageMaker Resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SageMaker.html) — Defining endpoints, training jobs, and pipelines in CloudFormation.
- [SageMaker-Provided Project Templates](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-projects-templates-sm.html) — Pre-built MLOps templates with CI/CD baked in.

---

## Domain 4: ML Solution Monitoring, Maintenance, and Security (24% of exam)

~70 minutes total. Priority: 1 → 2 → 3 → 4 → 5.

### 1. Model Monitoring (~20 min)

- [SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html) — Data quality, model quality, bias drift, and feature attribution drift monitoring.
- [Monitor Data Quality](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-data-quality.html) — Baselines, constraints, and statistical tests for detecting data drift.
- [Bias Drift for Models in Production](https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-monitor-bias-drift.html) — Continuous bias monitoring with SageMaker Clarify.
- [Model Quality Metrics and CloudWatch](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-cw.html) — Automated alerting on model performance degradation.

### 2. Security and Access Control (~15 min)

- [Secure Deployment of SageMaker Resources (AWS Blog)](https://aws.amazon.com/blogs/security/secure-deployment-of-amazon-sagemaker-resources) — VPC config, encryption, IAM roles, and network isolation.
- [Securing SageMaker Studio with a Private VPC (AWS Blog)](https://aws.amazon.com/blogs/machine-learning/securing-amazon-sagemaker-studio-connectivity-using-a-private-vpc/) — VPC-only mode, PrivateLink, and security groups.
- [Securing SageMaker API Calls with PrivateLink (AWS Blog)](https://aws.amazon.com/blogs/machine-learning/securing-all-amazon-sagemaker-api-calls-with-aws-privatelink/) — VPC endpoints for SageMaker API and Runtime.

### 3. Cost Optimization (~10 min)

- [SageMaker Managed Spot Training](https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html) — Up to 90% savings with checkpointing for fault tolerance.
- [SageMaker Managed Warm Pools](https://docs.aws.amazon.com/sagemaker/latest/dg/train-warm-pools.html) — Reuse provisioned infrastructure to reduce startup latency.
- [Auto Scaling SageMaker Endpoints](https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html) — Target tracking, step scaling, and scheduled scaling policies.

### 4. Observability (~10 min)

- [SageMaker and CloudWatch Integration](https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html) — Metrics, logs, and alarms for training jobs and endpoints.
- [ML Best Practices: Model Monitoring (AWS Whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/ml-best-practices-healthcare-life-sciences/model-monitoring.html) — Data quality drift, model quality drift, and remediation patterns.

### 5. Governance and Compliance (~15 min)

- [SageMaker Model Registry](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html) — Model versioning, approval workflows, and lineage tracking.
- [SageMaker Model Cards](https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html) — Document model details for governance and responsible AI.
- [ML Lineage Tracking](https://docs.aws.amazon.com/sagemaker/latest/dg/lineage-tracking.html) — Track data, code, and model artifacts across the ML lifecycle.

---

## Cross-Domain: ML Foundations (beyond the exam)

These won't appear directly on the exam but deepen your understanding of the algorithms and techniques tested.

### Free Courses and Lecture Notes

- [Stanford CS229: Machine Learning (lecture notes)](https://cs229.stanford.edu/syllabus-new.html) — Andrew Ng's ML course. Supervised learning, unsupervised learning, learning theory.
- [Stanford CS231n: CNNs for Visual Recognition (notes)](https://cs231n.github.io/) — Neural network fundamentals, backpropagation, CNNs, training tricks.
- [fast.ai Practical Deep Learning](https://course.fast.ai/) — Free, code-first deep learning course. Top-down approach.
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — Free, interactive ML fundamentals with TensorFlow exercises.

### Key Concepts and Visual Explainers

- [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/) — Best visual explanation of self-attention and transformers.
- [The Illustrated BERT (Jay Alammar)](https://jalammar.github.io/illustrated-bert/) — How BERT works, masked language modeling, and fine-tuning.
- [The Illustrated Word2Vec (Jay Alammar)](https://jalammar.github.io/illustrated-word2vec/) — Word embeddings, skip-gram, and CBOW explained visually.
- [Distill.pub](https://distill.pub/) — Research journal with interactive ML visualizations (attention, feature visualization, etc.).

### Papers Worth Skimming

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762) — The transformer paper. Sections 1-3 are the most relevant.
- [XGBoost: A Scalable Tree Boosting System (Chen & Guestrin, 2016)](https://arxiv.org/abs/1603.02754) — The algorithm behind many SageMaker built-in use cases.
- [BERT: Pre-training of Deep Bidirectional Transformers (Devlin et al., 2018)](https://arxiv.org/abs/1810.04805) — Foundation for modern NLP transfer learning.

---

## AWS-Specific Study Resources (Free)

- [AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/) — Regularly updated with SageMaker tutorials and best practices.
- [AWS Skill Builder: ML Learning Plan](https://explore.skillbuilder.aws/learn/learning_plan/view/28/machine-learning-learning-plan) — Free digital training courses from AWS.
- [AWS Well-Architected Framework — Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html) — Best practices for ML workloads on AWS.
- [Jayendra Patil's MLA-C01 Learning Path](https://jayendrapatil.com/aws-certified-machine-learning-engineer-associate-mla-c01-exam-learning-path) — Comprehensive topic-by-topic study guide with links.

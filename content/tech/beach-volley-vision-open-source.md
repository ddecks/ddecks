+++
title = 'Open-Sourcing Beach Volley Vision'
description = 'The beach volleyball match-analysis project is now open source — code on GitHub, fine-tuned ball-tracking model on Hugging Face.'
date = 2026-08-31
tags = ['project', 'ai', 'beach', 'volleyball', 'computer-vision', 'open-source']
weight = 2
+++

## TL;DR

[Beach Volley Vision](/tech/beach-volley-vision/) — my system for turning raw beach
volleyball footage into stats — is now **open source**:

- **Code:** https://github.com/ddecks/beach-volley-vision
- **Fine-tuned model:** https://huggingface.co/deadfast/beach-volley-vision-models

Both are MIT licensed. Clone it, run it, break it, improve it.

## Why now

I started this to scratch my own itch: I wanted real analytics off match video without
paying an analyst or tagging every rally by hand. Since then, a few companies have shipped
polished tooling in the same space with far more resources than a solo nights-and-weekends
project can muster.

So rather than keep it in a private repo chasing a product dream that others are already
executing better, the more useful move is to put it in the open. The interesting parts —
adapting a small-fast-object tracker to volleyball, the rally/event state machine, the
annotation workflow — are worth sharing whether or not this ever becomes a product.

## What's in the box

- **Python ML pipeline** — detection (YOLOv8), multi-object tracking, court calibration
  via homography, ball tracking, and rally/event detection.
- **Rust analysis CLI** — reads the structured match JSON and computes stats.
- **Fine-tuned ball tracker** — a [TrackNetV3](https://github.com/qaz812345/TrackNetV3)
  model adapted to beach volleyball, published on
  [Hugging Face](https://huggingface.co/deadfast/beach-volley-vision-models).
- **Example data** — a small curated set of annotation CSVs and evaluation outputs so you
  can see the data formats and run the eval harness without hunting for footage.

## The model

Stock object detectors are bad at volleyballs — the ball is tiny, fast, and often occluded
by hands on contact. The fix was a heatmap-based tracker (TrackNetV3, originally built for
badminton shuttlecocks) fine-tuned on hand-annotated volleyball rallies.

The fine-tuned weights are a **derivative of TrackNetV3** and carry its MIT license forward,
with attribution to the original author. The trajectory-inpainting module is unchanged from
upstream, so grab that from the original repo if your pipeline uses it. Details are on the
[model card](https://huggingface.co/deadfast/beach-volley-vision-models).

## Getting started

```bash
git clone git@github.com:ddecks/beach-volley-vision.git
cd beach-volley-vision
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# Fine-tuned ball tracker (~130 MB) from Hugging Face
git lfs install
curl -L https://huggingface.co/deadfast/beach-volley-vision-models/resolve/main/tracknet_best.pt \
  -o data/models/tracknet_best.pt

pytest tests/ -v
```

See the repo's `ONBOARDING.md` and `docs/annotation-guide.md` for the full workflow.

## Where it goes from here

It's open source, so honestly — wherever people take it. If you play, coach, or just like
computer-vision side projects, PRs and issues are welcome. And if you've been beaten to your
own dream project too: shipping it into the open beats sitting on it.

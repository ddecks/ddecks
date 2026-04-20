+++
title = 'Beach Volley Vision: Building a Match Analyzer from Scratch'
description = 'Using YOLO, Python, and Rust to automatically analyze beach volleyball matches from video — detecting players, tracking the ball, and generating stats'
date = 2026-04-20
tags = ['project', 'ai', 'beach', 'volleyball', 'computer-vision']
weight = 3
+++

## What Is This

I'm building a system that takes raw beach volleyball match video and turns it into stats — automatically. Detect players, track the ball, classify events (serve, pass, set, attack), and spit out useful analytics. No manual tagging required (or at least, minimal).

The end goal: film a match, run it through the pipeline, and get back things like sideout percentage, serve placement heatmaps, and attack efficiency — the kind of data that pro teams have analysts for.

## Architecture

Two main pieces:

1. **Python ML pipeline** — handles video processing, object detection (YOLO), multi-object tracking (ByteTrack), court calibration, and event classification
2. **Rust analysis CLI** — reads the structured match JSON output and computes stats, trends, and reports

```
Video files
    │
    ▼
┌─────────────────────────────────────┐
│  Python ML Pipeline                 │
│  Detection → Tracking → Events     │
│  (YOLO)     (ByteTrack)            │
│  Court Calibration → Homography    │
└──────────────────┬──────────────────┘
                   │ match.json
                   ▼
┌─────────────────────────────────────┐
│  Rust Analysis CLI                  │
│  Stats • Reports • Trends • TUI    │
└─────────────────────────────────────┘
```

## What's Done

### Video ingestion & frame extraction

Wrote a script to pull frames from match footage at configurable intervals. Using OpenCV's VideoCapture — nothing fancy, but it works. Extracted ~700 frames from a test match for annotation.

### Player detection (stock YOLO)

YOLOv8n detects people out of the box with high accuracy. Beach volleyball is actually a great case for this — high contrast (skin/jerseys vs sand), only 4 players on court, minimal occlusion. Ran it on test footage and it picks up players reliably.

### Ball detection — the hard part

Stock YOLO is terrible at finding volleyballs. The ball is small (~20px in 1080p from distance), fast, and frequently occluded by hands during contacts. Ran a test and got detection in under 20% of frames — not usable.

So I annotated 700 frames in Roboflow (294 with YOLO-format labels, 174 containing actual ball bounding boxes, 120 negative frames where the ball isn't visible). Single class: `volleyball`.

### Detection preview videos

Generated two preview videos from the test match:
- `detection_preview.mp4` — player detection only
- `detection_with_ball.mp4` — players + stock ball detection (to see how bad it is)

## What's In Progress

### Fine-tuning YOLOv8 for ball detection

Currently training a fine-tuned YOLOv8n on my annotated dataset. Starting from pretrained COCO weights and training for up to 100 epochs with early stopping (patience=20).

Dataset split: 235 train / 59 val images. Training on CPU so it'll take a while — probably 5-6 hours. Early results after 12 epochs show mAP50 climbing from 0.026 to 0.073, so the model is learning.

If this gets to a reasonable detection rate (>50% of frames), I can fill gaps with trajectory interpolation. If not, the fallback is a TrackNet-style heatmap model designed specifically for small fast objects.

## What's Next

Roughly in order:

- **Evaluate the trained ball detector** — run it on test footage, measure detection rate, decide if it's good enough or needs more data/different approach
- **Player tracking** — ByteTrack via ultralytics (built-in, should be trivial with only 4 players)
- **Court calibration** — click 4 corners, compute homography to map pixels → real court coordinates (16m × 8m)
- **Ball tracking with interpolation** — Kalman filter + physics priors (parabolic arcs) to fill detection gaps
- **Event classification** — start with a rule-based state machine (beach volleyball has a rigid rally structure: serve → receive → set → attack → point), then add ML for edge cases
- **Rust stats engine** — parse match JSON, compute per-player and per-team stats, zone analysis

## Dev Log

### 2026-04-20

**Project kickoff day.** Set up the repo structure, Python pipeline package, and Rust analysis crate. Extracted frames from test match footage. Ran stock YOLOv8n — great for players, bad for the ball. Annotated 700 frames in Roboflow for ball detection. Kicked off fine-tuning training run. Wrote dataset preparation and training scripts.

Key numbers from today:
- Stock YOLO ball detection: ~18% of frames (not usable)
- Annotated dataset: 294 labeled images, 174 with ball annotations
- Training: YOLOv8n fine-tune, 100 epochs, mAP50 at 0.073 after 12 epochs and climbing

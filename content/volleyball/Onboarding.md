# Beach Volley Vision 🏐

Automated beach volleyball match analysis from video. Detect the ball, identify rallies, track players, attribute points, and generate stats — with minimal manual tagging.

## What This Does

Given a raw match video (phone on a tripod, YouTube broadcast, etc.), the pipeline:

1. **Detects the ball** frame-by-frame using a fine-tuned neural network (TrackNet)
2. **Identifies rallies** — when the ball is in play vs dead time between points
3. **Clips the video** into individual rally segments or a condensed highlight reel
4. (Coming soon) **Scores the match** by detecting who served and attributing points

## Current Status

The ball detection model works but isn't perfect — it's trained on ~40,000 frames across 33 rallies from 4 matches. More diverse training data = better accuracy. That's where you come in.

### What's Working
- Ball detection via TrackNet (fine-tuned on beach volleyball footage)
- Rally detection state machine with multiple filtering gates
- Video condensing and per-rally clip splitting
- Fast inference (~15-50 fps depending on hardware)
- Player detection and tracking (YOLOv8 + BoT-SORT)
- Court calibration (manual corner annotation → homography)

### What Needs Help (Your Role)
- **Ball annotation** — reviewing model predictions and correcting errors
- **Expanding training data** — labeling new clips from different camera angles, lighting, ball colors
- **Validation** — watching split clips and flagging where rally boundaries are wrong

## Architecture Overview

```
Raw match video
    │
    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Ball Detect  │────▶│ Rally Detect │────▶│ Video Split  │
│ (TrackNet)   │     │ (state mach) │     │ (FFmpeg)     │
└──────────────┘     └──────────────┘     └──────────────┘
```

The model looks at 8 consecutive video frames and predicts where the ball is in each frame (as a heatmap). The rally detector watches that signal over time — when the ball is consistently detected and moving, a rally is in progress. When it disappears for 2+ seconds, the point is over.

## Annotation Workflow

This is the primary task for contributors. The workflow is:

### 1. Get a clip to annotate
You'll receive pre-cut video clips (~60 seconds each, ~1800 frames). These are segments of full matches already split into manageable chunks.

### 2. Run the model's predictions
The model generates its best guess for ball position in every frame. These predictions are saved as a CSV:
```
frame,x,y,visibility,confidence
0,412,287,1,0.82
1,418,279,1,0.75
2,0,0,0,0.0        ← model thinks no ball here
3,425,268,1,0.91
...
```

### 3. Review and correct
Using the annotation tool, you'll scroll through frames and:
- **Confirm** correct predictions (ball is where the model says)
- **Correct** wrong predictions (ball is elsewhere — click the right spot)
- **Add** missed detections (model said no ball, but ball is visible)
- **Remove** false positives (model said ball is here, but it's actually a shoe/hand/sand reflection)

### 4. Submit corrected annotations
The corrected CSV gets added to the training dataset. The model retrains and gets better at exactly the types of frames it was getting wrong.

## What Makes a Good Annotation

- **Only annotate when the ball is clearly visible.** If you can't see it, mark as not visible.
- **Center of the ball.** Click the middle, not the edge.
- **Between rallies:** the ball might be sitting on sand, being tossed to the server, etc. These frames should generally be marked as NOT visible (we don't want the model triggering on dead-ball situations).
- **Fast-moving ball (motion blur):** still annotate — mark the center of the blur streak. The model needs to learn this.
- **Ball partially occluded by player:** annotate if you can tell where center is. Skip if it's fully hidden.

## Data Diversity Goals

We need training data from varied conditions to make the model robust:

| Condition | Status | Priority |
|-----------|--------|----------|
| Outdoor daytime (sunny) | ✅ Have plenty | Low |
| Outdoor overcast | ⚠️ Some | Medium |
| Different camera heights | ⚠️ Mostly courtside | High |
| Different ball colors (yellow, blue/yellow) | ⚠️ Mostly yellow Mikasa | High |
| Night/indoor lighting | ❌ None | Medium |
| Broadcast footage (elevated, wide angle) | ⚠️ Some | Medium |

## Tech Stack

- **Python 3.12**, PyTorch, OpenCV, NumPy
- **TrackNet** (neural network for ball detection)
- **YOLOv8** (player detection)
- **FFmpeg** (video cutting)

## Getting Started

Setup instructions will be provided separately once you have repo access. The short version:

```bash
git clone <repo-url>
cd beach-volley-vision
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Download model weights (link provided separately)
# Download annotation clips (link provided separately)

# Verify setup
pytest tests/ -v  # should pass in <2 seconds

# Run predictions on a clip
python scripts/preannotate_tracknet.py --clips data/labeling_clips/clip01.mp4 \
    --weights data/models/tracknet_best.pt --format csv

# Launch annotation tool
python scripts/annotate_ball.py data/labeling_clips/clip01.mp4 \
    --predictions data/predictions/clip01_pred.csv
```

## Questions?

Reach out to me, or ask AI. 

+++
title = 'Building cert-drill: A CLI Study Tool in Rust in Half a Day'
description = 'How I built a terminal-based certification exam tool with AI-assisted development, and what I learned along the way'
date = 2026-04-14
tags = ['rust', 'cli', 'aws', 'certification', 'ai', 'project']
weight = 1
+++

## The Problem

I was studying for the AWS Solutions Architect Associate (SAA-C03) exam. My study method was simple: take practice questions, write down my answers with my reasoning, then have an AI review not just what I got right or wrong, but *why* I chose each answer.

It worked great. The AI could spot misconceptions in my thinking — like when I was confident that DAX could cache RDS queries (it can't, it's DynamoDB-only) or when I kept confusing FSx for Lustre with FSx for Windows.

But the workflow was clunky. I was writing answers in a plain text file, manually formatting them, then copy-pasting into AI chats. The grading was done by the AI too, which meant I couldn't quickly check my score without a full conversation.

I wanted a tool that:
- Presents questions in the terminal (where I already live)
- Captures my answer AND my reasoning
- Auto-grades against an answer key
- Exports results in a format optimized for AI review
- Tracks progress by domain over time
- Works on my phone (Termux) for studying on the go

Nothing like this existed. Flashcard tools are everywhere, but none of them do multiple-choice exam simulation with reasoning capture.

So I built it.

## The Build

I chose Rust for a few reasons:
- Single binary — no runtime dependencies, easy to install anywhere including Termux
- The CLI ecosystem is mature (clap, dialoguer, colored)
- It's a resume piece, and Rust stands out more than Python for CLI tools
- I wanted to learn more Rust

The entire tool was built in a single afternoon session with AI assistance. Here's roughly how it went:

### Hour 1: Scaffold and Core Flow

Started with the project structure and data models. The key insight was keeping everything in human-readable formats:
- Questions in structured markdown (easy to author)
- Answer keys in TOML (easy to parse)
- User attempts in TOML (easy for AI to read)

The core `take` command presents questions one at a time, lets you type your answer (A, B, C, D), then prompts for your reasoning. Navigation with `>`, `<`, `#5` to jump around, `!s` to submit.

### Hour 2: Grading and Progress

Auto-grading compares your answers against the key and shows results with color-coded markers:
- ✓ (your answer, correct) in green
- ✗ (your answer) in red  
- ← correct in green

For correct answers, it just shows your reasoning and "Nice." — no need to reiterate the explanation. For wrong answers, it shows your reasoning alongside the correct explanation so you can see where your thinking went wrong.

Progress tracking aggregates scores by domain across all attempts, showing you exactly where you're weak.

### Hour 3: Features That Matter

This is where it got fun. Each feature took 15-30 minutes:

**Cram mode** (`--cram`) — skips the reasoning prompt for speed drilling. Just letters, rapid fire.

**Domain filtering** (`--domain "Secure"`) — only study questions from a specific exam domain.

**Random mode** (`--random`) — shuffle question order so you're not just memorizing sequences.

**Import** — parse existing markdown answer sheets. I had already written answers in a plain text file, so I built a parser that handles formats like `1. D - reasoning here #shotInDark`.

**Flashcards** — reveal-and-rate mode for drilling concepts. Rate yourself: forgot, fuzzy, got it.

### Hour 4: The AI Integration

This is the part I'm most proud of. The `--ai-context` export flag generates output specifically formatted for AI review:

```
I just took a practice exam for aws-saa-c03 and scored 14/24 (58.3%).
Below are the questions I got wrong along with my reasoning.
Please review my thought process, identify misconceptions, and help me understand what I got wrong.

❌ Q62
A company runs a relational database on RDS MySQL. They need to cache frequently accessed query results...

  C) Amazon DynamoDB DAX (my answer) ← correct: B) Amazon ElastiCache for Redis
  My reasoning: Cache of any kind sounds good here since it's a db I want to say DAX
  Explanation: ElastiCache for Redis is the standard caching layer for relational databases. DAX is only for DynamoDB.
```

Pipe it to your clipboard: `cert-drill export aws-saa-c03 --ai-context | pbcopy`

The tool also includes `CLAUDE.md` and `llms.txt` files — AI context documents that help any AI assistant understand the project structure, data formats, and how to interpret the reasoning data. This is a pattern I think more projects should adopt.

### Post-Submit Flow

After submitting a quiz, your score shows automatically. Then you get a menu:

```
What next?
  1  — show all results
  2  — show only missed
  3  — export as markdown
  4  — export as AI review context
  5  — done
```

No need to remember separate commands. Everything flows naturally from the quiz session.

## The Exam Pack Format

Anyone can create an exam pack. It's just a directory with 3-4 files:

```
exams/my-cert/
├── exam.toml         # metadata (title, domains, passing score)
├── questions.md      # structured markdown questions
├── answers.toml      # answer key with explanations
└── flashcards.md     # optional flashcards
```

The SAA-C03 pack ships with the repo: 100 questions across 4 domains, 119 flashcards across 16 topics, full answer key with explanations.

## What I Learned (About AWS)

Building the tool was the easy part. The hard part was the actual studying. Here's where I stood after going through all 100 questions:

| Domain | Score |
|--------|-------|
| Secure Architectures | ~70-75% |
| Resilient Architectures | ~75% |
| High-Performing Architectures | 58.3% ⚠️ |
| Cost-Optimized Architectures | 85% |

Domain 3 was rough. My misses clustered around service selection — knowing which AWS service does what:
- DAX is DynamoDB-only, ElastiCache is for everything else
- Firehose delivers to S3/OpenSearch (managed), Kinesis Data Streams is for custom processing
- Glue ETL transforms data, Athena queries it, QuickSight visualizes it
- Redshift is for petabyte analytics, Aurora is for transactional workloads

The good news: these are memorization gaps, not conceptual ones. The flashcards I built from my weak areas are specifically designed to drill these distinctions.

## What I Learned (About Building)

**AI-assisted development is real.** The entire tool — scaffold, core flow, grading, progress tracking, flashcards, export, import, 119 flashcards, full documentation — was built in one session. Not because AI wrote all the code, but because the iteration loop was incredibly fast. Describe what you want → get a working implementation → test it → describe the next thing.

**Design for AI from the start.** Including `CLAUDE.md` and `llms.txt` isn't just a nice touch — it fundamentally changes how useful the tool is. When you paste your results into an AI chat, the AI already understands the data format, knows that reasoning fields are the most valuable data, and can give targeted feedback.

**Solve your own problems.** The best portfolio projects are tools you actually use. I'm going to use cert-drill to study for this exam and probably the next one too. That motivation shows in the design decisions.

## The Landscape

cert-drill isn't the first terminal study tool, but it fills a gap none of the others cover. [hashcards](https://github.com/eudoxia0/hashcards) (Rust, 1.1k stars) is excellent for spaced repetition with plain text flashcards and uses the FSRS algorithm for scheduling. [flashdown](https://github.com/SteveRidout/flashdown) (TypeScript) has a beautiful TUI and cram mode. [markdown-flashcards](https://github.com/bttger/markdown-flashcards) (Go) follows the UNIX philosophy with flat markdown files and even runs on Termux.

All of them are flashcard tools. None do multiple-choice exam simulation, none capture your reasoning, and none export structured data for AI review. That's the niche — cert-drill is built for the specific workflow of "take a practice exam, record your thinking, then have an AI tutor review your misconceptions." If you just need flashcards, hashcards is probably better. If you need exam simulation with AI integration, this is it.

## About the SAA-C03

The AWS Solutions Architect Associate exam is 65 questions in 130 minutes (~2 min per question). 50 are scored, 15 are unscored (you don't know which). Passing is 720/1000, roughly 72%. Four domains: Secure Architectures (30%), Resilient Architectures (26%), High-Performing Architectures (24%), and Cost-Optimized Architectures (20%). The exam tests breadth more than depth — you need to know which service to pick for a given scenario, not how to configure it in detail. AWS offers free practice exams on Skill Builder, and employees at many companies get 50% off the real exam.

## Generating the Practice Questions

The 100-question exam pack that ships with cert-drill was generated with AI, but not blindly. Here's the prompt strategy that worked:

I started by giving the AI the official [SAA-C03 exam guide](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html) and asked it to generate questions weighted by domain — 30 questions for Secure, 26 for Resilient, 24 for High-Performing, 20 for Cost-Optimized — matching the actual exam distribution. Each question needed four plausible answer choices where the distractors were common misconceptions, not obviously wrong.

The key prompt detail: I asked for explanations that don't just say "B is correct" but explain *why each wrong answer is wrong*. This is what makes the grading output useful — when you miss a question, you see not just the right answer but why your choice was a trap.

For the 119 flashcards, I took a different approach. Instead of generating them from scratch, I fed the AI my actual study session results — every question I missed, my reasoning for each wrong answer, and the weak areas I'd identified. The AI then generated flashcards targeted at my specific gaps: DAX vs ElastiCache, Firehose vs Kinesis Data Streams, the EBS IOPS chart, S3 storage class decision trees. These aren't generic flashcards — they're personalized to the misconceptions I actually had.

The lesson: AI-generated study material is only as good as the context you give it. Generic "make me 100 AWS questions" produces generic results. "Here are the 31 questions I got wrong, here's what I was thinking for each one, generate flashcards that correct these specific misconceptions" produces something genuinely useful.

## Exam Update

<!-- TODO: Update this section after the exam on Monday April 20 -->

*Exam scheduled for Monday, April 20. Will update with results.*

---

## Try It

```bash
git clone https://github.com/ddecks/cert-drill.git
cd cert-drill
cargo install --path .
cert-drill list
cert-drill take aws-saa-c03 --range 1-10
```

Works on Linux, macOS, Windows, and Termux (Android).

[GitHub →](https://github.com/ddecks/cert-drill)

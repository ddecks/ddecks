+++
title = 'Blog Image Hosting Architecture'
description = 'How I built a self-monitoring image CDN for my blog using S3, CloudFront, and Lambda — for under $0.05/month'
date = 2026-04-16
tags = ['aws', 'architecture', 'project', 'cloudfront', 's3', 'lambda']
weight = 2
+++

## The Problem

I needed image hosting for this blog. Adding images directly to the GitHub repo would bloat it over time, and I wanted something I controlled with usage monitoring and cost protection.

## The Architecture

{{< mermaid >}}
graph LR
    subgraph Viewers
        B[Blog Reader]
        H[Hotlinker]
    end

    subgraph AWS
        CF[CloudFront CDN]
        S3I[S3: Images]
        S3L[S3: Logs]
        LP[Lambda: Log Processor]
        CB[Lambda: Circuit Breaker]
        SNS[SNS: Alerts]
        BUD[AWS Budget]
        R53[Route 53]
        ACM[ACM Certificate]
    end

    B -->|HTTPS| R53
    H -->|HTTPS| R53
    R53 -->|images.midnightdmdecke.click| CF
    ACM -.->|TLS| CF
    CF -->|OAC| S3I
    CF -->|Access Logs| S3L
    S3L -->|S3 Event| LP
    LP -->|Hotlink Alert| SNS
    LP -->|Daily Warning| SNS
    LP -->|Request Spike| CB
    CB -->|Disable CF| CF
    CB -->|Alert| SNS
    BUD -->|Budget Exceeded| CB
    SNS -->|Email| E[kinaidecker@gmail.com]
{{< /mermaid >}}

## How It Works

**Serving images:** CloudFront sits in front of a private S3 bucket. The bucket has no public access — CloudFront authenticates via Origin Access Control (OAC). Route 53 points `images.midnightdmdecke.click` to the distribution with a free ACM certificate for HTTPS.

**Monitoring:** CloudFront writes access logs to a separate S3 bucket. Each log file triggers a Lambda function that:
- Parses the log and checks the `Referer` header
- Alerts via SNS if someone hotlinks an image from a non-blog domain
- Tracks daily request counts in a state file
- Writes daily summaries (top pages, unique visitors, edge locations)

**Circuit breaker:** Two independent kill switches:

| Trigger | Threshold | Action |
|---|---|---|
| Daily requests | 1,000 | Email warning |
| Daily requests | 5,000 | Auto-disable CloudFront |
| Monthly AWS bill | $5 | Auto-disable CloudFront |

If either trips, a second Lambda disables the CloudFront distribution and sends an alert. Re-enabling is a single script: `~/cf-reenable.sh`.

**Log lifecycle:** Lambda deletes raw logs after processing. S3 lifecycle rules act as a safety net (1-day expiry on raw, 90-day on summaries).

## Cost

| Resource | Monthly Cost |
|---|---|
| S3 storage (~1GB) | $0.023 |
| CloudFront (free tier) | $0.00 |
| Lambda (free tier) | $0.00 |
| ACM certificate | $0.00 |
| Route 53 hosted zone | $0.50 |
| **Total** | **~$0.52** |

## Infrastructure as Code

Two CloudFormation stacks manage everything:
- `blog-images` — S3 bucket, CloudFront, ACM cert, Route 53 record, IAM upload role
- `blog-images-monitoring` — Log bucket, Lambda functions, SNS topic, budget alarm

## Uploading Images

```bash
aws s3 cp photo.jpg s3://$bucket/posts/my-post/photo.jpg
```

Then in a Hugo post:
```markdown
{{</* figure src="https://images.midnightdmdecke.click/posts/my-post/photo.jpg" alt="description" width="300px" */>}}
```
{{< figure src=https://images.midnightdmdecke.click/posts/20250125_170028.jpg alt=20250125_170028.jpg width=300px >}}
{{< figure src=https://images.midnightdmdecke.click/posts/20250509_160324.jpg alt=20250509_160324.jpg width=300px >}} 
{{< figure src=https://images.midnightdmdecke.click/posts/20251011_180935.jpg alt=20251011_180935.jpg width=300px >}} 
{{< figure src=https://images.midnightdmdecke.click/posts/20260106_190734.jpg alt=20260106_190734.jpg width=300px >}} 
{{< figure src=https://images.midnightdmdecke.click/posts/20260322_154745.jpg alt=20260322_154745.jpg width=300px >}}
{{< figure src=https://images.midnightdmdecke.click/posts/Drawing_assist_20251231_170426.jpg alt=Drawing_assist_20251231_170426.jpg width=300px >}} Drawing_assist_20251231_170426.jpg

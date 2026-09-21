---
layout: post
title: "Harness-of-Harness (HoH) Architecture: Long-Horizon Execution without Context Bloat"
date: 2026-09-21
author: Namit Sehgal
excerpt: "Executive Summary When autonomous agents run complex, multi-day engineering or operational tasks, single prompt-loop designs inevitably fail. Token contexts overflow, error logs pollute working memory"
hashnode_url: https://articles.namitsehgal.com/harness-of-harness-hoh-architecture-long-horizon-execution-without-context-bloat
---

### Executive Summary

When autonomous agents run complex, multi-day engineering or operational tasks, single prompt-loop designs inevitably fail. Token contexts overflow, error logs pollute working memory, and models end up in unproductive debugging cycles.

The **Harness-of-Harness (HoH)** architecture solves this by separating execution across three specialized agent roles. It isolates runtime logs using **Progressive Disclosure**, tracking state strictly through separate **Artifact** and **Evidence** pipelines.

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/04b03d37-f8c6-4907-8ff6-e6cf19a3ab12.png)

### Dual State Management: Artifact vs. Evidence

To avoid flooding the model with raw execution logs, HoH splits state tracking into two explicit channels:

1. **Artifact State (A\_t):** The authoritative, version-controlled repository of generated assets (source code, configuration manifests, system schemas).
2. **Evidence State (E\_t):** Verifiable metrics and evaluation data generated during testing (test output, pass/fail matrices, coverage metrics, performance benchmarks).

### The Progressive Disclosure Pattern

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/8d07fdaa-289b-4b9b-9d15-4beb5142b020.png)

Instead of sending raw log output back into the primary agent prompt window, raw execution logs are offloaded directly to disk. An **Evidence Parser Engine** extracts key stack traces and failure signatures, generating a compact **Error Delta**.

Only this succinct summary is passed back to the Project Planner, ensuring context windows remain focused on task execution rather than debug noise.

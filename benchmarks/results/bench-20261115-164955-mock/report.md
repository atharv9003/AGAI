# CodeFix AI benchmark — `bench-20261115-164955-mock`

> **MOCK RUN** — agents were played by the offline oracle mock. These numbers validate the harness and pipeline mechanics only; they are NOT model results.

4 runs · 2 bugs · architectures: developer, enduser

## Headline comparison

| Metric | developer | enduser |
|---|---|---|
| Resolved (fresh-clone full suite green) | 2/2 (100%) | 2/2 (100%) |
| Previously-failing test green | 2/2 | 2/2 |
| Judge verdict = pass | 2/2 (100%) | 2/2 (100%) |
| Judge verdict = partial | 0 | 0 |
| **Judge accuracy** (agrees with tests) | 100% | 100% |
| Mean Fixer attempts | 2.00 | 2.00 |
| Runs needing a retry | 2 | 2 |
| Escalated to human | 0 | 0 |
| Errors | 0 | 0 |
| Reference fix: exact match | 2/2 (100%) | 2/2 (100%) |
| Reference fix: edit similarity (0-1) | 1.00 | 1.00 |
| Reference fix: same file(s) changed | 2/2 | 2/2 |
| Mean wall-clock / run | 51.6s | 24.5s |
| Wall-clock std-dev | 29.1s | 1.8s |
| Mean pipeline cost / run | $0.0000 | $0.0000 |
| Total pipeline cost | $0.000 | $0.000 |
| Mean LLM calls / run | 4.0 | 4.0 |
| Mean tokens / run | 6636 | 5843 |
| Mean envelope size (bytes) | 285 | 285 |

## Per-agent mean latency (seconds per run)

| Agent | developer | enduser |
|---|---|---|
| Diagnoser | 0.4 | 0.2 |
| Fixer | 4.2 | 0.4 |
| Tester | 3.3 | 3.2 |
| PR agent | 0.4 | 0.5 |
| Manager (LLM time) | 0.0 | 0.0 |

Bottleneck agent per architecture: **developer** → fixer, **enduser** → tester

## Failure-stage breakdown (non-passing runs)

_No failures._

## Judge vs objective tests (all architectures)

| Judge \ Tests | green | red |
|---|---|---|
| pass | 4 | 0 |

## Per-bug outcomes (✅ resolved · ❌ not resolved · attempts)

| Bug | difficulty | developer | enduser |
|---|---|---|---|
| js01-slugify-global | easy | ✅2 | ✅2 |
| py05-region-case | medium | ✅2 | ✅2 |

## By difficulty (resolved / runs)

| Difficulty | developer | enduser |
|---|---|---|
| easy | 1/1 | 1/1 |
| medium | 1/1 | 1/1 |

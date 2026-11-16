# CodeFix AI benchmark — `bench-20261115-180009`

2 runs · 2 bugs · architectures: hierarchical

## Headline comparison

| Metric | hierarchical |
|---|---|
| Resolved (fresh-clone full suite green) | 2/2 (100%) |
| Previously-failing test green | 2/2 |
| Judge verdict = pass | 2/2 (100%) |
| Judge verdict = partial | 0 |
| **Judge accuracy** (agrees with tests) | 100% |
| Mean Fixer attempts | 1.00 |
| Runs needing a retry | 0 |
| Escalated to human | 0 |
| Errors | 0 |
| Reference fix: exact match | 2/2 (100%) |
| Reference fix: edit similarity (0-1) | 1.00 |
| Reference fix: same file(s) changed | 2/2 |
| Mean wall-clock / run | 65.8s |
| Wall-clock std-dev | 8.7s |
| Mean pipeline cost / run | $0.0357 |
| Total pipeline cost | $0.071 |
| Mean LLM calls / run | 4.5 |
| Mean tokens / run | 18887 |
| Mean envelope size (bytes) | 408 |

## Per-agent mean latency (seconds per run)

| Agent | hierarchical |
|---|---|
| Diagnoser | 24.0 |
| Fixer | 15.1 |
| Tester | 1.8 |
| PR agent | 0.5 |
| Manager (LLM time) | 0.0 |

Bottleneck agent per architecture: **hierarchical** → diagnoser

## Failure-stage breakdown (non-passing runs)

_No failures._

## Judge vs objective tests (all architectures)

| Judge \ Tests | green | red |
|---|---|---|
| pass | 2 | 0 |

## Per-bug outcomes (✅ resolved · ❌ not resolved · attempts)

| Bug | difficulty | hierarchical |
|---|---|---|
| js01-slugify-global | easy | ✅1 |
| py05-region-case | medium | ✅1 |

## By difficulty (resolved / runs)

| Difficulty | hierarchical |
|---|---|
| easy | 1/1 |
| medium | 1/1 |

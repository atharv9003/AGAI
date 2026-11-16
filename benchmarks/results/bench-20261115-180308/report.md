# CodeFix AI benchmark — `bench-20261115-180308`

140 runs · 16 bugs · architectures: hierarchical, p2p, sequential

## Headline comparison

| Metric | hierarchical | p2p | sequential |
|---|---|---|---|
| Resolved (fresh-clone full suite green) | 47/47 (100%) | 46/46 (100%) | 46/47 (98%) |
| Previously-failing test green | 47/47 | 46/46 | 46/47 |
| Judge verdict = pass | 46/47 (98%) | 46/46 (100%) | 46/46 (100%) |
| Judge verdict = partial | 1 | 0 | 0 |
| **Judge accuracy** (agrees with tests) | 98% | 100% | 100% |
| Mean Fixer attempts | 1.00 | 1.00 | 1.00 |
| Runs needing a retry | 0 | 0 | 0 |
| Escalated to human | 0 | 0 | 0 |
| Errors | 0 | 0 | 0 |
| Reference fix: exact match | 34/47 (72%) | 35/46 (76%) | 37/47 (79%) |
| Reference fix: edit similarity (0-1) | 0.95 | 0.95 | 0.98 |
| Reference fix: same file(s) changed | 47/47 | 46/46 | 46/47 |
| Mean wall-clock / run | 62.1s | 58.5s | 55.9s |
| Wall-clock std-dev | 23.0s | 12.5s | 11.2s |
| Mean pipeline cost / run | $0.0336 | $0.0309 | $0.0280 |
| Total pipeline cost | $1.577 | $1.423 | $1.317 |
| Mean LLM calls / run | 4.2 | 4.1 | 3.9 |
| Mean tokens / run | 16549 | 15500 | 13919 |
| Mean envelope size (bytes) | 396 | 469 | 460 |

## Per-agent mean latency (seconds per run)

| Agent | hierarchical | p2p | sequential |
|---|---|---|---|
| Diagnoser | 27.7 | 27.3 | 24.9 |
| Fixer | 11.7 | 8.6 | 8.2 |
| Tester | 1.9 | 1.9 | 1.9 |
| PR agent | 0.4 | 0.4 | 0.4 |
| Manager (LLM time) | 0.0 | 0.0 | 0.0 |

Bottleneck agent per architecture: **hierarchical** → diagnoser, **p2p** → diagnoser, **sequential** → diagnoser

## Failure-stage breakdown (non-passing runs)

| Stage | hierarchical | p2p | sequential |
|---|---|---|---|
| None | 0 | 0 | 1 |

## Judge vs objective tests (all architectures)

| Judge \ Tests | green | red |
|---|---|---|
| pass | 138 | 0 |
| partial | 1 | 0 |

## Per-bug outcomes (✅ resolved · ❌ not resolved · attempts)

| Bug | difficulty | hierarchical | p2p | sequential |
|---|---|---|---|---|
| js01-slugify-global | easy | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| js02-truncate-length | easy | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| js03-template-falsy | medium | ✅1 ✅1 ✅1 | ✅1 ✅1 | ✅1 ✅1 ❌1 |
| js04-camelcase-index | medium | ✅1 ✅1 | ✅1 ✅1 | ✅1 ✅1 |
| py01-subtotal-skips-last | easy | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py02-discount-returns-discount | easy | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py03-rounding-truncates | medium | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py04-reserve-exact-stock | easy | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py05-region-case | medium | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py06-free-shipping-threshold | medium | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py07-promo-end-inclusive | medium | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py08-mutable-default | hard | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py09-snapshot-aliasing | medium | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py10-bulk-tier-boundary | easy | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py11-sku-dashes | hard | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |
| py12-split-leftover | medium | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 | ✅1 ✅1 ✅1 |

## By difficulty (resolved / runs)

| Difficulty | hierarchical | p2p | sequential |
|---|---|---|---|
| easy | 18/18 | 18/18 | 18/18 |
| medium | 23/23 | 22/22 | 22/23 |
| hard | 6/6 | 6/6 | 6/6 |

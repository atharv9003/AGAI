<#
.SYNOPSIS
  Live prompt-variant and persona sweeps, sized to reuse the main benchmark's baseline.

.DESCRIPTION
  The 140-run architecture benchmark already contains, for every bug, the
  hierarchical / react / default / developer arm with three repetitions. That IS the baseline,
  so these sweeps run only the NON-default levels and are compared against it pairwise on the
  same bugs (see codefix/eval/compare.py). 36 runs instead of 112.

    B  prompt variants    8 bugs x {fewshot, react-reflect}            16 runs
    C  agent personas     4 bugs x {senior, novice, security}          12 runs
    D  reporter persona   8 bugs x {enduser}  (no stack trace)          8 runs

  Runs detached so it survives the shell that started it. Progress: bench_prompts.log
#>
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$py = ".\.venv\Scripts\python.exe"
$B8 = "py01-subtotal-skips-last,py03-rounding-truncates,py05-region-case,py08-mutable-default,py09-snapshot-aliasing,py11-sku-dashes,js01-slugify-global,js03-template-falsy"
$B4 = "py05-region-case,py08-mutable-default,js01-slugify-global,js03-template-falsy"

"### B: prompt variants (fewshot, react-reflect) x 8 bugs = 16 runs"
& $py -m codefix.cli.main bench --arch hierarchical --bugs $B8 `
    --variants fewshot,react-reflect --personas default --runs 1 --llm live

"### C: agent personas (senior, novice, security) x 4 bugs = 12 runs"
& $py -m codefix.cli.main bench --arch hierarchical --bugs $B4 `
    --variants react --personas senior,novice,security --runs 1 --llm live

"### D: reporter persona (enduser, no stack trace) x 8 bugs = 8 runs"
& $py -m codefix.cli.main bench --arch hierarchical --bugs $B8 `
    --variants react --personas default --reporters enduser --runs 1 --llm live

"### ALL SWEEPS DONE"

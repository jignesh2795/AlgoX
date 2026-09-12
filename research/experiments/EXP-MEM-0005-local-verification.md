# EXP-MEM-0005 — Local Verification Protocol

**Status:** IMPLEMENTED — execution is intentionally local

## Objective

Verify AlgoX memory and governance behavior without relying on GitHub Actions or hosted CI.

## Rationale

AlgoX development must remain usable with a normal GitHub account. GitHub stores source, research records, and the pull request; local Python execution is the verification environment.

## Verification layers

### V1 — Python compilation

```bash
python tools/local_verify.py
```

The runner compiles the `algox/` package before executing the benchmark.

### V2 — Memory benchmark

The same command executes `EXP-MEM-0001` through the existing benchmark entry point:

```bash
python experiments/memory_benchmark.py
```

### V3 — Full test suite

When `pytest` is installed locally:

```bash
python tools/local_verify.py --pytest
```

This runs the complete repository test suite after compilation and the memory benchmark.

## Evidence policy

Do not mark a workload as executed merely because its code exists. Record actual local output, environment, Python version, package versions, and date when measurements are published.

Latency is machine-dependent. Repository documentation must not invent timing results.

## Expected workflow

```text
edit locally
   ↓
python tools/local_verify.py --pytest
   ↓
inspect failures
   ↓
fix
   ↓
repeat
   ↓
git commit
   ↓
git push research/algo-trading-github
   ↓
review PR #1
```

GitHub Actions is not a required dependency for AlgoX verification.

## Next evidence

After local verification is actually run, record:

- pass/fail counts;
- Python/runtime environment;
- benchmark output;
- p50/p95 measurements for repeated benchmark runs;
- any failures and their root causes;
- reproducibility notes.

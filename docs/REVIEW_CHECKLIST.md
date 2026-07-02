# Review Checklist

For every non-trivial task, Codex must perform the role reviews below before reporting completion.

Codex must not say "completed" unless every required role passes or a blocker is clearly reported.

## 1. Project Manager Review

- Pass / Fail:
- Findings:
- Fixes made:
- Remaining blockers:
- Hard requirement: no final completion if Macro Dashboard has no visible macro raw data, provider timestamps, or missing-data warning.

## 2. Developer Review

- Pass / Fail:
- Findings:
- Fixes made:
- Remaining blockers:

## 3. Localization Review

- Pass / Fail:
- Findings:
- Fixes made:
- Remaining blockers:

## 4. UI/UX Review

- Pass / Fail:
- Findings:
- Fixes made:
- Remaining blockers:

## 5. Investment Analyst Review

- Pass / Fail:
- Findings:
- Fixes made:
- Remaining blockers:
- Hard requirement: verify FRED raw data, market proxy raw data, score diagnostics, timestamps, and fallback warnings are visible before trusting market scores.

## 6. QA Tester Review

- Pass / Fail:
- Findings:
- Fixes made:
- Remaining blockers:
- Hard requirement: `python scripts/enforce_macro_data_gate.py` must pass for any macro/scoring UI change.

## 7. Security Officer Review

- Pass / Fail:
- Findings:
- Fixes made:
- Remaining blockers:

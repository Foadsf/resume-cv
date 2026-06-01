# Evidence Method

This repository treats a CV claim as publishable only when it is tied to evidence and phrased at the right confidence level.

## Evidence Levels

| Level | Meaning | CV use |
|---|---|---|
| `verified` | Confirmed by portfolio, gap report, KG module, or source document | Safe for resume and CV. |
| `probable` | Strong evidence exists, but ownership or scope needs conservative wording | Use careful verbs such as "supported", "worked across", or "led workstreams". |
| `needs-confirmation` | Mentioned but not yet backed by enough evidence | Keep out of public resumes. |
| `private/internal` | Personal, legal, salary, family, or confidential detail | Never include in public CVs. |

## Claim Rules

- Every metric needs an evidence source.
- Strong verbs such as `secured`, `owned`, `architected`, and `founded` need a matching claim entry.
- Do not convert portfolio text directly into resume text; rewrite it as role-specific evidence.
- Prefer concrete nouns over adjectives: project, mechanism, method, artifact, platform, outcome.
- Do not disclose internal customer details or program codes unless they are already approved for external use.

## Workflow

1. Add or update a claim in `data/claims.yml`.
2. Mark allowed variants and confidence level.
3. Write the resume/CV bullet.
4. Run `python tools\detect_cv_slop.py <variant>`.
5. Run `python tools\validate_claims.py <variant>`.
6. Build the PDF and inspect layout manually.

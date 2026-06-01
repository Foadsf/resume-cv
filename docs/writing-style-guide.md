# Writing Style Guide

The writing goal is senior, technical, and evidence-based. Avoid hype and avoid generic AI phrasing.

## Preferred Bullet Pattern

Use one of these shapes:

```text
[Action] [specific technical object] using [method/tool] to achieve [verified outcome].
[Role] for [project/system], coordinating [interfaces/stakeholders] through [review/release/test gate].
Identified [root cause] and introduced [mitigation], validated by [metric/evidence].
```

## Good Examples

- Identified EDM recast layer as a fatigue-risk driver for Inconel 718 E-pin folded leaf springs and introduced plasma polishing plus Kolsterising/K33, validated by 2x fatigue life on actual leaf springs.
- Led EXE Cable Slab tooling workstreams across fixtures, hose and cable preforming, molds, CAD interfaces, supplier feedback, and manufacturability closure.
- Performed system engineering for the EXE:5200 SCFS sensor assembly, including design kickoff, part-numbering, and release-planning coordination.

## Avoid

- Inflated adjectives: `groundbreaking`, `pioneering`, `visionary`, `world-class`.
- Empty business phrases: `synergy`, `transformational`, `innovative solutions`.
- AI meta-language that describes the resume itself: `evidence spans`, `adoption claims`, `contribution scope should remain`, `keeping claims conservative`. These are internal authoring notes, not resume content.
- Claiming institutional adoption when the evidence only supports introduction, proposal, or limited adoption.
- Listing every project in every resume. Select what fits the target role.
- Vague nouns like `habits` when you mean `workflows`, `tooling`, or `pipelines`.

## Compound Adjectives

Hyphenate compound adjectives before nouns: `MRI-compatible`, `review-ready`, `tolerance-sensitive`, `CAD-facing`. The slop detector enforces this.

## Publication and Patent Titles

Never alter a published paper or patent title. Copy the exact title as it appears in IEEE, WIPO, or the official publication. If a title uses `MRI-Compatible` (with hyphen), keep it; if it uses `MRI Compatible` (without), keep that.

## .tex / .adoc Consistency

Every resume and CV has both a `.tex` and `.adoc` source. These must contain the same content (sections, bullets, contact details). The `.adoc` is the default build path. When editing content, update both files. The `.tex` formatting will differ (LaTeX macros vs AsciiDoc markup), but the text must match.

## Required Sections in Resumes

Every resume (one-page) must include: header with Dutch citizen, Professional Summary, Professional Experience, Education, and Technical Skills. Missing Education is a validator failure.

## Resume Density

- One-page resumes should stay one page.
- Current role: maximum 4 bullets.
- Previous role: maximum 3 bullets.
- Skills: grouped rows, not a keyword flood.
- CVs may hold more detail, but should still favor selected case studies over exhaustive project lists.

# Acronym Guard

The repository enforces the [Terminology & Acronym Readability Rule](TERMINOLOGY-RULE.md).

Reader-facing Markdown is checked for known technical abbreviations. Where a term is used without a same-page expansion, the repository guard adds a compact `Terminology on this page` block **at the end of the page**. Existing generated legends are automatically relocated to the page end; they must never interrupt the main content or sit below the title/header.

Reader-facing SVG visuals are checked by the same rule. Where required, the guard adds a visible terminology footer at the **bottom of the visual** without moving the existing artwork. SVG normalization is idempotent: a later run restores the base canvas geometry before regenerating the footer, so repeated checks do not keep increasing the canvas height.

Singular and regular plural forms are treated as the same terminology item, for example KPI/KPIs, OKR/OKRs, API/APIs and LLM/LLMs.

The intended reading standard is: **full term + abbreviation at first use, or a visible legend at the end of the same page/slide/visual.**

This page documents the behavior that future changes must preserve.

<!-- acronym-legend:start -->
> **Terminology on this page**  
> **API** — Application Programming Interface · **KPI** — Key Performance Indicator · **LLM** — Large Language Model  
> **OKR** — Objectives and Key Results
<!-- acronym-legend:end -->

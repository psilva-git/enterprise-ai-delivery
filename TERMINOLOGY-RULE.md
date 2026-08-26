# Terminology & Acronym Readability Rule

## Mandatory rule

Every reader-facing page, presentation slide, diagram, table or visual must be understandable without assuming that the reader already knows technical abbreviations.

### 1. First-use rule

At the **first meaningful occurrence on a page or slide**, write the full term followed by the abbreviation in parentheses where this is readable and natural.

Examples:

- **Artificial Intelligence (AI)**
- **Project Management Office (PMO)**
- **Objectives and Key Results (OKR)**
- **Key Performance Indicator (KPI)**
- **Return on Investment (ROI)**
- **Total Cost of Ownership (TCO)**
- **Model Context Protocol (MCP)**
- **Application Programming Interface (API)**
- **Large Language Model (LLM)**
- **Retrieval-Augmented Generation (RAG)**

After the first expansion, the abbreviation may be used alone on the same page or slide.

### 2. Terminology placement rule — always at the end

If a terminology/acronym legend is used, it must appear **at the end of the page, slide or visual**. It must not interrupt the main content, sit between sections, or appear directly below the title/header.

For Markdown pages, the generated `Terminology on this page` block is the **final content block on the page**.

For slides and diagrams, place the legend in a compact footer at the **bottom of the same slide/visual**.

A link to a glossary on another page is useful as supplementary reference but **does not replace the same-page requirement**.

### 3. Visuals and SVG diagrams

Acronyms used inside SVGs or other diagrams must either:

1. be written out directly in the visual at first use, or
2. have a visible legend in a footer at the bottom of the same visual.

Do not rely on surrounding README text to explain an acronym that appears unexplained inside a standalone visual.

### 4. Presentations and interview/showcase material

Each slide, diagram or showcase page must be able to stand on its own when exported or screenshotted. If inline expansion would make the slide too dense, use a compact terminology footer at the **bottom of that slide**.

### 5. Product names versus abbreviations

Do not expand genuine product or company names that are not abbreviations in the context used. Examples include **Rovo, Jira, Confluence, ServiceNow, Snowflake and Databricks**.

Where a shortened product name can be ambiguous, define it once. Example: **Jira Service Management (JSM)**.

### 6. Release-maturity terminology

Where vendor maturity matters:

- **GA — General Availability / Generally Available**: production release under the vendor's normal availability/support model.
- **Preview / Beta**: pre-GA maturity state; do not present it as equivalent to GA.

### 7. Data-engineering terminology

Use these definitions consistently:

- **ETL — Extract, Transform, Load:** data is extracted from source systems, transformed before loading, and then written into the target data store.
- **ELT — Extract, Load, Transform:** raw or minimally processed data is extracted and loaded first; transformations are performed afterward within or against the target data platform.

### 8. Common repository terminology

| Abbreviation | Meaning |
|---|---|
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| BI | Business Intelligence |
| CI/CD | Continuous Integration / Continuous Delivery (or Deployment where explicitly meant) |
| CRM | Customer Relationship Management |
| DMAIC | Define, Measure, Analyze, Improve, Control |
| ELT | Extract, Load, Transform |
| ETL | Extract, Transform, Load |
| GA | General Availability / Generally Available |
| ITSM | IT Service Management |
| JSM | Jira Service Management |
| KPI | Key Performance Indicator |
| LLM | Large Language Model |
| MCP | Model Context Protocol |
| OKR | Objectives and Key Results |
| PMO | Project Management Office |
| P50 | 50th percentile forecast threshold |
| P85 | 85th percentile forecast threshold |
| RAG | Retrieval-Augmented Generation |
| RBAC | Role-Based Access Control |
| ROI | Return on Investment |
| TCO | Total Cost of Ownership |
| WIP | Work in Progress |

## Review gate

Before merging reader-facing content, verify:

- no unexplained technical acronym appears on a page or visual;
- first occurrence is expanded or a same-page legend is present;
- every generated Markdown terminology block is the **last block on the page**;
- every diagram/slide legend is at the **bottom**, not between content sections;
- diagrams can be understood when viewed independently;
- terms are used consistently across delivery, commercial, AI and governance content.

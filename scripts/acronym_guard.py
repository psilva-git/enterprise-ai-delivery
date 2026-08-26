#!/usr/bin/env python3
"""Enforce acronym clarity across reader-facing Markdown and SVG visuals.

Markdown: if a known abbreviation is used without its meaning somewhere on the
same page, --fix places a compact page-local terminology legend at the END of
the page. Existing generated legends are relocated to the page end so they never
interrupt the main reading flow.

SVG: if a known abbreviation is used without its meaning in the same visual,
--fix extends the SVG canvas downward and adds a visible terminology footer.
The operation is idempotent: an existing generated footer is removed and the
base canvas geometry is restored before the footer is regenerated.

Singular and regular plural acronym forms are treated as the same terminology
item (for example KPI/KPIs, OKR/OKRs, API/APIs and LLM/LLMs).

Repository policy: TERMINOLOGY-RULE.md
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- acronym-legend:start -->"
END = "<!-- acronym-legend:end -->"
SVG_START = "<!-- acronym-svg-legend:start -->"
SVG_END = "<!-- acronym-svg-legend:end -->"

TERMS = {
    "AI": "Artificial Intelligence",
    "A2A": "Agent-to-Agent protocol",
    "AIOps": "Artificial Intelligence for IT Operations",
    "API": "Application Programming Interface",
    "BI": "Business Intelligence",
    "CI/CD": "Continuous Integration / Continuous Delivery",
    "CMDB": "Configuration Management Database",
    "CRM": "Customer Relationship Management",
    "CSD": "Core Software Delivery",
    "DevSecOps": "Development, Security and Operations",
    "DMAIC": "Define, Measure, Analyze, Improve, Control",
    "ELT": "Extract, Load, Transform",
    "ERP": "Enterprise Resource Planning",
    "ETL": "Extract, Transform, Load",
    "GA": "General Availability / Generally Available",
    "HA/DR": "High Availability / Disaster Recovery",
    "HR": "Human Resources",
    "ITSM": "IT Service Management",
    "JSM": "Jira Service Management",
    "KPI": "Key Performance Indicator",
    "LLM": "Large Language Model",
    "MCP": "Model Context Protocol",
    "ML": "Machine Learning",
    "OKR": "Objectives and Key Results",
    "P50": "50th percentile forecast threshold",
    "P85": "85th percentile forecast threshold",
    "PLM": "Product Lifecycle Management",
    "PMO": "Project Management Office",
    "PoC": "Proof of Concept",
    "RAG": "Retrieval-Augmented Generation",
    "RBAC": "Role-Based Access Control",
    "ROI": "Return on Investment",
    "SAST": "Static Application Security Testing",
    "SPM": "Strategic Portfolio Management",
    "SQL": "Structured Query Language",
    "TCO": "Total Cost of Ownership",
    "WIP": "Work in Progress",
}

EXCLUDE = {Path("TERMINOLOGY-RULE.md")}
IGNORED_PARTS = {".git", ".venv", "venv", "node_modules"}

ROOT_SVG_RE = re.compile(r"<svg\b[^>]*>", re.S)
VIEWBOX_RE = re.compile(
    r'viewBox=(["\'])\s*([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\s*\1'
)
HEIGHT_RE = re.compile(r'height=(["\'])([0-9.]+)(px)?\1')


def fmt_num(value: float) -> str:
    return f"{value:g}"


def has_token(text: str, token: str) -> bool:
    """Match a terminology token in singular or regular plural form."""
    return (
        re.search(
            rf"(?<![A-Za-z0-9]){re.escape(token)}s?(?![A-Za-z0-9])",
            text,
        )
        is not None
    )


def strip_generated(text: str) -> str:
    text = re.sub(rf"{re.escape(START)}.*?{re.escape(END)}\s*", "", text, flags=re.S)
    text = re.sub(rf"{re.escape(SVG_START)}.*?{re.escape(SVG_END)}\s*", "", text, flags=re.S)
    return text


def strip_markdown_legend(text: str) -> str:
    return re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\s*", "\n", text, flags=re.S)


def missing_definitions(text: str, strip_legend: bool = False) -> list[str]:
    clean = strip_generated(text) if strip_legend else text
    return [
        token
        for token, meaning in TERMS.items()
        if has_token(clean, token) and meaning.lower() not in clean.lower()
    ]


def pack_markdown_lines(tokens: list[str], max_chars: int = 150) -> list[str]:
    entries = [f"**{token}** — {TERMS[token]}" for token in tokens]
    lines: list[str] = []
    current: list[str] = []

    for entry in entries:
        candidate = " · ".join(current + [entry])
        if current and len(candidate) > max_chars:
            lines.append(" · ".join(current))
            current = [entry]
        else:
            current.append(entry)

    if current:
        lines.append(" · ".join(current))
    return lines


def legend(tokens: list[str]) -> str:
    lines = pack_markdown_lines(tokens)
    body = [START, "> **Terminology on this page**  "]
    for index, line in enumerate(lines):
        suffix = "  " if index < len(lines) - 1 else ""
        body.append(f"> {line}{suffix}")
    body.append(END)
    return "\n".join(body) + "\n"


def apply_legend(text: str, tokens: list[str]) -> str:
    """Place the generated terminology block strictly at the end of the page."""
    clean = strip_markdown_legend(text).rstrip()
    return clean + "\n\n" + legend(tokens)


def markdown_legend_is_at_end(text: str) -> bool:
    """Generated Markdown legends are allowed only as the final page block."""
    start = text.find(START)
    if start == -1:
        return True
    end = text.find(END, start)
    if end == -1:
        return False
    return not text[end + len(END) :].strip()


def svg_geometry(text: str) -> tuple[float, float] | None:
    root_match = ROOT_SVG_RE.search(text)
    if not root_match:
        return None

    viewbox = VIEWBOX_RE.search(root_match.group(0))
    if not viewbox:
        return None

    return float(viewbox.group(4)), float(viewbox.group(5))


def set_root_svg_height(text: str, new_height: float) -> str:
    """Update only the root SVG viewBox/height, never child element heights."""
    root_match = ROOT_SVG_RE.search(text)
    if not root_match:
        return text

    root = root_match.group(0)
    viewbox = VIEWBOX_RE.search(root)
    if not viewbox:
        return text

    new_viewbox = (
        f'viewBox="{viewbox.group(2)} {viewbox.group(3)} '
        f'{viewbox.group(4)} {fmt_num(new_height)}"'
    )
    new_root = root[: viewbox.start()] + new_viewbox + root[viewbox.end() :]

    height = HEIGHT_RE.search(new_root)
    if height:
        unit = height.group(3) or ""
        new_height_attr = f'height="{fmt_num(new_height)}{unit}"'
        new_root = new_root[: height.start()] + new_height_attr + new_root[height.end() :]

    return text[: root_match.start()] + new_root + text[root_match.end() :]


def restore_svg_base(text: str) -> str:
    """Remove a generated footer and restore the canvas height used before it."""
    block_match = re.search(
        rf"{re.escape(SVG_START)}.*?{re.escape(SVG_END)}", text, flags=re.S
    )
    if not block_match:
        return text

    block = block_match.group(0)
    base_match = re.search(r'data-base-height=["\']([0-9.]+)["\']', block)
    if not base_match:
        base_match = re.search(
            r'<rect\b[^>]*\by=["\']([0-9.]+)["\'][^>]*\bheight=', block, flags=re.S
        )

    stripped = text[: block_match.start()].rstrip() + "\n" + text[block_match.end() :].lstrip()
    if not base_match:
        return stripped

    return set_root_svg_height(stripped, float(base_match.group(1)))


def pack_svg_lines(tokens: list[str], width: float, x: float) -> list[str]:
    entries = [f"{token} = {TERMS[token]}" for token in tokens]
    max_chars = max(70, int((width - 2 * x) / 7.0))
    lines: list[str] = []
    current: list[str] = []

    for entry in entries:
        candidate = " · ".join(current + [entry])
        if current and len(candidate) > max_chars:
            lines.append(" · ".join(current))
            current = [entry]
        else:
            current.append(entry)

    if current:
        lines.append(" · ".join(current))
    return lines


def apply_svg_legend(text: str, tokens: list[str]) -> str:
    text = restore_svg_base(text)
    geometry = svg_geometry(text)
    if not geometry:
        return text

    width, base_height = geometry
    x = max(16.0, width * 0.018)
    text_lines = pack_svg_lines(tokens, width, x)
    footer_height = max(62.0, 34.0 + 24.0 * len(text_lines))
    new_height = base_height + footer_height

    text = set_root_svg_height(text, new_height)
    title_y = base_height + 22.0

    lines = [
        SVG_START,
        (
            '<g id="acronym-legend" aria-label="Terminology legend" '
            f'data-base-height="{fmt_num(base_height)}">'
        ),
        (
            f'<rect x="0" y="{fmt_num(base_height)}" width="{fmt_num(width)}" '
            f'height="{fmt_num(footer_height)}" fill="#f8fafc" '
            'stroke="#cbd5e1" stroke-width="1"/>'
        ),
        (
            f'<text x="{fmt_num(x)}" y="{fmt_num(title_y)}" '
            'font-family="Arial, Helvetica, sans-serif" font-size="13" '
            'font-weight="700" fill="#334155">Terminology</text>'
        ),
    ]

    for index, line in enumerate(text_lines):
        y = title_y + 21.0 + index * 22.0
        lines.append(
            f'<text x="{fmt_num(x)}" y="{fmt_num(y)}" '
            'font-family="Arial, Helvetica, sans-serif" font-size="12" '
            f'fill="#475569">{html.escape(line)}</text>'
        )

    lines.extend(["</g>", SVG_END])
    return text.rstrip().replace("</svg>", "\n".join(lines) + "\n</svg>", 1)


def files(pattern: str) -> list[Path]:
    result = []
    for path in ROOT.rglob(pattern):
        rel = path.relative_to(ROOT)
        if rel in EXCLUDE or any(part in IGNORED_PARTS for part in rel.parts):
            continue
        result.append(path)
    return sorted(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    markdown_violations: list[tuple[Path, list[str]]] = []
    markdown_placement_violations: list[Path] = []
    svg_violations: list[tuple[Path, list[str]]] = []
    changed: list[Path] = []

    for path in files("*.md"):
        text = path.read_text(encoding="utf-8")

        if args.fix:
            clean = strip_markdown_legend(text).rstrip()
            missing = missing_definitions(clean)
            new_text = apply_legend(clean, missing) if missing else clean + "\n"
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                changed.append(path)
            continue

        missing = missing_definitions(text)
        if missing:
            markdown_violations.append((path, missing))
        if not markdown_legend_is_at_end(text):
            markdown_placement_violations.append(path)

    for path in files("*.svg"):
        text = path.read_text(encoding="utf-8")
        missing = missing_definitions(text, strip_legend=args.fix)
        if not missing:
            continue

        svg_violations.append((path, missing))
        if args.fix:
            new_text = apply_svg_legend(text, missing)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                changed.append(path)

    if args.fix:
        for path in changed:
            print(f"FIXED {path.relative_to(ROOT)}")
        return 0

    if markdown_violations or markdown_placement_violations or svg_violations:
        if markdown_violations:
            print("Markdown pages with undefined abbreviations:")
            for path, tokens in markdown_violations:
                print(f"- {path.relative_to(ROOT)}: {', '.join(tokens)}")
        if markdown_placement_violations:
            print("\nMarkdown pages with terminology legend not at page end:")
            for path in markdown_placement_violations:
                print(f"- {path.relative_to(ROOT)}")
        if svg_violations:
            print("\nSVG visuals with undefined abbreviations:")
            for path, tokens in svg_violations:
                print(f"- {path.relative_to(ROOT)}: {', '.join(tokens)}")
        return 1

    print("Acronym readability check passed; Markdown legends are at page end and SVG legends are at visual end.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

try:
    import markdown  # type: ignore
except Exception:
    markdown = None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def render_markdown(md_text: str) -> str:
    if markdown is None:
        raise RuntimeError(
            "Python package 'markdown' is not installed. "
            "Run: python3 -m pip install -r requirements.txt"
        )
    return markdown.markdown(
        md_text,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "sane_lists",
            "toc",
        ],
        output_format="html5",
    )

def infer_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        match = re.match(r\"^#\\s+(.+)$\", line.strip())
        if match:
            return match.group(1).strip()
    return fallback


def build_html(content_html: str, template_html: str, title: str) -> str:
    return (
        template_html.replace("{{CONTENT}}", content_html)
        .replace("{{TITLE}}", title)
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a Markdown document to HTML using a template."
    )
    parser.add_argument("input", help="Path to input Markdown file")
    parser.add_argument(
        "-o", "--output", help="Output HTML path (default: same name with .html)"
    )
    parser.add_argument(
        "-t",
        "--template",
        default="template.html",
        help="HTML template file (default: template.html in tool folder)",
    )
    parser.add_argument(
        "--title",
        default="Document",
        help="HTML title (default: Document)",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 1

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else input_path.with_suffix(".html")
    )

    template_path = Path(args.template).expanduser().resolve()
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        return 1

    md_text = read_text(input_path)
    title = infer_title(md_text, args.title)
    content_html = render_markdown(md_text)
    template_html = read_text(template_path)
    full_html = build_html(content_html, template_html, title)

    write_text(output_path, full_html)
    print(f"OK: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

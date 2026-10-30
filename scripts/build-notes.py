#!/usr/bin/env python3
"""Embed the Markdown notes in index.html without adding runtime dependencies."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "notes"


def build() -> None:
    manifest = json.loads((NOTES / "content.json").read_text())
    content = {"topics": [], "problems": []}
    for kind in content:
        seen = set()
        for entry in manifest.get(kind, []):
            record = dict(entry)
            body_path = (NOTES / record.pop("body_file")).resolve()
            if not body_path.is_relative_to(NOTES.resolve()) or body_path.suffix != ".md":
                raise ValueError("Note bodies must be Markdown files inside notes/.")
            if record["id"] in seen:
                raise ValueError(f"Duplicate {kind} ID: {record['id']}")
            seen.add(record["id"])
            record["body"] = body_path.read_text()
            content[kind].append(record)

    encoded = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
    for character in "<>&":
        encoded = encoded.replace(character, f"\\u{ord(character):04x}")
    block = '<script id="repository-content" type="application/json">' + encoded + "</script>"
    target = ROOT / "index.html"
    html = target.read_text()
    pattern = r'<script id="repository-content" type="application/json">[\s\S]*?</script>'
    if re.search(pattern, html):
        html = re.sub(pattern, lambda _: block, html, count=1)
    else:
        anchor = '<script id="embedded-data" type="application/json">null</script>'
        if anchor not in html:
            raise ValueError("Cannot find the repository content insertion point.")
        html = html.replace(anchor, anchor + "\n" + block, 1)
    target.write_text(html)
    print(f"Embedded {len(content['problems'])} problem notes and {len(content['topics'])} master notes.")


if __name__ == "__main__":
    build()

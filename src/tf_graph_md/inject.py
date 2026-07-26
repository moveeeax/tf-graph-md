"""Idempotently inject a Mermaid block into a README between markers."""
from __future__ import annotations

START = "<!-- tf-graph-md:start -->"
END = "<!-- tf-graph-md:end -->"


def _block(mermaid: str) -> str:
    body = mermaid.rstrip("\n")
    return f"{START}\n```mermaid\n{body}\n```\n{END}"


def inject(readme: str, mermaid: str) -> str:
    """Return readme with the Mermaid block placed between the markers.

    If the markers already exist their contents are replaced (idempotent — running
    twice yields the same file). If they do not exist, the block is appended.
    """
    block = _block(mermaid)
    s = readme.find(START)
    e = readme.find(END)
    if s != -1 and e != -1 and e > s:
        before = readme[:s]
        after = readme[e + len(END):]
        return before + block + after
    sep = "" if readme.endswith("\n") or readme == "" else "\n"
    tail = "" if readme == "" else "\n"
    return readme + sep + tail + block + "\n"

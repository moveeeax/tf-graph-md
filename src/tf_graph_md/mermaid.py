"""Render a parsed Terraform graph as Mermaid `graph` syntax."""
from __future__ import annotations

import re
from typing import Dict, List

from .dot import Graph

# Node ids that are Terraform plumbing rather than real resources.
_META = re.compile(
    r'(provider\[|^provider\.|^var\.|^local\.|^output\.|'
    r'meta\.count-boundary|^root$)'
)

_MODULE = re.compile(r"^module\.([^.\[]+)")


def is_meta(node_id: str) -> bool:
    """Whether a node is provider/meta plumbing that clutters the diagram."""
    return bool(_META.search(node_id))


def _module_of(node_id: str) -> str:
    m = _MODULE.match(node_id)
    return m.group(1) if m else ""


def render(
    graph: Graph,
    direction: str = "LR",
    collapse: bool = True,
    group_modules: bool = False,
) -> str:
    """Return a Mermaid `graph` document for the given Terraform graph."""
    keep = [n for n in graph.nodes() if not (collapse and is_meta(n))]
    kept = set(keep)

    ids: Dict[str, str] = {n: f"n{i}" for i, n in enumerate(keep)}
    lines: List[str] = [f"graph {direction}"]

    def node_decl(n: str) -> str:
        label = graph.labels.get(n, n).replace('"', "'")
        return f'{ids[n]}["{label}"]'

    if group_modules:
        groups: Dict[str, List[str]] = {}
        for n in keep:
            groups.setdefault(_module_of(n), []).append(n)
        for mod in sorted(k for k in groups if k):
            lines.append(f'  subgraph module_{mod}["module.{mod}"]')
            for n in groups[mod]:
                lines.append("    " + node_decl(n))
            lines.append("  end")
        for n in groups.get("", []):
            lines.append("  " + node_decl(n))
    else:
        for n in keep:
            lines.append("  " + node_decl(n))

    seen = set()
    for a, b in graph.edges:
        if a not in kept or b not in kept:
            continue
        key = (a, b)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"  {ids[a]} --> {ids[b]}")

    return "\n".join(lines) + "\n"

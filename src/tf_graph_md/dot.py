"""A small parser for the Graphviz DOT that `terraform graph` emits."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

_EDGE = re.compile(r'"([^"]+)"\s*->\s*"([^"]+)"')
_NODE = re.compile(r'^\s*"([^"]+)"\s*(?:\[(?P<attrs>.*)\])?\s*;?\s*$')
_LABEL = re.compile(r'label\s*=\s*"([^"]*)"')


@dataclass
class Graph:
    """Directed graph of Terraform nodes."""

    labels: Dict[str, str] = field(default_factory=dict)  # id -> display label
    edges: List[Tuple[str, str]] = field(default_factory=list)

    def nodes(self) -> List[str]:
        return list(self.labels.keys())


_MODE = re.compile(r"\s+\([a-z][a-z ]*\)$")


def _clean(node_id: str) -> str:
    """Normalize a node id: drop the `[root] ` prefix and the trailing graph-mode
    annotation Terraform appends (` (expand)`, ` (close)`, ` (destroy)`), so ids
    are clean resource addresses that edges and node declarations agree on.
    """
    if node_id.startswith("[root] "):
        node_id = node_id[len("[root] "):]
    return _MODE.sub("", node_id)


def parse(dot: str) -> Graph:
    """Parse DOT text into a Graph, recording every node id referenced.

    Both explicit node declarations and endpoints of edges become nodes, so a
    graph that only lists edges still yields the full node set.
    """
    g = Graph()

    def ensure(raw: str, label: str = "") -> str:
        nid = _clean(raw)
        if nid not in g.labels or (label and g.labels[nid] == nid):
            g.labels[nid] = label or g.labels.get(nid) or nid
        return nid

    for line in dot.splitlines():
        m = _EDGE.search(line)
        if m:
            a = ensure(m.group(1))
            b = ensure(m.group(2))
            g.edges.append((a, b))
            continue
        nm = _NODE.match(line)
        if nm and "->" not in line and "{" not in line and "}" not in line:
            attrs = nm.group("attrs") or ""
            lm = _LABEL.search(attrs)
            ensure(nm.group(1), lm.group(1) if lm else "")
    return g

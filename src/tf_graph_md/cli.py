"""Command-line interface for tf-graph-md."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .dot import parse
from .inject import inject
from .mermaid import render


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tf-graph-md",
        description="Turn `terraform graph` DOT output into a Mermaid diagram.",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("-i", "--input", help="read DOT from a file instead of stdin")
    p.add_argument("-d", "--direction", default="LR", choices=["LR", "RL", "TD", "TB", "BT"],
                   help="Mermaid graph direction (default LR)")
    p.add_argument("--group-modules", action="store_true", help="group nodes into subgraphs by module")
    p.add_argument("--no-collapse", action="store_true", help="keep provider/meta plumbing nodes")
    p.add_argument("--inject", metavar="README", help="write the diagram into a README between markers")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    dot = open(args.input).read() if args.input else sys.stdin.read()
    graph = parse(dot)
    mermaid = render(
        graph,
        direction=args.direction,
        collapse=not args.no_collapse,
        group_modules=args.group_modules,
    )

    if args.inject:
        try:
            with open(args.inject) as f:
                readme = f.read()
        except FileNotFoundError:
            readme = ""
        updated = inject(readme, mermaid)
        with open(args.inject, "w") as f:
            f.write(updated)
        print(f"Injected diagram into {args.inject}", file=sys.stderr)
    else:
        sys.stdout.write(mermaid)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

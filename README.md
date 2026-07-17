# tf-graph-md

> Turn your Terraform dependency graph into a Mermaid diagram you can paste into any README.

**Status:** 🚧 In development

## Overview

Convert `terraform graph` output into a Mermaid diagram ready to embed in a README.

## Features

- Parse Graphviz DOT emitted by `terraform graph`
- Translate nodes/edges into Mermaid `graph` syntax
- Collapse provider/meta nodes and optionally group by module
- Write a fenced ```mermaid block or inject into a README marker
- Zero external services — pure local transform

## Stack

Python 3.11, `pydot`/DOT parsing, Mermaid output.

## Usage

```bash
terraform graph | tf-graph-md --group-modules > graph.mmd
tf-graph-md --inject README.md
```

## License

MIT

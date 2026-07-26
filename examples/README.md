# examples

- [`graph.dot`](graph.dot) — sample `terraform graph` output (one resource, one
  bucket, a module subnet, and a provider node).
- [`README.sample.md`](README.sample.md) — a README with `tf-graph-md` markers to
  inject into.

```bash
# render to a Mermaid file
tf-graph-md --input graph.dot --group-modules > graph.mmd

# or inject straight into a README between the markers (idempotent)
tf-graph-md --input graph.dot --inject README.sample.md
```

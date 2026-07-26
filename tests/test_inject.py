from tf_graph_md.inject import END, START, inject


def test_replace_between_markers():
    readme = f"# Title\n\n{START}\nOLD\n{END}\n\ntail\n"
    out = inject(readme, "graph LR\n  a --> b\n")
    assert "OLD" not in out
    assert "```mermaid" in out
    assert "a --> b" in out
    assert out.startswith("# Title")
    assert out.rstrip().endswith("tail")


def test_idempotent():
    readme = f"{START}\nx\n{END}\n"
    once = inject(readme, "graph LR\n  a --> b\n")
    twice = inject(once, "graph LR\n  a --> b\n")
    assert once == twice


def test_append_when_no_markers():
    out = inject("# Title\n", "graph LR\n  a --> b\n")
    assert START in out and END in out
    assert "```mermaid" in out


def test_empty_readme():
    out = inject("", "graph LR\n  a --> b\n")
    assert out.startswith(START)

import os

from tf_graph_md.dot import parse
from tf_graph_md.mermaid import is_meta, render

FIX = os.path.join(os.path.dirname(__file__), "..", "examples", "graph.dot")


def graph():
    return parse(open(FIX).read())


def test_is_meta():
    assert is_meta('provider["registry.terraform.io/hashicorp/aws"]')
    assert not is_meta("aws_instance.web")


def test_render_collapses_provider():
    out = render(graph())
    assert out.startswith("graph LR")
    assert "aws_instance.web" in out
    # provider node dropped, and edges to it too.
    assert "provider[" not in out
    # two surviving edges (web->data, web->subnet).
    assert out.count("-->") == 2


def test_render_no_collapse_keeps_provider():
    out = render(graph(), collapse=False)
    assert "provider[" in out
    assert out.count("-->") == 3


def test_group_modules_emits_subgraph():
    out = render(graph(), group_modules=True)
    assert "subgraph module_vpc" in out
    assert "module.vpc" in out


def test_direction():
    out = render(graph(), direction="TD")
    assert out.startswith("graph TD")


def test_labels_are_quoted():
    out = render(graph())
    assert '["aws_instance.web"]' in out

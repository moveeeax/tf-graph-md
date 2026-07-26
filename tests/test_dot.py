import os

from tf_graph_md.dot import parse

FIX = os.path.join(os.path.dirname(__file__), "..", "examples", "graph.dot")


def test_parse_nodes_and_edges():
    g = parse(open(FIX).read())
    # [root] prefix stripped; label preferred over id.
    assert "aws_instance.web" in g.labels.values()
    ids = set(g.labels.keys())
    assert any("aws_instance.web" in i for i in ids)
    # three edges from the fixture.
    assert len(g.edges) == 3


def test_edge_endpoints_become_nodes():
    g = parse('digraph { "[root] a" -> "[root] b" }')
    assert set(g.labels.keys()) == {"a", "b"}
    assert g.edges == [("a", "b")]


def test_label_used_when_present():
    g = parse('"[root] x" [label = "pretty"]')
    assert g.labels["x"] == "pretty"


def test_prefix_stripped():
    g = parse('"[root] module.vpc.aws_subnet.a" [label = "module.vpc.aws_subnet.a"]')
    assert "module.vpc.aws_subnet.a" in g.labels

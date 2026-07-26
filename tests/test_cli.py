import os

from tf_graph_md.cli import main

FIX = os.path.join(os.path.dirname(__file__), "..", "examples", "graph.dot")


def test_stdout_render(capsys):
    rc = main(["--input", FIX])
    assert rc == 0
    out = capsys.readouterr().out
    assert out.startswith("graph LR")
    assert "aws_instance.web" in out


def test_group_modules_flag(capsys):
    main(["--input", FIX, "--group-modules"])
    assert "subgraph module_vpc" in capsys.readouterr().out


def test_inject_writes_file(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("# Demo\n")
    rc = main(["--input", FIX, "--inject", str(readme)])
    assert rc == 0
    text = readme.read_text()
    assert "```mermaid" in text and "aws_instance.web" in text
    # idempotent second run
    main(["--input", FIX, "--inject", str(readme)])
    assert readme.read_text() == text

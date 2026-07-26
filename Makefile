.PHONY: install test clean
install:
	pip install -e ".[dev]"
test:
	pytest -q
clean:
	rm -rf build dist *.egg-info .pytest_cache

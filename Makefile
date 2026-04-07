run:
	python3 a_maze_ing.py config.txt

install:
	pip install mypy flake8

debug:
	python3 -m pdb a_maze_ing.py
build :
	poetry build
	mv dist/maze_gene-0.1.0-py3-none-any.whl .
	mv dist/maze_gene-0.1.0.tar.gz .
	rm -rf dist

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
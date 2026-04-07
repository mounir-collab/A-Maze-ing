run:
	python3 a_maze_ing.py config.txt

install:
	pip install -r requirements.txt

debug:
	python3 -m pdb a_maze_ing.py
build :
	python3 -m build maze_gen

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
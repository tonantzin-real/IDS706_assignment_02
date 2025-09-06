# Should run with make ___

install:								# Updates pip to the latest version and installs the requirements.txt
	pip install --upgrade pip && pip install -r requirements.txt

format:									# Reformats the Python files to follow black's styling rules
	black *.py

lint:									# Keeps the code clean and consistent by flagging issues like: incorrect indentation, Line too long, etc
	flake8 analysis.py
	flake8 test_analysis.py

test:									# Runs .py (if I had another line below with a different .py it will also run it)
	python -m pytest -vv --cov=hello test_analysis.py

clean:									# Cleans up leftover files that Python and test tools create (the ones besides rm -rf)
	rm -rf __pycache__ .pytest_cache .coverage

all: install format lint test			# Runs all the makes 

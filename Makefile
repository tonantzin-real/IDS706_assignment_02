# Should run with make ___

install:								# Updates pip to the latest version and installs the requirements.txt
	pip install --upgrade pip && pip install -r requirements.txt

format:									# Reformats the Python files to follow black's styling rules
	black *.py

lint:									# Keeps the code clean and consistent by flagging issues like: incorrect indentation, Line too long, etc
	flake8 hello.py

test:									# Runs test_hello.py (if I had another line below with a different .py it will also run it)
	python -m pytest -vv --cov=hello test_hello.py

clean:									# Cleans up leftover files that Python and test tools create (the ones besides rm -rf)
	rm -rf __pycache__ .pytest_cache .coverage

all: install format lint test			# Runs all the makes 

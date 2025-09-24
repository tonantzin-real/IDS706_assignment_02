# Should run with make ___

install:								# Updates pip to the latest version and installs the requirements.txt
	python -m pip install --upgrade pip
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
	pip install pytest pytest-cov black flake8

format:									# Reformats the Python files to follow black's styling rules
	black --line-length 79 analysis.py test_analysis.py

lint: format							# Keeps the code clean and consistent by flagging issues like: incorrect indentation, Line too long, etc
# Code quality checks (AFTER format)
# ignores E501 long lines (>79 characters) and W503 (operador al final de linea)
	flake8 analysis.py test_analysis.py --ignore=E501,W503 

test: lint								# Runs .py (if I had another line below with a different .py it will also run it)
# # Run tests (AFTER lint)
	python -m pytest test_analysis.py -v --cov=analysis

clean:									# Cleans up leftover files that Python and test tools create (the ones besides rm -rf)
	rm -rf __pycache__ .pytest_cache .coverage

all: test								# Run complete pipeline in ORDER
		@echo "✅ All checks completed successfully!"

ci: lint test							# For CI/CD (format is check-only in CI)
	@echo "✅ CI pipeline completed!"
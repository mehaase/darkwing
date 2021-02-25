.PHONY: test

check: mypy test

coverage:
	poetry run codecov

mypy:
	poetry run mypy -p darkwing

test:
	poetry run pytest --cov=darkwing/ test/
	poetry run coverage report -m

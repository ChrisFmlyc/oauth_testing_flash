all: run

clean:
	rm -rf venv build dist .pytest_cache .mypy_cache *.egg-info

venv:
	python3 -m venv venv && \
		venv/bin/pip install --upgrade pip setuptools && \
		venv/bin/pip install --editable ".[dev]"

run: venv
	venv/bin/flask --app oauth_testing_flask --debug run

run_sec: venv
	venv/bin/flask --app oauth_testing_flask --debug run --cert=cert.pem --key=key.pem

test: venv
	venv/bin/pytest

dist: venv test
	venv/bin/pip wheel --wheel-dir dist --no-deps .

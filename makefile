all:

lint:
	npx prettier@3.6.2 --check .
	uvx black@24.1.0 --check .
	
format:
	npx prettier@3.6.2 --write .
	uvx black@24.1.0 .

%.min.js: %.js
	npx uglify-js@3.19.3 --compress --mangle -- $< > $@

test:
	uv run --python 3.11 --with fastapi[standard]==0.135.1 --with pytest-playwright==0.7.2 python -m playwright install chromium firefox
	uv run --python 3.11  --with fastapi[standard]==0.135.1 --with pytest-playwright==0.7.2 python -m pytest --doctest-modules --browser chromium --browser firefox

serve:
	uv run --python 3.11 --with fastapi[standard]==0.135.1 fastapi dev

clean:
	rm -rf .pytest_cache __pycache__ dep.css .venv

all: deploy

lint:
	npx prettier@3.6.2 --check .
	
format:
	npx prettier@3.6.2 --write .

%.min.js: %.js
	npx uglify-js@3.19.3 --compress --mangle -- $< > $@

dep.css:
	wget -O dep.css https://example.com/dep.css

test:
	uv run --with pytest-playwright==0.7.2 python -m playwright install chromium firefox
	uv run --with pytest-playwright==0.7.2 python -m pytest --browser chromium --browser firefox

deploy: dep.css

clean:
	rm -rf .pytest_cache __pycache__ dep.css

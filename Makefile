run:
	python -m aiohttp.web -H localhost -P 8080 app.main:init_func
build:
	pip install -r requirements.txt
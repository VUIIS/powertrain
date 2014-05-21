.PHONY: docs

test: clean
	./manage.py test

clean:
	rm -rf htmlcov
	find . -type f -name "*.pyc" -delete

docs:
	cd docs && make clean && make html

open_docs: docs
	open docs/_build/html/index.html

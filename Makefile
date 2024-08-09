dumpdata:
	python manage.py dumpdata goods.Categories > fixtures/goods/cats.json
	python manage.py dumpdata goods.Products > fixtures/goods/prod.json
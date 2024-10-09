dumpdata:
	python manage.py dumpdata goods.Categories > fixtures/goods/cats.json
	python manage.py dumpdata goods.Products > fixtures/goods/prod.json

loaddata:
	python manage.py loaddata fixtures/goods/cats.json
	python manage.py loaddata fixtures/goods/prod.json
	python manage.py loaddata fixtures/users/users.json
	python manage.py loaddata fixtures/orders/orders.json

ruff:
	ruff check --fix
	ruff format
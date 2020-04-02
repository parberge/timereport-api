NAME=timereport-api
VERSION=0.0.1

DB_PORT = 8000
API_PORT = 8010
export DB_HOST = http://localhost:$(DB_PORT)
export FLASK_APP = main.py

.PHONY: run stop restart

run:
	docker run --rm --name dynamodb-local -d -p $(DB_PORT):$(DB_PORT) amazon/dynamodb-local
	# Wait for local DB to start
	sleep 5
	flask run --port $(API_PORT)

stop:
	docker stop dynamodb-local

restart:
	docker restart dynamodb-local
	# Wait for local DB to start
	sleep 5
	flask run --port $(API_PORT)

default: run
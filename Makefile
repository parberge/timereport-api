NAME=timereport_backend
VERSION=0.0.1

WORKDIR = timereport_backend
PORT = 8010

.PHONY: pull run stop restart rm

pull:
	docker pull amazon/dynamodb-local

run:
	docker run --name dynamodb-local -d -p $(PORT):$(PORT) amazon/dynamodb-local
	cd $(WORKDIR) && chalice local

stop:
	docker stop dynamodb-local

restart:
	docker restart dynamodb-local

rm:
	docker rm dynamodb-local

default: run
clean: stop rm

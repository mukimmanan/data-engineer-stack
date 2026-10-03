.PHONY: build up down clean restart logs network

network:
	docker network create shared-network || true

build:
	docker compose build

up: network
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v
	docker network rm shared-network || true

restart: down up

logs:
	docker compose logs -f

up:
	docker-compose up

build:
	docker-compose up --build

down:
	docker-compose down

migrate:
	docker exec -it battery_service python manage.py migrate

migrations:
	docker exec -it battery_service python manage.py makemigrations

test:
ifeq ($(TEST),)
	docker-compose run --rm --entrypoint "pytest $(FILE) -s --disable-warnings" battery_service
else
	docker-compose run --rm --entrypoint "pytest $(FILE) -s --disable-warnings -k $(TEST)" battery_service
endif

bash:
	docker-compose exec battery_service bash

lint:
	bash "./scripts/lint.sh"

superuser:
	docker exec -it battery_service bash -c "./scripts/create_superuser.sh"

run:
	docker-compose up --build -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

clean.all:
	docker-compose down -v --rmi all --remove-orphans
	docker volume prune -f
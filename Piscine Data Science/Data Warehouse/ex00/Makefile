PROJECT_NAME=DS-00

COMPOSE=docker-compose -f docker-compose.yml

NETWORK_NAME = my_net

up:
	$(COMPOSE) up -d

create-network:
	@if ! docker network ls --format '{{.Name}}' | grep -wq $(NETWORK_NAME); then \
		echo "Creating network $(NETWORK_NAME)..."; \
		docker network create $(NETWORK_NAME); \
	else \
		echo "Network $(NETWORK_NAME) already exists."; \
	fi

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f

restart:
	$(COMPOSE) down && $(COMPOSE) up -d

clean:
	$(COMPOSE) down -v --rmi all --remove-orphans

ps:
	$(COMPOSE) ps -a

shell:
	docker exec -it python-app bash

pgshell:
	docker exec -it postgres psql -U makhtar -d piscineds

rm_vols:
	@if [ "$$(docker volume ls -q)" != "" ]; then \
		echo "Removing all Docker volumes..."; \
		docker volume rm $$(docker volume ls -q); \
	else \
		echo "No Docker volumes to remove."; \
	fi

rm_images:
	@if [ "$$(docker images -a -q)" != "" ]; then \
		echo "Removing all Docker images..."; \
		docker rmi -f $$(docker images -a -q); \
	else \
		echo "No Docker images to remove."; \
	fi

rm_orphans:
	@if [ "$$(docker ps -qa)" != "" ]; then \
		echo "Removing all containers..."; \
		docker rm -v -f $$(docker ps -qa); \
	else \
		echo "No containers to remove."; \
	fi

rm_net:
	@if docker network ls --format '{{.Name}}' | grep -wq $(NETWORK_NAME); then \
		echo "Removing Docker network '$(NETWORK_NAME)'..."; \
		docker network rm $(NETWORK_NAME); \
	else \
		echo "Network '$(NETWORK_NAME)' does not exist."; \
	fi

fclean: down rm_orphans rm_vols rm_images rm_net
		rm -rf Python/scripts/
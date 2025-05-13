# Piscine Data Science

## Services:
1. Postgres(independent)
2. pgadmin (depends_on postgres via network my_net)
3. python (depends_on postgres via network my_net)

## Shell Commands:

	docker-compose up -d --build -> Builds all the respective images and runs all the container.

	docker-compose run python-app -. Runs the Python Service.

	docker rm -v -f $(docker ps -qa) -> Removes all the containers.

	docker exec -it postgres psql -U makhtar -d piscineds -h localhost -W -> Creates an interactive terminal for the container postgres with -U username, -d piscineds (database name) -h localhost (hosted at localhost) -W (Prompts the user to write the password)

	docker rmi -f $(docker images -a -q) -> Removes all the docker images.

	docker volume rm $(docker volume ls -q) -> Removes all the docker volumes.

## Volumes Created:
1. Postgres:/tmp/
2. pgadmin:/var/lib/pgadmin
3. python:/app/

## Interactive Shells:
	docker exec -it postgres bash -> Interactive terminal for the postgres shell.

	docker-compose exec -it python-app bash -> Interactive terminal for the python shell.

## Check for Items:

	// SQL Commands
	\dt               -- List all tables
	SELECT COUNT(*) FROM items;
	SELECT * FROM items LIMIT 5;

	// Python Script
	with engine.connect() as conn:
    	result = conn.execute(f"SELECT COUNT(*) FROM {tableName}")
    	count = result.scalar()
    	print(f"✅ Table {tableName} contains {count} rows.")

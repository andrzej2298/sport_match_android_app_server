delete_migrations: api/models.py
	rm -rf api/migrations
	docker-compose kill db
	docker-compose rm db
	docker-compose up -d

# you need to wait for the container to start to execute this
add_initial_migration: api/models.py
	docker-compose exec api ./manage.py makemigrations api
	docker-compose exec api ./manage.py migrate
	# by default the migrations folder is owned by root,
	# because docker containers execute with root privileges
	sudo chown $(USER) -R api/migrations


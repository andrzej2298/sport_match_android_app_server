# Setup
```
docker-compose build
docker-compose up
```

# Database migrations
Because creating a migration requires
connecting to the database, you can do it this way:
```
# deleting previous migrations
# because keeping them
# is currently unnecessary
rm -rf api/migrations
docker-compose kill db
# info about migrations is
# also kept in the database
docker-compose rm db

# generating new migrations
docker-compose up
docker-compose exec api bash
./manage.py makemigrations api
./manage.py migrate
```
By default Docker creates files with root permissions,
so additionally you can change the owner of the
migrations folder to yourself instead of root.

# API endpoints

To see available API endpoints, run `firefox localhost:8000/api/`.

# Relevant links
- [GeoDjango](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/)
- [PostGIS](https://postgis.net)

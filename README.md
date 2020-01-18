# Setup
```
docker-compose build
docker-compose up
```

# Database migrations
Because creating a migration requires
connecting to the database, you can do it this way:
```
docker-compose up
docker-compose exec api bash
./manage.py makemigrations
```

# API endpoints

To see available API endpoints, run `firefox localhost:8000/api/`.

# Relevant links
- [GeoDjango](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/)
- [PostGIS](https://postgis.net)

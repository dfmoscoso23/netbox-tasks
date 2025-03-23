docker compose exec -it netbox python manage.py loaddata fixtures/needed_data.json
docker compose cp Scripts/basic_filter.py netbox:/opt/netbox/netbox/scripts/
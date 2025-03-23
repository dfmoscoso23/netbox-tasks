echo 'First without filter:'
docker compose exec -it script-container python Scripts/api_script.py
echo 'Second filtering status active:'
docker compose exec -it script-container python Scripts/api_script.py --status active
echo 'Run tests:'
docker compose exec -it script-container pytest Scripts/test_api_script.py
echo 'First without filter:'
docker compose exec -it script-container python api_script.py
echo 'Second filtering status active:'
docker compose exec -it script-container python api_script.py --status active
echo 'Run tests:'
docker compose exec -it script-container pytest test_api_script.py
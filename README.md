# NETBOX TASKS

## NetBox Usage Disclaimer
This version uses the Docker image of NetBox and only keeps the necessary files to run the image.
For the full NetBox repository, visit: [NetBox Docker Repository](https://github.com/netbox-community/netbox-docker).

## Run
To start the containers, execute:
To run the image execute

```docker compose up -d```

Then, load the fixtures by running:

```sh execute-fixtures.sh```


## TASK 1: Filter Script

This script must be executed in the NetBox UI.
To add it, go to Scripts and click + Add.

### Features:
	- Filters devices by status, site, and rack.
	- Outputs the result in YAML format.
	- Displays logs of the found devices.
The script is located in:

Scripts/basic_filter.py
 
 >To acces I used the user *test-user@gmail.com* (It is added in the fixture)
 >Password: testestes
 >Naturally, you can create a superuser using createsuper, as always.

## TASK 2: Api Script

A separate Python container *script-container* has been added to docker-compose.yml to run the API script independently of the NetBox runtime (it still uses the internal container network).
It uses a token from the user added in the fixture, which is stored in the env folder under script.env. The container reads this token from the environment file. 

### Running the API Script

**Inside container:**

```python api_script.py```

Can filter status with *--status*

```python api_script.py --status active```

**Outside the container:**
```docker compose exec -it script-container python api_script.py```
or ```docker compose exec -it script-container python api_script.py --status active```

Also i added a sh to run and tested more easily with ```sh execute-api-script.sh```

In all cases, the script prints the count of devices for all statuses or only for the requested status.

### Running API Script Tests

The script includes mocked API tests using pytest.

This script has a test mocking the api can be runned whith the sh or with
```docker compose exec -it script-container pytest test_api_script.py```

## FILES
All the scripts are in the Scripts folder.
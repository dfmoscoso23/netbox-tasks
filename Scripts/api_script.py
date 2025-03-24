import argparse
from collections import defaultdict
import os
import requests

URL = os.getenv("NETBOX_URL")
TOKEN = os.getenv("TOKEN_NETBOX")


def make_query(status):
	"""
	Queries the NetBox API to get the number of devices with a specific status
	or counts all statuses if no status is provided.
	"""
	headers = {
	'Authorization': f'Token {TOKEN}'
	}

	if status:
		params = {"status": status}
		response = requests.get(URL, headers=headers, params=params)
		if response.status_code != 200:
			raise ConnectionError(response.content)
		json_response = response.json()
		return f"Exist {json_response["count"]} with status {status}"

	response = requests.get(URL, headers=headers)
	if response.status_code != 200:
		raise ConnectionError(response.content)
	json_response = response.json()
	if json_response.get("count") == 0:
		raise ValueError("There is no devices")
	devices = defaultdict(int)
	for device in json_response.get("results", []):
		status = device.get("status",{}).get("value")
		devices[status] += 1
	return f"Exist this quantity of devices: \n {devices}"


def main():
	"""
	Main function that parses command-line arguments and runs the query.
	Retrieves the quantity of devices grouped by status.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--status", required=False)
	args = parser.parse_args()

	query_result = make_query(args.status)
	print(query_result)
	return query_result


if __name__ == "__main__":
    main()
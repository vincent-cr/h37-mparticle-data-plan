from client import Client


CONFIG = {
	"client_id": "{{YOUR_CLIENT_ID}}",
	"client_secret": "{{YOUR_CLIENT_SECRET}}",
	"workspace_id": "{{YOUR_WORKSPACE_ID}}",     # INT
	"plan_id": "{{YOUR_PLAN_ID}}",               # STRING
	"plan_version": "{{YOUR_PLA_VERSION}}"       # INT
}

client = Client(
		client_id=CONFIG.get('client_id'),
		client_secret=CONFIG.get('client_secret')
)

# Alternatively:
# client = Client().from_json(path="credentials.json")

# Download the plan
plan = client.get_data_plan(
		CONFIG.get('workspace_id'),
		CONFIG.get('plan_id'),
		CONFIG.get('plan_version')
)

# Map events and attributes
# and save as a CSV file
plan.matrix_csv(path='matrix.csv')


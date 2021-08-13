import requests
import json
import logging
from plan import Plan


class Client:

	def __init__(self, client_id=None, client_secret=None, creds_path="credentials.json"):
		self.client_id = client_id
		self.client_secret = client_secret
		if client_id and client_secret:
			creds = {
				"client_id": client_id,
				"client_secret": client_secret,
				"audience": "https://api.mparticle.com",
				"grant_type": "client_credentials"
			}
			self.__access_token = self.get_access_token(creds)
		else:
			creds = self.get_creds_from_json(creds_path)
			self.__access_token = self.get_access_token(creds)

	@staticmethod
	def get_creds_from_json(path):
		with open(path) as f:
			creds = json.load(f)
		return creds

	@property
	def access_token(self):
		return self.__access_token

	@staticmethod
	def get_access_token(creds):
		r = requests.post(
				"https://sso.auth.mparticle.com/oauth/token",
				headers={"Content-Type": "application/json"},
				json=creds
		)
		return r.json().get("access_token")

	def from_json(self, path='credentials.json'):
		creds = self.get_creds_from_json(path)
		access_token = self.get_access_token(creds)
		self.__access_token = access_token
		return self

	def get_data_plan(self, workspace_id: int, plan_id: str, version: int):
		url = f'https://api.mparticle.com/platform/v2/workspaces/{workspace_id}/plans/{plan_id}'
		header = {"Authorization": f'Bearer {self.access_token}'}
		logging.info(f"Fetching data plan at {url} ...")
		r = requests.get(
				url,
				headers=header
		)
		all_plans = r.json().get('data_plan_versions')
		if r.status_code == 200:
			for p in all_plans:
				if p.get('version') == version:
					return Plan(p)
				else:
					logging.warning(f'No version {version} could be found in plan {plan_id}')
		else:
			logging.warning(
					{
						"message": f"No data plan named {plan_id} could be found in the workspace {workspace_id}",
						"code": r.status_code,
						"error": r.text
					}
			)





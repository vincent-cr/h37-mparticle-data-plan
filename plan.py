from munch import munchify
from itertools import chain
import pandas as pd


class Plan:
	def __init__(self, plan_dict):
		self.__data = munchify(plan_dict)
		self.__dict_data = plan_dict

	@property
	def data(self):
		return self.__data

	@property
	def dict(self):
		return self.__dict_data

	@property
	def events(self):
		events = [
			{
				"type": i.match.type,
				"name": i.match.criteria.screen_name
				if i.match.type == "screen_view"
				else i.match.criteria.get('event_name'),
				"attributes": [
					k for k in i.validator.definition.properties.data.properties.custom_attributes.properties
				]
			}
			for i in self.data.version_document.data_points
			if i.match.type not in ["user_identities", "user_attributes"]
		]
		return events

	@property
	def unique_attributes(self):
		unique_attributes = list(set(list(chain.from_iterable([e.get('attributes') for e in self.events]))))
		unique_attributes.sort()
		return unique_attributes

	@property
	def matrix(self):
		matrix = [
			{
				"type": i.get('type'),
				"name": i.get('name'),
				**{j: 'X' if bool(j in i.get('attributes')) else "" for j in self.unique_attributes}
			}
			for i in self.events
		]
		return matrix

	def matrix_csv(self, path='matrix.csv'):
		df = pd.DataFrame(self.matrix)
		return df.sort_values(
				by=["type", "name"]).to_csv(
					path,
					columns=["type", "name"] + self.unique_attributes,
					index=False
				)






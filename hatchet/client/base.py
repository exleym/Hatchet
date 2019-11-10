import logging
from marshmallow import Schema
import requests
from typing import Any
import hatchet.client.models as client_models


logger = logging.getLogger(__name__)


class ResourceClient(object):

    def __init__(self, domain: str, context: str, schema: type(Schema),
                 model: type(client_models.Resource)):
        self.domain = domain
        self.context = context
        self.schema = schema()
        self.model = model

    def get_data(self, url: str, params: dict = None, headers: dict = None):
        params = params or {}
        headers = headers or {}
        resp = requests.get(url=url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def post_data(self, url: str, body: dict = None, headers: dict = None):
        body = body or {}
        headers = headers or {}
        resp = requests.post(url=url, json=body, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def unwrap(self, data):
        many = isinstance(data, list)  # True if data is list else False
        return self.schema.load(data, many=many)

    def list_resources(self, **kwargs):
        return self.unwrap(self.get_data(url=self.base_url, params=kwargs))

    def get_resource_by_id(self, id: int):
        return self.unwrap(self.get_data(url=f"{self.base_url}/{id}"))

    def get_resource_by_code(self, code: str):
        data = self.get_data(url=self.base_url, params={"code": code})
        return self.unwrap(data[0])

    def update_resource(self, resource):
        data = self.schema.dump(resource)
        url = f"{self.base_url}/{resource.id}"
        resp = requests.put(url, json=data)
        resp.raise_for_status()
        return self.unwrap(resp.json())

    def delete_resource(self, id: int):
        url = f"{self.base_url}/{id}"
        resp = requests.delete(url=url)
        resp.raise_for_status()
        return None

    def create_resource(self, **kwargs):
        data = self.schema.dump(kwargs)
        resp = requests.post(self.base_url, json=data)
        resp.raise_for_status()
        return self.unwrap(resp.json())

    def search(self, field: str, op: str, value: Any):
        url = f"{self.base_url}/search"
        pkg = {"filters": [{"field": field, "op": op, "value": value}]}
        resp = requests.post(url, json=pkg)
        return self.unwrap(resp.json())

    @property
    def base_url(self):
        return f"{self.domain}{self.context}"
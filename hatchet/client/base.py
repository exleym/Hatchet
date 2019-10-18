import requests


class BaseClient(object):

    base_url: str

    def get_data(self, url: str, params: dict = None, headers: dict = None):
        params = params or {}
        headers = headers or {}
        resp = requests.get(url=url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def unwrap(self, data):
        return data

    def list_resources(self):
        return [self.unwrap(x) for x in self.get_data(url=self.base_url)]

    def get_resource_by_id(self, id: int):
        url = f"{self.base_url}/{id}"
        return self.unwrap(self.get_data(url=url))

    def get_resource_by_code(self, code: str):
        data = self.get_data(url=self.base_url, params={"code": code})
        return self.unwrap(data[0])

    def create_resource(self, **kwargs):
        resp = requests.post(self.base_url, json=kwargs)
        resp.raise_for_status()
        return self.unwrap(resp.json())

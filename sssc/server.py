
from abc import ABC, abstractmethod
import requests

from enum import Enum

from requests.exceptions import ConnectionError
from time import sleep

class Endpoint(Enum):
    GILLESPY2_MODEL = 1
    GILLESPY2_RESULTS = 2
    CLOUD = 3

class Server(ABC):    

    _endpoints = {
        Endpoint.GILLESPY2_MODEL: "/api/v2/simulation/gillespy2/run",
        Endpoint.GILLESPY2_RESULTS: "/api/v2/simulation/gillespy2/results",
        Endpoint.CLOUD: "/api/v2/cloud"
    }

    def __init__(self) -> None:
        raise TypeError('Server cannot be instantiated directly. Must be ComputeServer or Cluster.')

    @property
    @abstractmethod
    def address(self):
        return NotImplemented

    def post(self, endpoint: Endpoint, sub: str, request = None) -> requests.Response:

        if self.address is NotImplemented:
            raise NotImplementedError

        url = f"{self.address}{self._endpoints[endpoint]}{sub}"

        n_try = 1
        sec = 3
        while n_try <= 3:
            try:
                if request is None:
                    print(f"[POST] {url}")
                    return requests.post(url)
                print(f"[{type(request).__name__}] {url}")
                return requests.post(url, json=request.__dict__)

            except ConnectionError as ce:
                print(f"Connection refused by server. Retrying in {sec} seconds....")
                sleep(sec)
                n_try += 1
                sec *= n_try
            
            except Exception as e:
                print(f"Unknown error: {e}. Retrying in {sec} seconds....")
                sleep(sec)
                n_try += 1
                sec *= n_try


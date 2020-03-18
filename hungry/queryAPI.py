import requests


class BaseAPI(object):
    '''
    The BaseAPI abstract class the provides a convient wrapper for calling get
    requests to requests library.

    Parameters
    ----------
    key : str
        The api key for authorizatiing the use of the api
    version : str
        The argument for the api version
    service : str
        The argument for the url of the api service used

    Attributes
    ----------
    url : str
        The url to query the api
    header: dict{str:str}
        The headers used for the get request
    param: dict{str:str}
        The parameters used of the get requet
    '''

    def query(self, **kwargs):
        query_params = self.param.copy()
        query_params.update(kwargs)
        r = requests.get(
            url=self.url,
            headers=self.header,
            params=query_params
        )
        return r.json()


class YelpAPI(BaseAPI):
    base_url = "https://api.yelp.com/"

    def __init__(self, key, version, service):
        self.url = YelpAPI.base_url + version + "/" + service
        self.header = {"Authorization": "Bearer " + key}


class ChicagoBusAPI(BaseAPI):
    base_url = "http://www.ctabustracker.com/bustime/api/"

    def __init__(self, key, version, service):
        self.url = ChicagoBusAPI.base_url + version + "/" + service
        self.header = {}
        self.param = {
            "key": key,
            "locale": "en",
            "format": "json"
        }

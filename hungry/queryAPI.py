import requests


class BaseAPI(object):
    '''
    The API class the provides a convient wrapper for calling get
    requests to requests library. The initalization of this class is handled
    by the child classes as the authorization is handled differently for each
    API

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
        '''
        A wrapper to the resquests package get request

        Returns
        ----------
        r.json(): dict{}
            Gets the json data from the request and returns a python dictionary
        '''

        query_params = self.param.copy()
        query_params.update(kwargs)
        r = requests.get(
            url=self.url,
            headers=self.header,
            params=query_params
        )
        r.raise_for_status()
        return r.json()


class YelpAPI(BaseAPI):
    base_url = "https://api.yelp.com/"
    __doc__ = BaseAPI.__doc__  # Inherit parent doc string

    def __init__(self, key, version, service):
        self.url = YelpAPI.base_url + version + "/" + service
        # Yelp API authorization is in the header
        self.header = {"Authorization": "Bearer " + key}
        self.param = {
            "locale": "en_US"
        }


class ChicagoBusAPI(BaseAPI):
    base_url = "http://www.ctabustracker.com/bustime/api/"
    __doc__ = BaseAPI.__doc__  # Inherit parent doc string

    def __init__(self, key, version, service):
        self.url = ChicagoBusAPI.base_url + version + "/" + service
        self.header = {}
        # set cta bustime API return format to json in English
        self.param = {
            "key": key,
            "locale": "en",
            "format": "json"
        }

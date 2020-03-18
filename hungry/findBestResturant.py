import hungry.queryAPI as q
import hungry.cta as cta


class FindBestResturants():
    '''
    This class is the primary interface for the application. The initalization
    of this class requires the yelp and cta API keys. Once the class is
    initalized search_by_route method can be called to get the highest rated
    resturant on Yelp 20 meters from a sequence of CTA bus stop on a specified
    route, direction and stop id. This method returns a list containing
    information on each stop and the best rated resturant on yelp

    Parameters
    ----------
    yelp_key: str
        The key to authorize the Yelp API. It is attached to the
        headers in the get request. This key can be aquired here
        https://www.yelp.com/developers
    cta_key: str
        The key nessiary to authorize the Chicago Transit Authority (CTA) bus
        tracker API. It is attached as a parameter to the get request. This
        key can be aquired here
        https://www.transitchicago.com/developers/bustracker/

    Attributes
    ----------
    The attributes of this class are values that need to be changed only
    sporadically. Such as when a new version of an API comes out.

    yelp_api_version: str
        The version of the Yelp API
    cta_api_version: str
        The version of the CTA bustracker API
    yelp_search_business: str
        The API pattern to call the business search service on the Yelp API.
        This service is used to query the best rated resturant near a bus stop
    cta_get_pattern: str
        The API pattern to request a JSON on the bus tacker API that container
        the location information needed to trace the geolocation of a bus
        route. The CTA calls this information patterns.
    next_stops_num: int
        The number of sequencial stops after the next stop that we search for
        the highest rated resturant inclusive of the first next stop

    '''
    yelp_api_version = "v3"
    cta_api_version = "v2"
    yelp_search_business = "businesses/search"
    cta_get_pattern = "getpatterns"
    next_stops_num = 7

    def __init__(self, yelp_key, cta_key):
        self.yelp = q.YelpAPI(
            key=yelp_key,
            version=FindBestResturants.yelp_api_version,
            service=FindBestResturants.yelp_search_business
            )
        self.cta = q.ChicagoBusAPI(
            key=cta_key,
            version=FindBestResturants.cta_api_version,
            service=FindBestResturants.cta_get_pattern
        )

    def search_by_route(self, route_id, direction, next_stop_id):
        '''
        The method called to gets data on the best rated resturant on Yelp
        within 20 meters on a squence of next stops. The number of stops
        considered is set by the class attribute next_stops_num. The sequence
        of next stops is found with parameters on the route number direction
        and the id of the first subsequent stop.

        Parameters
        ----------
        route_id: str
            The identifier of the route to be searched. This value is usally an
            integer between 1 and 200 with some routes having a single
            upper-case letter after the integer
        direction: str
            The direction of the route. Most CTA bus routes have two
            directions. This is use to determine the subsequent stops
        next_stop_id: str
            The id value for the first subsequent stop

        Returns
        ----------
        best_restaurant: dict{}
            A dictionary containing information on the restaurant with the
            highest Yelp reivews.
        '''

        # query for data on stops and parse
        raw_responce = self.cta.query(rt=route_id)
        patterns = raw_responce["bustime-response"]["ptr"]

        # get sequence of subsequent stops
        route = cta.Route(patterns)
        stops = route.get_stop_sequence(next_stop_id, direction, 7)

        # iterate through each stop to find the highest rated restaurant
        best_rating = 0
        best_restaurant = {}
        for stop in stops:
            # call the Yelp API to get the highest rated for a single stop
            restaurant = self._best_resturant_by_stop(stop)
            if restaurant["rating"] > best_rating:
                best_rating = restaurant["rating"]
                best_restaurant.clear()
                best_restaurant.update({restaurant["id"]: restaurant})
            if restaurant["rating"] == best_rating:
                best_restaurant.update({restaurant["id"]: restaurant})

        if len(best_restaurant) == 0:
            return "Yelp found no restaurants"
        return best_restaurant

    def _best_resturant_by_stop(self, stop):
        '''
        A function that quarries for the highest rated restaurant near each
        stop

        Parameters
        ----------
        stop: dict{}
            A dictionary containing the coordinate data needed for the Yelp API

        Returns
        ----------
        best_rated: dict{}
            A dictionary containing the information needed
        '''
        yelp_resp = self.yelp.query(
            latitude=stop["lat"],
            longitude=stop["lon"],
            limit=1,
            radius=20,
            categories="restaurants",
            sort_by="rating"
        )
        if yelp_resp["total"] == 0:
            return {"rating": -1}
        best_rated = yelp_resp["businesses"][0]
        return best_rated

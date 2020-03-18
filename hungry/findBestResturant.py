import queryAPI as q


class FindBestResturants():
    yelp_api_version = "v3"
    cta_api_version = "v2"
    yelp_search_business = "businesses/search"
    cta_get_pattern = "getpattern"
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
            service=FindBestResturants.cta_search_business
        )

    def search_by_route(self, route_num, direction, next_stop):
        self.dirction = direction
        self.next_stop = next_stop
        raw_responce = self.cta.query(rt=route_num)
        self.patterns = raw_responce["bustime-response"]["ptr"]
        for pattern in self.patterns:
            if pattern["rtdir"].lower() == direction:
                next_stops = self.get_next_stops(pattern["pt"])

    def get_next_stops(self, pattern):
        stops = {}
        n = FindBestResturants.next_stops_num
        points = iter(pattern)
        while True:
            try:
                point = next(points)
            except StopIteration:
                break

    def best_resturant_by_stop(self, stop):
        yelp_resp = self.yelp.query({
            "latitude": stop["latitude"],
            "longitude": stop["longitude"],
            "limit": 1,
            "radius": 20,
            "categories": "restaurants",
            "locale": "en_US",
            "sort_by": "rating"
        })


def get_next_stops(route_num, direction, next_stop, n):
    pass

class Route:
    '''
    A class to modularize the data transformation and extraction needed to get
    a list of sequencial stops from the json response from the CTA bustime API.

    Parameters
    ----------
    patterns : list[dicts]
        patterns include data on the waypoints and stops in a bus route with
        some metadata on the bus route such as direction. The pattern
        dictionary is extracted from the bustime API response.

    Attributes
    ----------
    routes : dict{str:dicts}
        The routes variable is a dictionary of dictionary holding data on each
        stop on a route

    dirs_count: int
        The number of directions a route can have. This value are only 1 or 2
        with routes with 2 directions making up the vast majority of routes
    '''

    def __init__(self, patterns):
        self.routes = {}

        # parse and filter the raw pattern data into cleaner route variables
        for route in patterns:
            route_stops_only = select_by_keyvalue(route["pt"], "typ", "S")
            # ensuring that casing won't cause errors
            direction = route["rtdir"].lower()
            self.routes.update({direction: route_stops_only})

        self.dirs_count = len(self.routes.keys())

    def get_reverse_direction(self, current_direction):
        '''
        A Route class method that returns a list containing data on stops in
        the reverse direction as the current direction. This method helps
        handle cases when the next stops are in the reverse direction as the
        bus is nearing a terminus of the route

        Parameters
        ----------
        current_direction: str
            The direction of the route with the first next stop

        Returns
        ----------
        reverse_route: list[dicts]
            The route of the stop with the opposite direction as the first next
            stop. This list also forgoes the first stop in the reverse
            direction to prevent over counting
        '''

        # Some routes only have one direction
        if self.dirs_count == 1:
            reverse_dir = current_direction
        else:
            route_directions = list(self.routes.keys())
            route_directions.remove(current_direction)
            reverse_dir = route_directions.pop()

        # returns everything but the first stop to prevent repetition
        reverse_route = self.routes[reverse_dir][1:]
        return reverse_route

    def get_stop_sequence(self, next_stop, direction, seq_num):
        '''
        A method that takes in the raw pattern data form the CTA bustime API
        and extracts out a list of sequencial stops with the first stop in the
        sequence give by the parameter next_stop. This method assumes that when
        a route reaches its terminus the bus turns around and contines the
        route just in the opposite direction. CTA bus routes only have one or
        two directions

        Parameters
        ----------
        next_stop: str
            The id for the first stop in the returned sequence of stops
        direction: str
            The direction of the route that contains the first next stop
        seq_num: int
            The number of sequencial next stops to return

        Returns
        ----------
        stops_sequnce: list[dicts]
            A list containing stops in sequencial order based on a direction
            and route
        '''

        # Set up nessiary variables and values
        stop_index = get_elem_index(self.routes[direction], next_stop)
        reverse_route = self.get_reverse_direction(direction)

        # join to handle cases where next stops are in the other direction
        subsequent_stops = self.routes[direction][stop_index:] + reverse_route
        return subsequent_stops[:seq_num]


def get_elem_index(elem_list, elem):
    '''
    This functions returns the index of an element in a list of elements

    Parameters
    ----------
    elem_list: list[]
        A list of arbitary objects
    elem: object
        An arbitary object whose index we want returned

    Returns
    ----------
    i: int
        The index of elem in the elem_list
    '''

    i = 0
    for ele in elem_list:
        if ele == elem:
            break
        i += 1
    return i


def select_by_keyvalue(list_of_dicts, key, value):
    '''
    This function takes in list of dictionaries and returns a list of
    dictionaries with only dictionaries containg a specified key value pair

    Parameters
    ----------
    list_of_dicts: list[dict{}]
        A list of dictionaries to be filtered based on key value pair
    key: str
        The key for the dictionaries in the list of dictionaries when matched
        with the specified value will determine if a particualr dictionary
        in the list of dictionaires will be selected
    value: object
        An arbitary value that when matched with the key will determine which
        dictionaries are selected

    Returns
    ----------
    selected: list[dict{}]
        A list of dictionaries containing dictionaires who have the specified
        key value pair
    '''

    selected = []
    for dict in list_of_dicts:
        if key in dict.keys():
            if dict[key] == value:
                selected.append(dict)
    return selected

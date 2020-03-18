class bus_routes:
    def __init__(self):
        pass


class route:
    def __init__(self, ptr):
        self.routes = {}
        for route in ptr:
            route_stops_only = []
            direction = route["rtdir"].lower()

            self.routes.update({direction: route["pt"]})
        self.dirs_count = len(self.routes.key())

    def get_stop_index(pts, next_stop):
        point_index = 0
        for point in pts:
            if point["stpid"] == next_stop:
                break
            point_index += 1
        return point_index

    def get_stop_sequence(self, next_stop, direction, seq_num):
        stops_sequence = []
        stop_index = self.get_stop_index(self.routes["direction"], next_stop)
        next_points = self.routes["direction"][stop_index:]
        for point in next_points and seq_num > 0:
            if point["typ"] == "S":
                stops_sequence.append(point)
                seq_num -= 1
        if seq_num > 0:
            self.reverse_direction(direction, seq_num)
        return stops_sequence

    def reverse_direction(self, old_direction, stops_left):
        directions = [self.routes.key()]
        if len(directions) > 1:
            for dir in directions:
                if dir != old_direction:
                    direction = dir
        else:
            direction = old_direction
        for point in self.routes[direction]:
            pass


# takes in a dict and returns a dict with only keys in the key list
def reduce_dict_by_key(dict, key_list):
    filtered = {}
    for k in dict.key():
        if k in key_list:
            filtered.update({k: dict[k]})
    return filtered


# takes in list of dict and returns a list of dicts with the key and value
def select_by_keyvalue(list_of_dicts, key, value):
    selected = []
    for dict in list_of_dicts:
        pass
    return selected

class Algorithms(object):
    
    def dj(nodes, costs, start_node):
        """
        Dijkstra's algorithm for computing the minimum additive cost from a start node to all other nodes.
        :param nodes: all unique nodes
        :param costs: costs from one node to another
        :param start_node: start node
        :return: minimum additive cost from start node to all other nodes
        """
        unvisited_nodes = {node: None for node in nodes}
        visited_nodes = {}
        current_node = start_node
        current_cost = 0
        unvisited_nodes[current_node] = current_cost
        while True:
            for neighbor, cost in costs[current_node].items():
                if neighbor not in unvisited_nodes:
                    continue
                new_cost = current_cost + cost
                if unvisited_nodes[neighbor] is None or new_cost < unvisited_nodes[neighbor]:
                    unvisited_nodes[neighbor] = new_cost
            visited_nodes[current_node] = current_cost
            del unvisited_nodes[current_node]
            if not unvisited_nodes:
                break
            candidates = [node for node in unvisited_nodes.items() if node[1]]

            # we need the maximum, so sort from largest to smallest
            current_node, current_cost = sorted(candidates, key=lambda x: x[1], reverse=False)[0]
        return visited_nodes


class Network(object):
    def __init__(self, file_name, by_distance=True):
        self.__cities = []
        self.__cities_as_index = []
        self.__costs = {}
        self.__by_distance = by_distance
        self.read_from_file(file_name)

    def cities(self):
        return self.__cities

    def cities_as_index(self):
        return self.__cities_as_index

    def city_by_index(self, index):
        return self.__cities[index]

    def costs(self):
        return self.__costs

    def compute_cost(self, distance):
        cost = 0.0
        if distance > 2000:
            cost += 0.002 * (distance - 2000) + 0.003 * 1000 + 0.004 * 500 + 0.005 * 500
        elif distance > 1000:
            cost += 0.003 * (distance - 1000) + 0.004 * 500 + 0.005 * 500
        elif distance > 500:
            cost += 0.004 * (distance - 500) + 0.005 * 500
        else:
            cost += 0.005 * distance
        return cost

    def read_from_file(self, file_name, delimeter=','):
        f = open(file_name, 'r')
        lines = f.readlines()
        print(lines)
        for line in lines:
            fields = line.rstrip().split(delimeter)
            city_1 = fields[0].strip(' ')
            city_2 = fields[1].strip(' ')
            distance = float(fields[2])

            # build the list of cities
            if city_1 not in self.__cities:
                self.__cities.append(city_1)
            if city_2 not in self.__cities:
                self.__cities.append(city_2)

            # build the dictionary of costs
            cost = self.compute_cost(distance) if not self.__by_distance else distance
            if self.__cities.index(city_1) not in self.__costs.keys():
                self.__costs[self.__cities.index(city_1)] = {self.__cities.index(city_2): cost}
            if self.__cities.index(city_2) not in self.__costs[self.__cities.index(city_1)].keys():
                self.__costs[self.__cities.index(city_1)][self.__cities.index(city_2)] = cost

        self.__cities_as_index = [self.__cities.index(x) for x in self.__cities]
        self.__costs = Network.make_two_way(self.__costs)

    
    def make_two_way(one_way):
        network = one_way.copy()
        for k_outer, v_outer in one_way.items():
            for k_inner, v_inner in v_outer.items():
                if k_inner not in network:
                    network[k_inner] = {}
                if k_inner not in network[k_inner].keys():
                    network[k_inner][k_outer] = v_inner
        return network


def driver():
    print('-' * 24)
    print('Network Analysis')
    print('-' * 24)
    response_by_distance = int(input('Computing by (0 for distance or 1 for costs)? '))

    # build the network of cities and costs
    file_name = r'C:\Users\Aditya Didwania\Desktop\Brandeis\Sem II\Bus 215 Python and Applications to Business Analytics\Assignment 3\Network.csv'
    network = Network(file_name, by_distance=response_by_distance == 0)

    # determine the start city
    for (index, city) in enumerate(network.cities()):
        print(f'{index}: {city:s}')
    start_city = int(input(f'What is the start city by index (0 to {max(network.cities_as_index()):d})? '))

    paths = Algorithms.dj(network.cities_as_index(), network.costs(), start_city)
    for k, v in paths.items():
        print(f'{network.city_by_index(start_city)} : {network.city_by_index(k)} = {round(v, 4)}')


if __name__ == '__main__':
    driver()

class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.resources = {
            "brick": 0,
            "lumber": 0,
            "wool": 0,
            "grain": 0,
            "ore": 0
        }
        self.victory_points = 0
        self.roads = []
        self.settlements = []
        self.cities = []
        self.dev_cards = []
        self.played_knights = 0

    def add_resource(self, resource_type, amount=1):
        if resource_type in self.resources:
            self.resources[resource_type] += amount

    def spend_resources(self, cost_dict):
        for resource, cost in cost_dict.items():
            if self.resources[resource] < cost:
                return False
        for resource, cost in cost_dict.items():
            self.resources[resource] -= cost
        return True
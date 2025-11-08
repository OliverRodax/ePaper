import json


class Plants():
    def __init__(self):
        self.plants = self.read_plants()

    def read_plants(self):
        with open("src/plants/my_plants.json", 'r') as f:
            plant_data = json.load(f)
            
        return plant_data

Plants()


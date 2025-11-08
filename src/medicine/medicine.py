import json

class Medicine():
    def __init__(self):
        self.medicine = self.read_medicine()

    def read_medicine():
        with open("src/plants/my_plants.json", 'r') as f:
            plant_data = json.load(f)
            
        return plant_data
import json
from datetime import date, timedelta


class Plants:
    def __init__(self):
        self.plants = self.read_plants()

    def read_plants(self):
        with open("src/data/my_plants.json", "r") as f:
            plant_data = json.load(f)
        return plant_data

    def update_plants(self):
        self.plants = self.read_plants()
        today = date.today()
        for plant in self.plants:
            water_date = date.fromisoformat(plant["water_date"])
            if water_date < today:
                new_water_date = today + timedelta(
                    days=(plant["watering"] - 1)
                )  # minus one because it updates one day later
                plant["water_date"] = new_water_date.isoformat()
        with open("src/data/my_plants.json", "w") as f:
            json.dump(self.plants, f, ensure_ascii=False, indent=2)

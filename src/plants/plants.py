import json
from datetime import date, timedelta
import os


class Plants:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.plants = self.read_plants()
        self.plants_water_today = self.read_water_today()
        

    def read_plants(self):
        file_path = os.path.join(self.current_dir, "data", "my_plants.json")
        with open(file_path, "r") as f:
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
        file_path = os.path.join(self.current_dir, "data", "my_plants.json")
        with open(file_path, "w") as f:
            json.dump(self.plants, f, ensure_ascii=False, indent=2)
        self.read_water_today()

    def read_water_today(self):
        self.plants = self.read_plants()
        today = date.today()
        plants_water_today = []
        for i,plant in enumerate(self.plants):
            water_date = date.fromisoformat(plant["water_date"])
            if water_date == today:
                plants_water_today.append(plant)
        self.plants_water_today = plants_water_today
        return plants_water_today
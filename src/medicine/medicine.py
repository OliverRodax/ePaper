import json
from datetime import date, timedelta


class Medicine:
    def __init__(self):
        self.medicine = self.read_medicine()
        self.today_medicine = self.read_today_medicine()

    def read_medicine(self):
        with open("src/data/my_medicine.json", "r") as f:
            self.medicine = json.load(f)

        return self.medicine

    def update_medicine(self):
        self.medicine = self.read_medicine()
        today = date.today()
        for medicine in self.medicine:
            take_date = date.fromisoformat(medicine["take_date"])
            if take_date < today:
                new_take_date = today + timedelta(
                    days=(medicine["how_often"] - 1)
                )  # minus one because it updates one day later
                medicine["take_date"] = new_take_date.isoformat()
        with open("src/data/my_medicine.json", "w") as f:
            json.dump(self.medicine, f, ensure_ascii=False, indent=2)

    def read_today_medicine(self):
        self.medicine = self.read_medicine()
        today = date.today()
        today_medicine = []
        for i,medicine in enumerate(self.medicine):
            take_date = date.fromisoformat(medicine["take_date"])
            if take_date == today:
                today_medicine.append(medicine)
        self.today_medicine = today_medicine
        return today_medicine

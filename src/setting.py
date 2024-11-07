import json
import os

class Settings:
    def __init__(self):
        self.settings_file = 'settings.json'
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = self.get_default_settings()
            self.save_settings()

    def save_settings(self):
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def get_default_settings(self):
        return {
            "telegram_token": "",
            "telegram_chat_id": "",
            "threshold": 3.0,
            "coins": ["BTC", "ETH", "XRP", "SOL"],
            "refresh_rate": 30,
            "sound_alert": True,
            "fees": {
                "upbit": {"maker": 0.0005, "taker": 0.0005},
                "binance": {"maker": 0.001, "taker": 0.001},
                "wire": 5000
            }
        }
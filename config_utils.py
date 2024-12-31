import json
import os


class ConfigManager:
    def __init__(self, module_name, config_dir="configs"):
        self.module_name = module_name
        self.config_dir = config_dir
        self.config_path = os.path.join(config_dir, (f"{module_name}.json"))
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.config_path, "w+") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set_config(self, key, value):
        self.config[key] = value
        self._save()

    def to_string(self):
        return json.dumps(self.config, indent=4)


if __name__ == "__main__":
    cat = ConfigManager("earth")
    print(cat.config_path)
    cat.set_config("speed", 0.5)
    print(cat.to_string())

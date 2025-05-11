import json
import os

class ProfileManager:
    def __init__(self, profile_dir='profiles'):
        self.profile_dir = profile_dir
        os.makedirs(self.profile_dir, exist_ok=True)

    def save_profile(self, profile_name, data):
        filepath = os.path.join(self.profile_dir, f"{profile_name}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Profile '{profile_name}' saved."

    def load_profile(self, profile_name):
        filepath = os.path.join(self.profile_dir, f"{profile_name}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Profile '{profile_name}' not found.")

    def list_profiles(self):
        return [f.replace('.json', '') for f in os.listdir(self.profile_dir) if f.endswith('.json')]

    def delete_profile(self, profile_name):
        filepath = os.path.join(self.profile_dir, f"{profile_name}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return f"Profile '{profile_name}' deleted."
        else:
            raise FileNotFoundError(f"Profile '{profile_name}' not found.")

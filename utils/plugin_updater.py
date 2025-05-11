import os
import subprocess
import importlib.util

class PluginUpdater:
    def __init__(self, plugin_dir='modules'):
        self.plugin_dir = plugin_dir

    def update_plugins(self):
        updated = []
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                path = os.path.join(self.plugin_dir, filename)
                updated.append(self._git_pull(path))
        return updated

    def _git_pull(self, path):
        repo_dir = os.path.dirname(path)
        try:
            if os.path.isdir(os.path.join(repo_dir, '.git')):
                result = subprocess.run(['git', '-C', repo_dir, 'pull'],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                return {'plugin': repo_dir, 'output': result.stdout.strip()}
            else:
                return {'plugin': repo_dir, 'output': 'Not a git repository.'}
        except Exception as e:
            return {'plugin': repo_dir, 'output': f'Error: {e}'}

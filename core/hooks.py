class Hooks:
    def __init__(self):
        self.hooks = {}
        self.plugin_commands = {}  # To store plugin commands

    def register_hook(self, hook_name, hook_function):
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(hook_function)

    def execute_hooks(self, hook_name, *args, **kwargs):
        if hook_name in self.hooks:
            for hook in self.hooks[hook_name]:
                hook(*args, **kwargs)

    def set_plugin_commands(self, plugin_name, commands):
        """Store the list of command handlers for a specific plugin."""
        self.plugin_commands[plugin_name] = commands

    def get_plugin_commands(self, plugin_name):
        """Retrieve the list of command handlers for a specific plugin."""
        return self.plugin_commands.get(plugin_name, [])

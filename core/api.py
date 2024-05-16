class CoreAPI:
    def __init__(self, db):
        self.db = db
        self.actions = {}

    def register_action(self, plugin_name, action_name, action_function):
        if plugin_name not in self.actions:
            self.actions[plugin_name] = {}
        self.actions[plugin_name][action_name] = action_function

    def execute_action(self, plugin_name, action_name, *args, **kwargs):
        if plugin_name in self.actions and action_name in self.actions[plugin_name]:
            return self.actions[plugin_name][action_name](*args, **kwargs)
        return None

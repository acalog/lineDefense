

class BaseState:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def enter(self, params=None):
        pass

    def exit(self):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass

    def handle_event(self, events):
        pass

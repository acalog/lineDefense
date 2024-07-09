from states.basestate import BaseState


class StateMachine:
    def __init__(self, states=None):
        self.empty = BaseState(self)
        self.states = states or {}
        self.current = self.empty

    def change(self, state_name, enter_params=None):
        assert state_name in self.states, "State must exist!"
        self.current.exit()
        self.current = self.states[state_name]()
        self.current.enter(enter_params)

    def update(self):
        self.current.update()

    def render(self, screen):
        self.current.render(screen)

    def handle_event(self, events):
        self.current.handle_event(events)

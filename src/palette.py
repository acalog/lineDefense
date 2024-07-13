

class Palette:
    def __init__(self):
        self.colors = {
            'RED': (255, 0, 0),
            'WHITE': (255, 255, 255),
            'LAND': (103, 114, 91),
            'BLUE': (0, 0, 255),
            'GREEN': (0, 255, 0),
            'PROJECTILE_RED': (255, 51, 51),
            'SKY': (38, 208, 208)
        }

    def get(self, color):
        return self.colors[color.upper()]

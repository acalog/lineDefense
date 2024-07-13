

class HealthBar:
    def __init__(self):
        self.MAX = 255
        self.MIN = 0
        self.step = 5
        self.bar_color = [
            0,
            155,
            255
        ]

    def get_red(self):
        return self.bar_color[0]

    def get_green(self):
        return self.bar_color[1]

    def get_blue(self):
        return self.bar_color[2]

    def update_color(self, index, increment=True):
        """
        Increments or decrements the value at index
        :param index:
        :param increment:
        :return void:
        """
        if increment:
            self.bar_color[index] = min(self.bar_color[index] + self.step, self.MAX)
        else:
            self.bar_color[index] = max(self.bar_color[index] - self.step, self.MIN)

    def update(self, health_percent):
        """
        Sets rgb values for health bar given percent of health remaining
        :param health_percent:
        :return void:
        """
        if 0.75 < health_percent < 1:
            self.update_color(1, increment=True)
            self.update_color(2, increment=False)
        elif 0.5 < health_percent < 0.75:
            self.update_color(0, increment=True)
            self.update_color(1, increment=True)
            self.update_color(2, increment=False)
        elif 0.25 < health_percent < 0.5:
            self.update_color(0, increment=True)
            self.update_color(1, increment=False)
            self.update_color(2, increment=False)
        elif 0.10 < health_percent < 0.25:
            self.update_color(0, increment=True)
            self.update_color(1, increment=False)
            self.update_color(2, increment=False)

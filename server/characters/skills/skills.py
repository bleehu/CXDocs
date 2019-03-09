
class skill:

    def __init__(self, name, points, profficient):
        self.name = name
        self.points = int(points)
        self.profficient = profficient

    def valid(self):
        if self.name.trim() == "":
            return False
        if self.points < 0:
            return False
        return True
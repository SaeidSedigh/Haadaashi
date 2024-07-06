
class M_Nakshatra():
    def __init__(self, name, pada):
        self.Name = name
        self.Pada = pada

    def __repr__(self):
        return f"{self.Name} Pada {self.Pada}"

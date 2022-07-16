import jsonpickle
from layout import Layout


def save_layout(layout, filename):
    json = jsonpickle.encode(layout)
    f = open(filename, "w")
    f.write(json)
    f.close()

def load_layout(filename) -> Layout:
    f = open(filename, "r")
    json = f.read()
    return jsonpickle.decode(json)

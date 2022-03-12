import jsonpickle

from src.album_project.album import Album, Vector2, Page, Photo
from src.layout_creation.layout import Layout


def save_album(album: Album, filename: str):
    json = jsonpickle.encode(album)
    f = open(filename, "w")
    f.write(json)
    f.close()


def load_album(filename: str) -> Album:
    f = open(filename, "r")
    json = f.read()
    return jsonpickle.decode(json)


def layout_to_page(layout: Layout) -> Page:
    leaves = layout.get_leaf_nodes()
    size = Vector2(layout.width, layout.height)
    page = Page(size, layout.border, layout.border_color)

    for leaf in leaves:
        data = leaf.data
        photo = Photo(data.rect, data.image)
        page.add_photo(photo)

    return page
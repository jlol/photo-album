from src.utils.image_cache import ImageCache
from PIL import Image


class Size:
    def __init__(self, w, h):
        self.width = w
        self.height = h


class LayoutImageProvider:

    def __init__(self, filenames: [str], image_cache: ImageCache):
        self.__paths = filenames
        self.__image_cache = image_cache

    def get_image_by_index(self, index):
        if index < 0 or index > self.number_of_images():
            print("Using wrong image index")
            return Image.new(mode="RGB", size=(4, 4))

        return self.__image_cache.get_image(self.__paths[index])

    def number_of_images(self) -> int:
        return len(self.__paths)

    def get_sizes(self) -> [Size]:
        sizes = []

        for p in self.__paths:
            size = self.__image_cache.get_image(p).size
            sizes.append(Size(size[0], size[1]))

        return sizes

    def get_ratios(self) -> [float]:
        ratios = []

        for p in self.__paths:
            size = self.__image_cache.get_image(p).size
            ratios.append(size[0] / size[1])

        return ratios

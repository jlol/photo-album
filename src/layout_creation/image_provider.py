from typing import List
from PIL import Image


class Size:
    def __init__(self, w, h):
        self.width = w
        self.height = h


class ImageProvider:

    def __init__(self):
        self.__img_dict = {}

    def add_image(self, image_path) -> bool:
        if image_path in self.__img_dict:
            return True

        image = Image.open(image_path)

        if image is None:
            print("[ImageProvider] Error reading image " + image_path)
            return False

        self.__img_dict[image_path] = image
        return True

    def get_image(self, image_path):
        if image_path not in self.__img_dict:
            print("[ImageProvider] Trying to open non-added image")

            if not self.add_image(image_path):
                print("[ImageProvider] Wrong image path")
                return Image.new(mode="RGB", size=(4, 4))

        return self.__img_dict[image_path]

    def get_image_by_index(self, index):
        if index < 0 or index > self.number_of_images():
            print("Using wrong image index")
            return Image.new(mode="RGB", size=(4, 4))

        return list(self.__img_dict.values())[index]

    def cleanup(self):
        for i in self.__img_dict.values():
            del i
        self.__img_dict = {}

    def number_of_images(self) -> int:
        return len(self.__img_dict)

    def get_sizes(self) -> [Size]:
        sizes = []

        for i in self.__img_dict.values():
            size = i.size
            sizes.append(Size(size[0], size[1]))

        return sizes

    def get_ratios(self) -> [float]:
        ratios = []

        for i in self.__img_dict.values():
            size = i.size
            ratios.append(size[0] / size[1])

        return ratios

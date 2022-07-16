from PIL import Image


class ImageCache:

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

    def cleanup(self):
        for i in self.__img_dict.values():
            del i
        self.__img_dict = {}

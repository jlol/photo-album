# TODO: improve scoring system!!!! Currently having one
# good fix for an image weighs too much!!
# TODO: when selecting images in layout creator, check if there
# is more than one fit and then select randomly between them
# TODO: add weight per image in layout creator, more score if
# that image gets bigger and better ratio
# from src.album_project import album_utils
# from src.layout_creation.image_provider import ImageProvider
# from src.layout_creation.layout_creator import LayoutCreator
# from src.layout_creation.layout_renderer import LayoutRenderer
#
# BORDER = 8
# MAX_ITERATIONS = 20
# border_color = (255, 255, 255)
# output_size = (2000, 1400)
#
# ip = ImageProvider()
# ip.add_image("../img/0.jpg")
# ip.add_image("../img/1.jpg")
# ip.add_image("../img/2.jpg")
#
# lc = LayoutCreator(output_size, ip, BORDER, border_color)
# layout = lc.create_layout()
# best_score = layout.score
#
# for i in range(0, MAX_ITERATIONS):
#     tmp_layout = lc.create_layout()
#
#     if tmp_layout.score < layout.score:
#         best_score = tmp_layout.score
#         layout = tmp_layout
#
# album = album_utils.layout_to_page(layout)
#
# renderer = LayoutRenderer(layout, output_size, ip)
# im = renderer.render()
# im.save("result.png")


import ui.main_window
ui.main_window.show_window()

import random
from typing import Tuple
from random import randint
from anytree import Node

from src.utils.image_cache import ImageCache
from src.layout_creation.layout import Layout
from src.layout_creation.node_data import SplitType, NodeData
from src.layout_creation.rect import Rect


class LayoutCreator:

    def __init__(
            self, size: Tuple[int, int],
            image_provider: ImageCache, border: int,
            border_color
    ):
        self.width = size[0]
        self.height = size[1]
        self.__image_provider = image_provider
        self.border = border
        self.border_color = border_color

    def create_layout(self) -> Layout:
        assert self.__image_provider.number_of_images() > 0, "Trying to create a layout without images"
        self.layout = Layout(self.width, self.height,
                             self.border, self.border_color)
        self.__generate_random_tree()
        self.__assign_pics()
        self.__update_neighbours(self.layout.root)
        return self.layout

    def __generate_random_tree(self):
        active_leaves = [self.layout.root]
        horizontal_split_index = SplitType.HORIZONTAL.value
        vertical_split_index = horizontal_split_index + 1
        image_count = self.__image_provider.number_of_images()

        while len(active_leaves) < image_count:
            node = random.choice(active_leaves)
            active_leaves.remove(node)
            random_split = randint(horizontal_split_index,
                                   vertical_split_index)

            self.__split(node, random_split, active_leaves)

    def __split(self, node, split_type_value, active_leaves):
        node.data.split = SplitType(split_type_value)
        node.name = node.data.split.name[0]
        rect = node.data.rect

        ldata, rdata = self.__get_child_data(node.data.split, rect)
        left_child = Node("l", data=ldata, parent=node)
        right_child = Node("r", data=rdata, parent=node)

        active_leaves.append(left_child)
        active_leaves.append(right_child)

    def __get_child_data(
            self, split_type, parent_rect
    ) -> Tuple[Rect, Rect]:
        if split_type == SplitType.HORIZONTAL:
            ldata = NodeData(Rect(parent_rect.x, parent_rect.y,
                                  parent_rect.w, parent_rect.h * 0.5))
            rdata = NodeData(Rect(
                parent_rect.x, parent_rect.y + parent_rect.h * 0.5,
                parent_rect.w, parent_rect.h * 0.5))

            return ldata, rdata

        ldata = NodeData(Rect(parent_rect.x, parent_rect.y,
                              parent_rect.w * 0.5, parent_rect.h))
        rdata = NodeData(Rect(
            parent_rect.x + parent_rect.w * 0.5,
            parent_rect.y, parent_rect.w * 0.5, parent_rect.h))
        return ldata, rdata

    def __assign_pics(self):
        self.layout.score = 0
        image_ratios = self.__image_provider.get_ratios()
        pending_indices = list(
            range(0, self.__image_provider.number_of_images())
        )
        leaf_nodes = self.layout.get_leaf_nodes()

        for leaf in leaf_nodes:
            ratio = leaf.data.rect.get_ratio()
            index, diff = self.__get_best_image_for_ratio(
                ratio, image_ratios, pending_indices)
            img = self.__image_provider.get_image_by_index(index)

            leaf.data.image = img.filename
            leaf.name = img.filename
            pending_indices.pop(pending_indices.index(index))
            self.layout.score += diff

    def __get_best_image_for_ratio(
            self, ratio, image_ratios, pending_indices
    ) -> Tuple[int, float]:
        best_index = pending_indices[0]
        best_ratio_diff = abs(image_ratios[best_index] - ratio)

        for i in pending_indices:
            ratio_diff = abs(image_ratios[i] - ratio)

            if best_ratio_diff > ratio_diff:
                best_index = i
                best_ratio_diff = ratio_diff

        return best_index, best_ratio_diff

    def __update_neighbours(self, parent):

        if len(parent.children) == 0:
            return

        parent_data = parent.data
        child0 = parent.children[0]
        data0 = child0.data
        child1 = parent.children[1]
        data1 = child1.data

        data0.copy_neighbours_mask(parent_data)
        data1.copy_neighbours_mask(parent_data)

        if parent.data.split == SplitType.HORIZONTAL:
            data0.set_neighbour(NodeData.BOTTOM_NEIGHBOUR, True)
            data1.set_neighbour(NodeData.TOP_NEIGHBOUR, True)
        else:
            data0.set_neighbour(NodeData.RIGHT_NEIGHBOUR, True)
            data1.set_neighbour(NodeData.LEFT_NEIGHBOUR, True)

        self.__update_neighbours(child0)
        self.__update_neighbours(child1)

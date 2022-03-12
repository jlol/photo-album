from anytree import Node, RenderTree, AsciiStyle, search

from src.layout_creation.node_data import NodeData
from src.layout_creation.rect import Rect


class Layout:

    def __init__(self, w: int, h: int, border: int, border_color):
        self.width = w
        self.height = h
        self.border = border
        self.border_color = border_color
        data = NodeData(Rect(0, 0, w, h))
        self.root = Node("root", data=data, parent=None)
        # TODO: find more elegant way of initializing score
        self.score = 1000000000000

    def get_leaf_nodes(self) -> [Node]:
        return search.findall(
            self.root, filter_=lambda node: len(node.children) == 0
        )

    def __str__(self):
        return (RenderTree(self.root, style=AsciiStyle()).by_attr())

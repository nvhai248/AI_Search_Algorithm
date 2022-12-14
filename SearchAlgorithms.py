from Space import *
from Constants import *


def is_Exist(arr: list[Node], val: Node):
    for i in range(0, len(arr)):
        if arr[i].value == val.value:
            return True

    return False


def printList(list: list[Node]):
    node = []
    for index in list:
        node.append(index.value)

    print(node)


def distanceNode(node1: Node, node2: Node):
    return sqrt(pow(node1.x - node2.x, 2) + pow(node1.y - node2.y, 2))


def set_Color_Path(g: Graph, path: [], sc: pygame.surface):

    g.re_draw(g.goal, grey, sc)
    prev = g.goal.value
    while prev != g.start.value:
        pygame.draw.line(sc, green, (g.grid_cells[prev].x, g.grid_cells[prev].y), (
            g.grid_cells[path[prev]].x, g.grid_cells[path[prev]].y), 2)
        pygame.display.flip()
        prev = path[prev]
        g.re_draw(g.grid_cells[prev], grey, sc)
        # path[i].set_color(grey)


""" def findMinCost(g: Graph, l: list[Node]):
    min = 99999
    result: Node = l[0]
    for index in l:
        if min > g.calculatorCost(index):
            min = g.calculatorCost(index)
            result = index

    return result """


def returnMinNodeCostWithHeuristic(g: Graph, open_set: list[Node], cost: []):
    min = 99999
    result = open_set[0]
    for node in open_set:
        if min > cost[node.value] + g.heuristic(node):
            min = cost[node.value] + g.heuristic(node)
            result = node

    return result


def returnNodeMinCost(g: Graph, open_set: list[Node], cost: []):
    min = 99999
    result = open_set[0]
    for node in open_set:
        if min > cost[node.value]:
            min = cost[node.value]
            result = node
    print(min)
    return result


def BFS_algorithm(g: Graph, open_set: list[Node], closed_set: list[Node], father: [], sc: pygame.surface):
    if len(open_set) == 0:
        return

    current_List: list[Node] = []
    current_List = current_List + open_set
    while len(current_List) != 0:
        current_Node: Node = current_List[0]
        if current_Node.value != g.start.value:
            g.re_draw(current_Node, yellow, sc)
        # ki???m tra xem t??m th???y node c???n t??m ch??a
        # n???u t??m th???y r => b??i m??u rgey ???????ng ??i
        # n???u ch??a th?? ki???m th??m node ??ang x??t v??o closed, x??a kh???i open
        # th??m v??o open c??c neighbors c???a node
        if g.is_goal(current_Node):
            set_Color_Path(g, father, sc)
            return

        # th??m v??o closed_set
        open_set.remove(current_Node)
        closed_set.append(current_Node)
        current_List.remove(current_Node)
        # current_Node.set_color(blue)
        # th??m v??o open_set
        neighbors: list[Node] = g.get_neighbors(current_Node)
        while len(neighbors) != 0:
            if not is_Exist(closed_set, neighbors[0]):
                if not is_Exist(open_set, neighbors[0]):
                    if neighbors[0].value != g.goal.value:
                        g.re_draw(neighbors[0], red, sc)
                    open_set.append(neighbors[0])
                    father[neighbors[0].value] = current_Node.value

            neighbors.remove(neighbors[0])

        if current_Node.value != g.start.value:
            g.re_draw(current_Node, blue, sc)

    BFS_algorithm(g, open_set, closed_set, father, sc)


def DFS_algorithm(g: Graph, open_set: list[Node], closed_set: list[Node], father: [], sc: pygame.surface):
    if len(open_set) == 0:
        return

    # l???y ??i???m g???n nh???t ???????c m??? t???i
    current_Node: Node = open_set[len(open_set) - 1]
    if current_Node.value != g.start.value:
        g.re_draw(current_Node, yellow, sc)

    if (g.is_goal(current_Node)):
        set_Color_Path(g, father, sc)
        return

    # x??a ??i???m ???? kh???i t???p m??? v?? th??m v??o t???p ????ng
    open_set.remove(current_Node)
    closed_set.append(current_Node)

    # t???o ra t???p ch???a c??c neighbors
    # th??m v??o sau open_set khi ??i???m ???? k c?? trong open_set v?? closed_set
    neighbors: list[Node] = g.get_neighbors(current_Node)
    while len(neighbors) != 0:
        if not is_Exist(closed_set, neighbors[len(neighbors) - 1]):
            if not is_Exist(open_set, neighbors[len(neighbors) - 1]):
                if neighbors[len(neighbors) - 1].value != g.goal.value:
                    g.re_draw(neighbors[len(neighbors) - 1], red, sc)
                open_set.append(neighbors[len(neighbors) - 1])
                father[neighbors[len(neighbors) -
                                 1].value] = current_Node.value

        neighbors.remove(neighbors[len(neighbors) - 1])

    # t?? l???i m??u
    if current_Node.value != g.start.value:
        g.re_draw(current_Node, blue, sc)

    DFS_algorithm(g, open_set, closed_set, father, sc)


def UCS_algorithm(g: Graph, open_set: list[Node], closed_set: list[Node], cost: [], father: [], sc: pygame.surface):
    if len(open_set) == 0:
        return
    # printList(open_set)
    # x??c ?????nh ??i???m x??t t???i
    current_Node: Node = returnNodeMinCost(g, open_set, cost)
    if current_Node.value != g.start.value:
        g.re_draw(current_Node, yellow, sc)

    # ki???m tra xem ??i???m ??ang x??t c?? ph???i l?? goal kh??ng
    if g.is_goal(current_Node):
        set_Color_Path(g, father, sc)
        return

    # x??a kh???i open_set v?? th??m v??o closed_set
    open_set.remove(current_Node)
    closed_set.append(current_Node)

    # ki???m tra c??c bi??n v?? update cost
    neighbors: list[Node] = g.get_neighbors(current_Node)
    while len(neighbors) != 0:
        if not is_Exist(closed_set, neighbors[0]):
            if not is_Exist(open_set, neighbors[0]):
                if neighbors[0].value != g.goal.value:
                    g.re_draw(neighbors[0], red, sc)
                cost[neighbors[0].value] = cost[current_Node.value] + \
                    distanceNode(current_Node, neighbors[0])
                open_set.append(neighbors[0])
                father[neighbors[0].value] = current_Node.value

        neighbors.remove(neighbors[0])

    if current_Node.value != g.start.value:
        g.re_draw(current_Node, blue, sc)
    UCS_algorithm(g, open_set, closed_set, cost, father, sc)


def AStar_Algorithm(g: Graph, open_set: list[Node], closed_set: list[Node], cost: [], father: [], sc: pygame.surface):
    if len(open_set) == 0:
        return

    # x??c ?????nh ??i???m x??t t???i
    current_Node: Node = returnMinNodeCostWithHeuristic(g, open_set, cost)
    if current_Node.value != g.start.value:
        g.re_draw(current_Node, yellow, sc)

    # ki???m tra xem ??i???m ??ang x??t c?? ph???i l?? goal kh??ng
    if g.is_goal(current_Node):
        set_Color_Path(g, father, sc)
        return

    # x??a kh???i open_set v?? th??m v??o closed_set
    open_set.remove(current_Node)
    closed_set.append(current_Node)

    # ki???m tra c??c bi??n v?? update cost
    neighbors: list[Node] = g.get_neighbors(current_Node)
    while len(neighbors) != 0:
        if not is_Exist(closed_set, neighbors[0]):
            if not is_Exist(open_set, neighbors[0]):
                if neighbors[0].value != g.goal.value:
                    g.re_draw(neighbors[0], red, sc)
                cost[neighbors[0].value] = cost[current_Node.value] + \
                    distanceNode(current_Node, neighbors[0])
                open_set.append(neighbors[0])
                father[neighbors[0].value] = current_Node.value

        neighbors.remove(neighbors[0])

    if current_Node.value != g.start.value:
        g.re_draw(current_Node, blue, sc)
    AStar_Algorithm(g, open_set, closed_set, cost, father, sc)


def DFS(g: Graph, sc: pygame.Surface):
    print('Implement DFS algorithm')

    # n??t m??? v???i b???t ?????u l?? ??i???m b???t ?????u
    # t???p ????ng ???
    # t???o ra 1 array v???i len = len(g)
    open_set: list[Node] = []
    open_set.append(g.start)
    closed_set: list[Node] = []
    father: list[Node] = []
    father = [-1]*g.get_len()

    DFS_algorithm(g, open_set, closed_set, father, sc)
    # TODO: Implement DFS algorithm using open_set, closed_set, and father
    """ raise NotImplementedError('Not implemented') """


def BFS(g: Graph, sc: pygame.Surface):
    print('Implement BFS algorithm')

    open_set: list[Node] = []
    open_set.append(g.start)
    closed_set: list[Node] = []
    father = [-1]*g.get_len()

    # TODO: Implement BFS algorithm using open_set, closed_set, and father
    BFS_algorithm(g, open_set, closed_set, father, sc)


def UCS(g: Graph, sc: pygame.Surface):
    print('Implement UCS algorithm')

    father = [-1]*g.get_len()
    cost = [0]*g.get_len()
    cost[g.start.value] = 0

    open_set: list[Node] = []
    open_set.append(g.start)
    closed_set: list[Node] = []

    UCS_algorithm(g, open_set, closed_set, cost, father, sc)
    # TODO: Implement UCS algorithm using open_set, closed_set, and father
    """ raise NotImplementedError('Not implemented') """


def AStar(g: Graph, sc: pygame.Surface):
    print('Implement A* algorithm')

    father = [-1]*g.get_len()
    cost = [0]*g.get_len()
    cost[g.start.value] = 0

    open_set: list[Node] = []
    open_set.append(g.start)
    closed_set: list[Node] = []

    AStar_Algorithm(g, open_set, closed_set, cost, father, sc)
    # TODO: Implement A* algorithm using open_set, closed_set, and father
    """ raise NotImplementedError('Not implemented') """

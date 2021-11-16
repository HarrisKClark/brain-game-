import math
import pygame

pygame.init()

FPS = 60

WIDTH = 1200
HEIGHT = 800
SIZE = 15

font = pygame.font.Font('freesansbold.ttf', 17)
font2 = pygame.font.Font('freesansbold.ttf', 32)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class UserInterface:
    def __init__(self):
        self.x = WIDTH-200
        self.color1 = (150, 150, 150)
        self.color2 = (100, 100, 100)

        self.SensoryX, self.SensoryY = WIDTH - 185, 30
        self.BrainX, self.BrainY = WIDTH - 185, 65
        self.MotorX, self.MotorY = WIDTH - 185, 100

        #brain buttons
        self.InvertX, self.InvertY = WIDTH - 185, 170
        self.MaxX, self.MaxY = WIDTH - 185, 205

        self.sensory = False
        self.brain = False
        self.motor = False

        #brain
        self.invert = False
        self.max = False

    # draws all the buttons and stuff
    def draw(self):
        pygame.draw.rect(WIN, self.color1, (self.x, 0, 300, HEIGHT))

        pygame.draw.rect(WIN, self.color2, (self.SensoryX - 5, self.SensoryY-5, 90, 30))
        pygame.draw.rect(WIN, self.color2, (self.BrainX - 5, self.BrainY - 5, 90, 30))
        pygame.draw.rect(WIN, self.color2, (self.MotorX - 5, self.MotorY - 5, 90, 30))

        button_sensory = font.render("Sensory", True, (0, 0, 0))
        button_brain = font.render("Brain", True, (0, 0, 0))
        button_copy = font.render("Motor", True, (0, 0, 0))

        WIN.blit(button_sensory, (self.SensoryX, self.SensoryY))
        WIN.blit(button_brain, (self.BrainX, self.BrainY))
        WIN.blit(button_copy, (self.MotorX, self.MotorY))

        #brain button
        if self.brain:
            '''invert'''
            pygame.draw.rect(WIN, self.color2, (self.InvertX - 5, self.InvertY - 5, 90, 30))
            button_invert = font.render("Invert", True, (0, 0, 0))
            WIN.blit(button_invert, (self.InvertX, self.InvertY))

            '''max'''
            pygame.draw.rect(WIN, self.color2, (self.MaxX - 5, self.MaxY - 5, 90, 30))
            button_invert = font.render("Max", True, (0, 0, 0))
            WIN.blit(button_invert, (self.MaxX, self.MaxY))

    def button_press(self, x, y):
        if valid_press(x, y, self.SensoryX, self.SensoryY):
                if self.sensory:
                    self.sensory = False
                else:
                    self.sensory = True
                    self.brain = False
                    self.motor = False

        if valid_press(x, y, self.BrainX, self.BrainY):
            if self.brain:
                self.brain = False
            else:
                self.sensory = False
                self.brain = True
                self.motor = False

        if valid_press(x, y, self.MotorX, self.MotorY):
                if self.motor:
                    self.motor = False
                else:
                    self.sensory = False
                    self.brain = False
                    self.motor = True

        #brain buttons
        if valid_press(x, y, self.InvertX, self.InvertY):
                self.invert = not self.invert

        if valid_press(x, y, self.MaxX, self.MaxY):
                self.max = not self.max

def valid_press(x, y, x2, y2):
    if(x > x2-5) and (x < x2 + 85):
        if(y > y2-5) and (y < y2+25):
            return True
    return False


class Node():
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.color = (200,200,200)


class SensoryNode(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (50, 50, 150)
        self.data = 0

    def sense(self, x, y):
        num = math.hypot(self.x-x, self.y-y)
        if num < 100:
            num = 100 - num
            self.color = (50, 50, 150+num)
            self.data = num
            return num
        else:
            self.color = (50, 50, 150)
            self.data =0
            return 0


class BrainNode(Node):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.color = (150,150,150)
        self.data = []

    def calculate(self):
        max = 0
        for x in self.data:
            if x > max:
                max = x
        self.data = [max]

class AntiNode(BrainNode):
    def __init__ (self, x, y):
        super().__init__(x,y)
        self.color = (150,150,150)

    def calculate(self, *inputs):
        reverse = []
        for input in inputs:
            reverse.append(-input)
        self.data = [reverse[0]]


class MotorNode(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (150, 50, 50)
        self.data = 0

    def move(self, x, y):
        if self.data > 0:
            print("forward")
        elif self.data < 0:
            print("backward")
        else:
            print("stay still")


class Edge():
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2


def find_path(graph, start, finish):
    paths = graph.get(start)

    for path in paths:
        if path == finish:
            return path

    newPaths = []

    for path in paths:
        tempPath = graph.get(path)
        for path2 in tempPath:
            newPaths.append(path2)

    find_path(newPaths, start, finish)


def draw_node(node, px, py):
    if math.hypot(node.x - px,node.y - py) < SIZE:
        pygame.draw.circle(WIN, (0, 0, 0), (node.x, node.y), SIZE+2)
        pygame.draw.circle(WIN, node.color, (node.x, node.y), SIZE)
    else:
        pygame.draw.circle(WIN, node.color, (node.x, node.y), SIZE)


def draw_edge(x1, y1, x2, y2):
    pygame.draw.line(WIN, (255, 255, 255),(x1, y1), (x2, y2),3)


def add_graph(graph,node, edge):
    if(node == None):
        graph.get(edge.node1).append(edge.node2)
        graph.get(edge.node2).append(edge.node1)

    if(edge == None):
        graph[node] = []

    return graph


def valid_position(nodes,x,y):
    if x < WIDTH - (200 + SIZE) and x > SIZE and y > SIZE and y < (HEIGHT + SIZE):
        for node in nodes:
            if math.hypot(node.x-x, node.y-y) < SIZE*2:
                return False
        return True
    return False


def main():
    clock = pygame.time.Clock()
    nodes = []
    edges = []
    addnode = []
    SensoryNodes = []
    BrainNodes = []
    MotorNodes = []

    graph = {}
    ui = UserInterface()

    run = True
    while run:
        x, y = pygame.mouse.get_pos()
        clock.tick(FPS)
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # checks for right and left input
            if event.type == pygame.MOUSEBUTTONDOWN and pressed[pygame.K_SPACE]:
                for node in nodes:

                    if math.hypot(node.x - x,node.y - y) < SIZE:
                        if len(addnode) == 0:
                            addnode.append(node)

                        else:
                            addnode.append(node)

                            if addnode[0] != addnode[1]:
                                addnode.append(node)
                                edge = Edge(addnode[0], addnode[1])
                                edges.append(edge)
                                graph = add_graph(graph, None, edge)

                            addnode.clear()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                ui.button_press(x,y)

                if event.button == 1:
                    if valid_position(nodes,x,y):
                        if ui.sensory:
                            node = SensoryNode(x, y)
                            SensoryNodes.append(node)
                        elif ui.brain:
                            node = BrainNode(x, y)
                            BrainNodes.append(node)
                        elif ui.motor:
                            node = MotorNode(x, y)
                            MotorNodes.append(node)
                        else:
                            node = Node(x,y)

                        nodes.append(node)
                        graph = add_graph(graph, node, None)

                elif event.button == 3:
                    print("poop")
                    temp_nodes = nodes.copy()
                    temp_edges = edges.copy()

                    for node in temp_nodes:
                        if math.hypot(node.x - x,node.y - y) < SIZE:
                            for edge in temp_edges:
                                if edge.node1 == node or edge.node2 == node:
                                    temp_edges.remove(edge)

                            temp_nodes.remove(node)

                            try:
                                if addnode[0] == node:
                                    addnode.clear()
                            except IndexError:
                                pass

                    nodes = temp_nodes.copy()
                    edges = temp_edges
                    temp_edges.clear()
                    temp_nodes.clear()

            if pressed[pygame.K_RIGHT]:
                print(find_path(graph, nodes[0], nodes[3]))
                print(nodes)

        WIN.fill((50, 50, 50))

        for node in SensoryNodes:
            node.sense(x,y)

        for node in graph:
            if node in SensoryNodes:
                tempNodes = graph.get(node)
                for node2 in tempNodes:
                    if node2 in BrainNodes:
                        node2.data.append(node.data)

        for node in BrainNodes:
            node.calculate()

        for node in graph:
            if node in (BrainNodes or SensoryNodes):
                tempNodes = graph.get(node)
                for node2 in tempNodes:
                    if node2 in MotorNodes:
                        if node in BrainNodes:
                            node2.data = node.data[0]
                        else:
                            node2.data = node.data

        for node in MotorNodes:
            node.move(x,y)

        for node in BrainNodes:
            node.data = []

        for node in SensoryNodes:
            node.data = 0

        for node in MotorNodes:
            node.data = 0


        for edge in edges:
            draw_edge(edge.node1.x, edge.node1.y, edge.node2.x, edge.node2.y)

        for node in nodes:
            draw_node(node,x,y)

        ui.draw()

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()

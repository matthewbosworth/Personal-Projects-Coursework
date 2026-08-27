import matplotlib.pyplot as plt
import math 
import sys
import numpy as np
import time
import matplotlib.animation as animation

from utils import *
from grid import *

# file parsing

def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                pt = pt.strip()
                if not pt:
                    continue
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons

# geometric functions

def point_on_segment(p, a, b):
    # true if point p lies exactly on line segment ab
    cross = (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x)
    if cross != 0:
        return False
    return (min(a.x, b.x) <= p.x <= max(a.x, b.x) and 
            min(a.y, b.y) <= p.y <= max(a.y, b.y))

def point_on_polygon_boundary(p, polygon):
    n = len(polygon)
    for i in range(n):
        if point_on_segment(p, polygon[i], polygon[(i+1)%n]):
            return True
    return False

def point_strictly_inside_polygon(p, polygon):
    # Ray-casting: True if p is strictly inside (not on the boundary of) the polygon
    n = len(polygon)
    inside = False
    x, y = p.x, p.y
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i].x, polygon[i].y
        xj, yj = polygon[j].x, polygon[j].y
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def point_in_or_on_polygon(p, polygon):
    return point_strictly_inside_polygon(p, polygon) or point_on_polygon_boundary(p, polygon)

def segments_properly_cross(p1, p2, p3, p4):
    # True if line segments p1p2 and p3p4 properly intersect
    def cross2d(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    d1 = cross2d(p3, p4, p1)
    d2 = cross2d(p3, p4, p2)
    d3 = cross2d(p1, p2, p3)
    d4 = cross2d(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
        ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False

def is_blocked_by_enclosure(p, epolygons):
    # a point is blocked if it is inside or on the boundary of any enclosure
    for polygon in epolygons:
        if point_in_or_on_polygon(p, polygon):
            return True
    return False

def move_crosses_enclosure(p, np_, epolygons):
    # true if the unit step p ->np_ crosses the boundary of any enclosure
    for polygon in epolygons:
        n = len(polygon)
        for i in range(n):
            if segments_properly_cross(p, np_, polygon[i], polygon[(i+1)%n]):
                return True
    return False

def action_cost(next_p, tpolygons):
    # cost to enter next_p is 1.5 if next_p is inside or on the boundary of any turf, else 1
    for polygon in tpolygons:
        if point_in_or_on_polygon(next_p, polygon):
            return 1.5
    return 1.0

# successor generation

# Order: up, right, down, left
DIRECTIONS = [(0,1), (1,0), (0,-1), (-1,0)]

def get_successors(p, epolygons, tpolygons):
    # return list of (next_point, step_cost) in order: up, right, down, left
    result = []
    for dx, dy in DIRECTIONS:
        nx, ny = p.x + dx, p.y + dy
        if 0 <= nx < MAX and 0 <= ny < MAX:
            np_ = Point(nx, ny)
            if not is_blocked_by_enclosure(np_, epolygons) and not move_crosses_enclosure(p, np_, epolygons):
                result.append((np_, action_cost(np_, tpolygons)))
    return result

# heuristic function

def sld(p, dest):
    # straight line distance heuristic
    return math.sqrt((p.x - dest.x)**2 + (p.y - dest.y)**2)

#
# search algorithms
#

def bfs(source, dest, epolygons, tpolygons):
    # Breadth-First Search algorithm - past cost = number of actions
    frontier = Queue()
    frontier.push((source, [source]))  
    explored = set()
    nodes_expanded = 0

    while not frontier.isEmpty():
        node, path = frontier.pop()
        state = (node.x, node.y)

        if state in explored:
            continue
        explored.add(state)
        nodes_expanded += 1

        if node == dest:
            return path, nodes_expanded

        for np_, _ in get_successors(node, epolygons, tpolygons):
            if (np_.x, np_.y) not in explored:
                frontier.push((np_, path + [np_]))
    return None, nodes_expanded

def dfs(source, dest, epolygons, tpolygons):
    # Depth-First Search algorithm - past cost = number of actions
    frontier = Stack()
    frontier.push((source, [source]))  
    explored = set()
    nodes_expanded = 0

    while not frontier.isEmpty():
        node, path = frontier.pop()
        state = (node.x, node.y)

        if state in explored:
            continue
        explored.add(state)
        nodes_expanded += 1

        if node == dest:
            return path, nodes_expanded

        for np_, _ in get_successors(node, epolygons, tpolygons):
            if (np_.x, np_.y) not in explored:
                frontier.push((np_, path + [np_]))
    return None, nodes_expanded

def gbfs(source, dest, epolygons, tpolygons):
    # Greedy Best-First Search algorithm (heuristic = straight line distance to dest)
    frontier = PriorityQueue()
    frontier.push((source, [source]), sld(source, dest))  
    explored = set()
    nodes_expanded = 0

    while not frontier.isEmpty():
        node, path = frontier.pop()
        state = (node.x, node.y)

        if state in explored:
            continue
        explored.add(state)
        nodes_expanded += 1

        if node == dest:
            return path, nodes_expanded

        for np_, _ in get_successors(node, epolygons, tpolygons):
            if (np_.x, np_.y) not in explored:
                frontier.push((np_, path + [np_]), sld(np_, dest))
    return None, nodes_expanded

def astar(source, dest, epolygons, tpolygons):
    # A* Search algorithm (heuristic = straight line distance to dest, costs use turf weights)
    frontier = PriorityQueue()
    frontier.push((source, [source], 0.0), sld(source, dest))  
    explored = set()
    nodes_expanded = 0

    while not frontier.isEmpty():
        node, path, g = frontier.pop()
        state = (node.x, node.y)

        if state in explored:
            continue
        explored.add(state)
        nodes_expanded += 1

        if node == dest:
            return path, nodes_expanded, g

        for np_, step_cost in get_successors(node, epolygons, tpolygons):
            if (np_.x, np_.y) not in explored:
                new_g = g + step_cost
                frontier.push((np_, path + [np_], new_g), new_g + sld(np_, dest))
    return None, nodes_expanded, float('inf')

# path cost helper

def path_cost(path, tpolygons):
    # weighted path cost (GBFS)
    return sum(action_cost(path[i], tpolygons) for i in range(1, len(path))) 

# draw helpers

def draw_world(ax, epolygons, tpolygons, source, dest):
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  
    draw_dest(ax, dest.x, dest.y)

    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
        for i in range(len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])
        
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
        for i in range(len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])

def draw_path_on_ax(ax, path):
    for i in range(len(path)-1):
        draw_result_line(ax, [path[i].x, path[i+1].x], [path[i].y, path[i+1].y])

# 
# main
# 

if __name__ == "__main__":
    epolygons = gen_polygons('TestingGrid/world1_enclosures.txt')
    tpolygons = gen_polygons('TestingGrid/world1_turfs.txt')

    source = Point(8,10)
    dest = Point(43,45)

    print("Running BFS...")
    bfs_path, bfs_exp = bfs(source, dest, epolygons, tpolygons)
    bfs_cost = len(bfs_path) - 1 if bfs_path else 0

    print("Running DFS...")
    dfs_path, dfs_exp = dfs(source, dest, epolygons, tpolygons)
    dfs_cost = len(dfs_path) - 1 if dfs_path else 0

    print("Running GBFS...")
    gbfs_path, gbfs_exp = gbfs(source, dest, epolygons, tpolygons)
    gbfs_cost = path_cost(gbfs_path, tpolygons) if gbfs_path else 0

    print("Running A*...")
    astar_path, astar_exp, astar_cost = astar(source, dest, epolygons, tpolygons)

    # print summary
    print("\n * Summary (source=(8,10), dest=(43,45)) *")
    print(f"BFS   : path cost = {bfs_cost}, nodes expanded = {bfs_exp}")
    print(f"DFS   : path cost = {dfs_cost}, nodes expanded = {dfs_exp}")
    print(f"GBFS  : path cost = {gbfs_cost:.1f}, nodes expanded = {gbfs_exp}")
    print(f"A*    : path cost = {astar_cost:.1f}, nodes expanded = {astar_exp}")

    # write summary.txt
    with open("summary.txt", "w") as f:
        f.write("bfs1:\n")
        f.write(f"Path cost: {bfs_cost}\n")
        f.write(f"Nodes expanded: {bfs_exp}\n\n")
        f.write("dfs1:\n")
        f.write(f"Path cost: {dfs_cost}\n")
        f.write(f"Nodes expanded: {dfs_exp}\n\n")
        f.write("gbfs1:\n")
        f.write(f"Path cost: {gbfs_cost:.1f}\n")
        f.write(f"Nodes expanded: {gbfs_exp}\n\n")
        f.write("astar1:\n")
        f.write(f"Path cost: {astar_cost:.1f}\n")
        f.write(f"Nodes expanded: {astar_exp}\n")

    # plot all four results
    results = [
        ("BFS", bfs_path, bfs_cost, bfs_exp),
        ("DFS", dfs_path, dfs_cost, dfs_exp), 
        ("GBFS", gbfs_path, gbfs_cost, gbfs_exp), 
        ("A*", astar_path, astar_cost, astar_exp)]

    for label, rpath, rcost, rexp in results:
        fig, ax = draw_board()
        draw_world(ax, epolygons, tpolygons, source, dest)
        if rpath:
            draw_path_on_ax(ax, rpath)
        ax.set_title(f"{label} | cost={rcost} | nodes={rexp})", fontsize=12)
        filename = label.replace("*", "star").lower()
        plt.savefig(f"TestingGrid/{filename}_result.png", dpi=120)
        plt.close()

    # world 2 custom test case
    epolygons2 = gen_polygons('TestingGrid/world2_enclosures.txt')
    tpolygons2 = gen_polygons('TestingGrid/world2_turfs.txt')

    source2 = Point(2,12)
    dest2 = Point(45,45)

    results2 = [
        ("BFS", bfs(source2, dest2, epolygons2, tpolygons2)), 
        ("DFS", dfs(source2, dest2, epolygons2, tpolygons2)), 
        ("GBFS", gbfs(source2, dest2, epolygons2, tpolygons2)), 
        ("A*", astar(source2, dest2, epolygons2, tpolygons2))]

    for label, result in results2:
        path = result[0]
        fig, ax = draw_board()
        draw_world(ax, epolygons2, tpolygons2, source2, dest2)
        if path:
            draw_path_on_ax(ax, path)
        ax.set_title(f"World2 {label}", fontsize=12)
        filename = label.replace("*", "star").lower()
        plt.savefig(f"TestingGrid/world2_{filename}_result.png", dpi=120)
        plt.close()
    


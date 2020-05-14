from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue, Stack

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []
traversal_graph = {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}

# Give dead ends a place to go
good_rooms = Stack()

reverse_dir = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

def get_paths(room_id):
    paths = []
    for direction, room in traversal_graph[room_id].items():
        if room == '?':
            paths.append(direction)

    return paths

def isSurrounded():
    surrounded = True
    for i in traversal_graph.values():
        if '?' in i.values():
            surrounded = False
    return surrounded

def dfs(starting_room, destination_room):
    stack = Stack()
    visited = set()
    stack.push([starting_room])

    while stack.size() > 0:
        path = stack.pop()
        room = path[-1]
        if room not in visited:
            if room == destination_room:
                break
            visited.add(room)
            for next_room in list(traversal_graph[room].values()):
                if next_room != '?':
                    n_path = list(path)
                    n_path.append(next_room)
                    stack.push(n_path)

    dirs = []
    for i in range(len(path) - 1):
        for direction, room in traversal_graph[path[i]].items():
            if room == path[i+1]:
                dirs.append(direction)
    return dirs

def bfs(starting_room, destination_room):
    queue = Queue()
    visited = set()
    queue.enqueue([starting_room])
    while queue.size() > 0:
        path = queue.dequeue()
        room = path[-1]
        if room not in visited:
            if room == destination_room:
                break
            visited.add(room)
            for next_room in list(traversal_graph[room].values()):
                if next_room != '?':
                    n_path = list(path)
                    n_path.append(next_room)
                    queue.enqueue(n_path)

    # Assign directions based on path
    dirs = []
    for i in range(len(path) - 1):
        for direction, room in traversal_graph[path[i]].items():
            if room == path[i+1]:
                dirs.append(direction)
    return dirs

while isSurrounded() == False:
    current_room = player.current_room.id

    # Add to good_rooms
    if len(get_paths(current_room)) > 1:
        good_rooms.push(current_room)

    # Check available paths, find shortest path to good_room
    a_paths = get_paths(current_room)
    if not a_paths:
        found_room = False
        while found_room == False:
            new_room = good_rooms.pop()
            if len(get_paths(new_room)) > 0:
                found_room = True
        retrace = bfs(current_room, new_room)

        for move in retrace:
            player.travel(move)

        traversal_path += retrace

        current_room = player.current_room.id

        a_paths = get_paths(current_room)

        if len(get_paths(current_room)) > 1:
            good_rooms.push(current_room)

    exits = {}
    cdirs = ['n', 's', 'e', 'w']
    for i in cdirs:
        if i in a_paths:
            tdir = i
            player.travel(tdir)
            exits[tdir] = len(player.current_room.get_exits())
            player.travel(reverse_dir[tdir])

    if len(exits) > 1 and 1 in exits.values():
        mdir = ''
        mexits = 10
        for direction, exit in exits.items():
            if exit < mexits:
                mdir = direction
                mexits = exit
        direction = mdir
    else:
        for i in cdirs:
            if i in a_paths:
                direction = i

    player.travel(direction)

    traversal_path.append(direction)

    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = {i : '?' for i in player.current_room.get_exits()}

    traversal_graph[current_room][direction] = player.current_room.id
    traversal_graph[player.current_room.id][reverse_dir[direction]] = current_room


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

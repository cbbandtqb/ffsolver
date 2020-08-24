import numpy as np
import json
import pprint
import os
import sys

def load_room(room_no):
    with open('.'+os.sep+'room'+os.sep+'room{}.json'.format(room_no)) as f:
        room = np.array(json.load(f))
    return room

def paint(room, p, c):
    painted = np.copy(room)
    x, y = p
    painted[y][x] = c
    l = [p]
    while (len(l)):
        x, y = l.pop()
        if painted[y+1][x] == 0:
            painted[y+1][x] = c
            l.append((x, y+1))
        if painted[y][x-1] == 0:
            painted[y][x-1] = c
            l.append((x-1, y))
        if painted[y-1][x] == 0:
            painted[y-1][x] = c
            l.append((x, y-1))
        if painted[y][x+1] == 0:
            painted[y][x+1] = c
            l.append((x+1, y))
    return painted

def was_solved(room):
    return np.count_nonzero(room == 6) == 0

def is_movable(reachable, p):
    x, y = p
    if reachable[y][x] == 2:
        if (reachable[y][x-1] == 7 or reachable[y-1][x] == 7 or reachable[y][x+1] == 7) and (reachable[y+1][x] in [0, 7]):
            return True
    elif reachable[y][x] == 3:
        if (reachable[y-1][x] == 7 or reachable[y][x+1] == 7 or reachable[y+1][x] == 7) and (reachable[y][x-1] in [0, 7]):
            return True
    elif reachable[y][x] == 4:
        if (reachable[y+1][x] == 7 or reachable[y][x-1] == 7 or reachable[y-1][x] == 7) and (reachable[y][x+1] in [0, 7]):
            return True
    elif reachable[y][x] == 5:
        if (reachable[y][x+1] == 7 or reachable[y+1][x] == 7 or reachable[y][x-1] == 7) and (reachable[y-1][x] in [0, 7]):
            return True
    return False

def is_destructible(reachable, p):
    x, y = p
    if reachable[y][x] == 2:
        if reachable[y-1][x] == 7 and (reachable[y+1][x] in [1, 2, 3, 4, 6]):
            return True
    elif reachable[y][x] == 3:
        if reachable[y][x+1] == 7 and (reachable[y][x-1] in [1, 2, 3, 5, 6]):
            return True
    elif reachable[y][x] == 4:
        if reachable[y][x-1] == 7 and (reachable[y][x+1] in [1, 2, 4, 5, 6]):
            return True
    elif reachable[y][x] == 5:
        if reachable[y+1][x] == 7 and (reachable[y-1][x] in [1, 3, 4, 5, 6]):
            return True
    return False

def is_gettable(reachable, p):
    x, y = p
    if reachable[y][x] == 6:
        if reachable[y+1][x] == 7 or reachable[y][x-1] == 7 or reachable[y-1][x] == 7 or reachable[y][x+1] == 7:
            return True
    return False
  
def move_block(room, o, p):
    redesign = np.copy(room)
    x, y = o
    redesign[y][x] = 0
    x, y = p
    if redesign[y][x] == 2:
        while (redesign[y+1][x] == 0):
            y += 1
        redesign[y][x] = 2
        if redesign[y+1][x] == 5:
            redesign[y][x] = 1
            redesign[y+1][x] = 1
    elif redesign[y][x] == 3:
        while (redesign[y][x-1] == 0):
            x -= 1
        redesign[y][x] = 3
        if redesign[y][x-1] == 4:
            redesign[y][x] = 1
            redesign[y][x-1] = 1
    elif redesign[y][x] == 4:
        while (redesign[y][x+1] == 0):
            x += 1
        redesign[y][x] = 4
        if redesign[y][x+1] == 3:
            redesign[y][x] = 1
            redesign[y][x+1] = 1
    else:
        while (redesign[y-1][x] == 0):
            y -= 1
        redesign[y][x] = 5
        if redesign[y-1][x] == 2:
            redesign[y][x] = 1
            redesign[y-1][x] = 1
    x, y = p
    redesign[y][x] = 7
    return redesign

def destroy_block(room, o, p):
    redesign = np.copy(room)
    x, y = o
    redesign[y][x] = 0
    x, y = p
    redesign[y][x] = 7
    return redesign

def get_fruits(room, o, p):
    redesign = np.copy(room)
    x, y = o
    redesign[y][x] = 0
    x, y = p
    redesign[y][x] = 7
    return redesign

def generate_candidate_list(room):
    for py in range(1, 11):
        for px in range(1, 17):
            if room[py][px] == 7:
                break
        else:
            continue
        break
    reachable = paint(room, (px, py), 7)
    movable_list = []
    destructible_list = []
    gettable_list = []
    for y in range(1, 11):
        for x in range(1, 17):
            if is_movable(reachable, (x, y)):
                movable_list.append((x, y))
            elif is_destructible(reachable, (x, y)):
                destructible_list.append((x, y))
            elif is_gettable(reachable, (x, y)):
                gettable_list.append((x, y))
    candidate_list = []
    for p in movable_list:
        candidate_list.append(move_block(room, (px, py), p))
    for p in destructible_list:
        candidate_list.append(destroy_block(room, (px, py), p))
    for p in gettable_list:
        candidate_list.append(get_fruits(room, (px, py), p))
    return candidate_list        

def wallize(room):
    redesign = np.copy(room)
    for y in range(1, 11):
        for x in range(1, 17):
            if redesign[y][x] == 2 and redesign[y+1][x] == 5:
                redesign[y][x] = 1
                redesign[y+1][x] = 1
                continue
            if redesign[y][x] == 4 and redesign[y][x+1] == 3:
                redesign[y][x] = 1
                redesign[y][x+1] = 1
    return redesign

def solve(room, depth):
    global solution
    global room_count, MAX_ROOM_COUNT
    if room_count == MAX_ROOM_COUNT:
        return False
#    print('depth = {}'.format(depth))
#    pprint.pprint(room)
#    sys.stdout.flush()
    room_count += 1
    if was_solved(room):
        solution.append(room.tolist())
        return True
    candidate_list = generate_candidate_list(room)
    if len(candidate_list) == 0:
        return False
    for candidate in candidate_list:
        if solve(candidate, depth+1):
            solution.append(room.tolist())
            return True
    return False

def main():
    global solution
    global room_count, MAX_ROOM_COUNT
    solution = []
    room_count = 0
    MAX_ROOM_COUNT = int(sys.argv[2])
    solve(wallize(load_room(int(sys.argv[1]))), 0)
    solution.reverse()
    result = {'room_count': room_count, 'solution': solution}
    pprint.pprint(result)

if __name__ == '__main__':
    main()
class cell:
    def __init__(self, x, y, dist): 
        self.x = x 
        self.y = y 
        self.dist = dist


def is_inside(x, y, n):
    """ function to check if a position is inside the NxN grid specified.
    """ 
    if (x >= 1 and x <= n and y >= 1 and y <= n):
        return True
    return False


def shortest_steps(n, a, b, knight_pos = [0,0]):
    """ function to calculate how many moves are in the shortest path."""
    # the  position the knight can move to is:
    # (x + a, y - b)
    # (x + a, y + b)
    # (x - a, y - b)
    # (x - a, y + b)
    # (x + b, y - a)
    # (x + b, y + a)
    # (x - b, y - a)
    # (x - b, y + a)

    # storing them into array form:
    dx = [a, a, -a, -a, b, b, -b, -b]
    dy = [-b, b, -b, b, -a, a, -a, a]

    queue = []

    # starting position:
    queue.append(cell(knight_pos[0], knight_pos[1], 0))
    visited = [[False for i in range(n + 1)] for j in range(n + 1)]

    # target position: (n-1, n-1)
    target_pos =  [n-1, n-1]

    # initiate moving state
    visited[knight_pos[0]][knight_pos[1]] = True

    # run till one element is added to queue
    while (len(queue) > 0):
        t = queue[0]
        queue.pop(0)

        # if knight has reached target
        if (t.x == target_pos[0] and t.y == target_pos[1]):
            return t.dist

        # move!
        for i in range(0, len(dx)):
            x = t.x + dx[i]
            y = t.y + dy[i]

            # if new pos is still within the boundary AND it hasn't been visited, push it to queue, and add distance 1 to parent; otherwise, keep looing
            if (is_inside(x, y, n) and not visited[x][y]):
                visited[x][y] = True
                queue.append(cell(x, y, t.dist + 1))
    
    # return something if path is not possible
    return "invalid"


def all_shortest_paths(n):
    success_paths = []
    invalid_paths = []
    sum_invalid = 0
    sum_steps = 0
    for b in range(1, n):
        for a in range(1, b+1):
            if shortest_steps(n=n, a=a, b=b) == "invalid":
                invalid_paths.append((a,b))
                sum_invalid += 1
            else:
                # if shortest_steps(n=n, a=a, b=b) is int:
                shortest_steps = shortest_steps(n=n, a=a, b=b)
                sum_steps += shortest_steps
                success_paths.append((a, b, shortest_steps))
    # print(success_paths)
    # print(invalid_paths)
    return sum_steps, sum_invalid


# Q1:
n5_a1_b2 = shortest_steps(n=5, a=1, b=2)
print("Q1. For n=5, how many moves are in the shortest path for knight(1,2)? {}".format(n5_a1_b2))

# Q2:
n5_sum_steps, n5_invalid = all_shortest_paths(5)
print("Q2. For n=5, what is the sum of the number of moves for the shortest paths for all knights with a<=b?: {}".format(n5_sum_steps))

# Q3:
n25_sum_steps, n25_invalid = all_shortest_paths(25)
print("Q3. For n=25, how many knights with 0<a<=b cannot reach (24,24)?: {}".format(n25_invalid))

# Q4:
n1000_a13_b23 = shortest_steps(n=1000, a=13, b=23)
print("Q4. For n=1000, how many moves are in the shortest path for knight(13,23)?: {}".format(n1000_a13_b23))

# Q5:
n5_sum_steps, n5_sum_invalid = all_shortest_paths(5)
print("Q5. For n=5, how many knights with 0<a<=b cannot reach (4,4)?: {}".format(n5_sum_invalid))

# Q6:
n25_a4_b7 = shortest_steps(n=1000, a=13, b=23)
print("Q6. For n=25, how many moves are in the shortest path for knight(4,7)?: {}".format(n25_a4_b7))

# Q7:
print("Q7. For n=25, what is the sum of the number of moves for the shortest paths for all knights with a<=b?: {}".format(n25_a4_b7))
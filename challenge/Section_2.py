class cell:
    def __init__(self, x, y, step): 
        self.x = x 
        self.y = y 
        self.step = step
    
    def is_inside(self, n):
        if (self.x >= 0 and self.x < n and self.y >= 0 and self.y < n):
            return True
        return False


class path_results:
    def __init__(self, n, invalid_paths, success_paths):
        self.n = n
        self.invalid_paths = invalid_paths
        self.success_paths = success_paths
    
    @property
    def invalid_total(self):
        return len(self.invalid_paths)
    
    @property
    def sum_success_steps(self):
        steps = [sp[2] for sp in self.success_paths]
        print(steps)
        return sum(steps)

# def is_inside(x, y, n):
#     """ function to check if a position is inside the NxN grid specified.
#     Args:
#     x (int): position on horizontal axis
#     y (int): position on vertical axis
#     n (int): size of board
#     """ 
#     if (x >= 0 and x < n and y >= 0 and y < n):
#         return True
#     return False


def shortest_steps(n, a, b):
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

    # starting and target positions:
    start_pos = [0,0]
    target_pos = [n - 1, n - 1]
    
    start_cell = cell(start_pos[0], start_pos[1], 0)
    queue.append(start_cell)

    # marking all board as unvisited, except the start position
    visited = [[False for i in range(n + 1)] for j in range(n + 1)]
    visited[start_pos[0]][start_pos[1]] = True

    # run till one element is added to queue
    while (len(queue) > 0):
        cur_pos = queue[0]  # initiate first move
        queue.pop(0)

        # if knight has reached target
        if (cur_pos.x == target_pos[0] and cur_pos.y == target_pos[1]):
            return cur_pos.step

        # move
        for i in range(0, len(dx)):
            x = cur_pos.x + dx[i]
            y = cur_pos.y + dy[i]
            new_pos = cell(x, y, cur_pos.step + 1)
            
            # if new pos is still within the boundary AND it hasn't been visited, push it to queue,  
            # and add step 1; otherwise, keep looing
            if (new_pos.is_inside(n) and not visited[x][y]):
                visited[x][y] = True
                queue.append(new_pos)
    
    # if after all tries queue is still empty, ie no valid paths found:
    return "invalid"


def combo_test(n):
    invalid_paths = []
    success_paths = []
    for b in range(1, n):
        for a in range(1, b + 1):
            ss_test = shortest_steps(n=n, a=a, b=b)
            if ss_test == "invalid":
                invalid_paths.append((a,b))
            else:
                success_paths.append((a, b, ss_test))

    return path_results(n, invalid_paths, success_paths)

if __name__ == '__main__':
    # Q1:
    n5_a1_b2 = shortest_steps(n=5, a=1, b=2)
    print("Q1. For n=5, how many moves are in the shortest path for knight(1,2)? {}".format(n5_a1_b2))

    # Q2:
    n5_combo = combo_test(5)
    q2_ans = n5_combo.invalid_total
    print("Q2. For n=5, how many knights with 0<a<=b cannot reach (4,4)?: {}".format(q2_ans))

    # Q3:
    q3_ans = n5_combo.sum_success_steps
    print("Q3. For n=5, what is the sum of the number of moves for the shortest paths for all knights with a<=b?: {}".format(q3_ans))

    # Q4:
    n25_a4_b7 = shortest_steps(n=25, a=4, b=7)
    print("Q4. For n=25, how many moves are in the shortest path for knight(4,7)?: {}".format(n25_a4_b7))

    # Q5:
    n25_combo = combo_test(25)
    q5_ans = n25_combo.invalid_total
    print("Q5. For n=25, how many knights with 0<a<=b cannot reach (24,24)?: {}".format(q5_ans))

    # Q6:
    q6_ans = n25_combo.sum_success_steps
    print("Q6. For n=25, what is the sum of the number of moves for the shortest paths for all knights with a<=b?: {}".format(q6_ans))

    # Q7:
    n1000_a13_b23 = shortest_steps(n=1000, a=13, b=23)
    print("Q7. For n=1000, how many moves are in the shortest path for knight(13,23)?: {}".format(n1000_a13_b23))

    # Q8:
    n1000_a73_b101 = shortest_steps(n=1000, a=73, b=101)
    print("Q8. For n=10000, how many moves are in the shortest path for knight(73,101)?: {}".format(n25_a4_b7))
import sys

# Print debug messages
DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def clamp(num):
    return max(min(num, 1), -1)


class Grid:
    def __init__(self):
        self.position_head = [0, 0]
        self.position_tail = [0, 0]
        self.visited_by_tail = set()
        self.save_tail_position()

    def move(self, direction):
        # Move the head
        if direction == 'U':
            self.position_head[1] += 1
        elif direction == 'D':
            self.position_head[1] -= 1
        elif direction == 'L':
            self.position_head[0] -= 1
        elif direction == 'R':
            self.position_head[0] += 1
        else:
            raise Exception('Invalid direction <' + str(direction) + '> for method Grid.move()')
        # Move the tail
        self.tail_follow()

    def tail_follow(self):
        diff_vector = [h - t for h, t in zip(self.position_head, self.position_tail)]
        debug('\tHead is ' + str(self.position_head))
        debug('\tTail is ' + str(self.position_tail))
        debug('\tTail follow vector is ' + str(diff_vector))

        # Tail only moves if there is a gap between it and the head
        if max([abs(x) for x in diff_vector]) <= 1:
            debug('\t\tTail does not move.')
            return

        # Tail moves maximum 1 field in each direction,
        # but it can move diagonally (in two directions at once)
        # and it is a preferred option.
        follow_vector = [clamp(x) for x in diff_vector]
        debug('\t\tTail move vector: ' + str(follow_vector))
        self.position_tail = [x + diff for x, diff in zip(self.position_tail, follow_vector)]
        debug('\t\tNew position: ' + str(self.position_tail))
        # Save new tail position
        self.save_tail_position()

    def save_tail_position(self):
        old_len = len(self.visited_by_tail)
        self.visited_by_tail.add(tuple(x for x in self.position_tail))
        new_len = len(self.visited_by_tail)
        if old_len == new_len:
            debug('\t' * 3 + 'Position was already visited.')
        else:
            debug('\t' * 3 + 'New tail position.')


def main():
    grid = Grid()
    with open('input_day_09.txt') as input_file:
        for line in input_file:
            line = line.strip()
            # debug(line)
            direction, steps_str = line.split(maxsplit=1)
            steps = int(steps_str)
            debug('Move ' + str(steps) + ' times in direction ' + direction)
            # Move as defined
            for i in range(steps):
                grid.move(direction)
    print('Number of positions visited: ' + str(len(grid.visited_by_tail)))


if __name__ == '__main__':
    main()

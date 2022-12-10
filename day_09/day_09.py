import sys

# Print debug messages
DEBUG = False

# Constants
ROPE_LENGTH = 10


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def clamp(num):
    return max(min(num, 1), -1)


class Grid:
    def __init__(self, rope_len):
        self.positions = [[0, 0] for _ in range(rope_len)]
        self.visited_by_tail = set()
        self.save_tail_position()

    def move(self, direction):
        # Move the head
        head = self.positions[0]
        if direction == 'U':
            head[1] += 1
        elif direction == 'D':
            head[1] -= 1
        elif direction == 'L':
            head[0] -= 1
        elif direction == 'R':
            head[0] += 1
        else:
            raise Exception('Invalid direction <' + str(direction) + '> for method Grid.move()')
        debug('Head position is now: ' + str(self.positions[0]))
        # Move the tail
        self.tail_follow()

    def tail_follow(self, part_idx=1):
        # For each part 'current' the 'previous' part acts as a "head" that it follows
        previous = self.positions[part_idx - 1]
        current = self.positions[part_idx]

        diff_vector = [h - t for h, t in zip(previous, current)]
        if part_idx == 1:
            debug('\tHead is ' + str(self.positions[0]))
        if part_idx == len(self.positions) - 1:
            debug('\tTail is ' + str(self.positions[-1]))
        debug('\tPart follow vector is ' + str(diff_vector))

        # Tail only moves if there is a gap between it and the head
        if max([abs(x) for x in diff_vector]) <= 1:
            if part_idx == len(self.positions) - 1:
                debug('\t\tTail does not move.')
            return

        # Each part moves maximum 1 field in each direction,
        # but it can move diagonally (in two directions at once)
        # and it is a preferred option.
        follow_vector = [clamp(x) for x in diff_vector]
        debug('\t\tPart move vector: ' + str(follow_vector))
        # Cannot save to 'current' as that would create new list and not overwrite the previous
        self.positions[part_idx] = [x + diff for x, diff in zip(current, follow_vector)]
        debug('\t\tNew position: ' + str(self.positions[part_idx]))

        # If last part, break the recursion
        if part_idx + 1 == len(self.positions):
            self.save_tail_position()
            return

        # Move next parts
        self.tail_follow(part_idx + 1)

    def save_tail_position(self):
        old_len = len(self.visited_by_tail)
        self.visited_by_tail.add(tuple(x for x in self.positions[-1]))
        new_len = len(self.visited_by_tail)
        if old_len == new_len:
            debug('\t' * 3 + 'Position was already visited.')
        else:
            debug('\t' * 3 + 'New tail position.')


def main():
    grid = Grid(ROPE_LENGTH)
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

import sys

# Print debug messages
DEBUG = False

PIX_ABOVE = "█"
PIX_UPPER = "▓"
PIX_LEVEL = "▒"
PIX_LOWER = "░"
PIX_BELOW = " "

ARR_UP = '^'
ARR_DOWN = 'v'
ARR_LEFT = '<'
ARR_RIGHT = '>'


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def get_level_pix(level, current):
    if level == current:
        return PIX_LEVEL
    elif level == current - 1:
        return PIX_LOWER
    elif level == current + 1:
        return PIX_UPPER
    elif level < current:
        return PIX_BELOW
    else:
        return PIX_ABOVE


class Field:
    def __init__(self, height):
        self.height = height
        self.up = None
        self.down = None
        self.left = None
        self.right = None

        self.steps = None  # Minimal number of steps required to get to the field from start
        self.prev = None  # Previous field - where the shortest path (minimal steps count) comes from

    def __str__(self):
        go_where = []
        if self.can_go_up():
            go_where.append('up')
        if self.can_go_down():
            go_where.append('down')
        if self.can_go_left():
            go_where.append('left')
        if self.can_go_right():
            go_where.append('right')
        return 'Field height ' + str(self.height) + ' accessible in ' + str(self.steps) + ' steps - can go ' + ', '.join(go_where)

    def can_go_up(self):
        return self.up is not None and self.up.height <= self.height + 1

    def can_go_down(self):
        return self.down is not None and self.down.height <= self.height + 1

    def can_go_left(self):
        return self.left is not None and self.left.height <= self.height + 1

    def can_go_right(self):
        return self.right is not None and self.right.height <= self.height + 1

    def print_line(self, line):
        if line == 0:
            up = ARR_UP if self.can_go_up() else ' '
            return '  ' + up + '  '
        elif line == 1:
            left = ARR_LEFT if self.can_go_left() else ' '
            right = ARR_RIGHT if self.can_go_right() else ' '
            height = str(self.height).rjust(2).ljust(3)
            return left + height + right
        elif line == 2:
            down = ARR_DOWN if self.can_go_down() else ' '
            return '  ' + down + '  '
        else:
            raise Exception('Only lines 0(upper) 1(middle) and 2(bottom) expected.')


def update_field(next, previous):
    if next.steps is not None and next.steps <= previous.steps:
        return False
    next.steps = previous.steps + 1
    next.prev = previous
    return True


def find_path(field_start):
    # From start to end try paths
    field_start.steps = 0
    fields = [field_start]
    cnt = 0
    # global DEBUG
    # DEBUG = False
    while len(fields) != 0:
        cnt += 1
        field = fields.pop(0)
        debug(str(field))
        if field.can_go_up():
            debug('UP')
            if update_field(field.up, field):
                if field.up not in fields:
                    fields.append(field.up)
        if field.can_go_down():
            debug('DOWN')
            if update_field(field.down, field):
                if field.down not in fields:
                    fields.append(field.down)
        if field.can_go_left():
            debug('LEFT')
            if update_field(field.left, field):
                if field.left not in fields:
                    fields.append(field.left)
        if field.can_go_right():
            debug('RIGHT')
            if update_field(field.right, field):
                if field.right not in fields:
                    fields.append(field.right)
        debug('Fields in line: ' + str(len(fields)))
        if len(fields) > 100:
            debug('HARD BREAK')
            break
    # DEBUG = True
    debug('Processed ' + str(cnt) + ' fields')
    # debug('There is ' + str(len(grid) * len(grid[0]) - cnt) + ' inaccessible fields.')


def clear_map(grid):
    for row in grid:
        for field in row:
            field.steps = None
            field.prev = None


def main():
    position_current = None
    position_target = None
    grid = []

    # with open('input_test.txt') as file_input:
    with open('input_day_12.txt') as file_input:
        grid_y = 0
        for line in file_input:
            line = line.strip()
            # debug(line)
            map_line = []
            grid_x = 0
            for char in line:
                height = ord(char) - ord('a')
                if char == 'S':
                    height = 0  # ord('a') - ord('a')
                    position_current = (len(map_line), len(grid))
                if char == 'E':
                    height = ord('z') - ord('a')
                    position_target = (len(map_line), len(grid))
                field = Field(height)

                # Create links between fields
                if grid_y != 0:
                    upper = grid[grid_y - 1][grid_x]
                    field.up = upper
                    upper.down = field
                if grid_x != 0:
                    left = map_line[grid_x - 1]
                    field.left = left
                    left.right = field

                # Add to grid
                map_line.append(field)
                grid_x += 1
            grid.append(map_line)
            grid_y += 1

    # Debug links
    for row in grid:
        line = '|'.join([field.print_line(0) for field in row])
        debug(line)
        line = '|'.join([field.print_line(1) for field in row])
        debug(line)
        line = '|'.join([field.print_line(2) for field in row])
        debug(line)
        line = ' '.join(['-----' for _ in row])
        debug(line)

    debug('FIELDS COUNT: ' + str(len(grid) * len(grid[0])))

    # Part 2 - find path for each field with height 0 as starting point
    shortest_length = None
    for row in grid:
        for field in row:
            if field.height == 0:
                clear_map(grid)  # Clear data saved for previous path
                find_path(field)
                x, y = position_target
                path_lenght = grid[y][x].steps
                if path_lenght is None:
                    debug('There is no path.')
                    continue
                # global DEBUG
                # DEBUG = True
                debug('Found path with ' + str(path_lenght) + ' steps.')
                # DEBUG = False
                if shortest_length is None:
                    shortest_length = path_lenght
                if path_lenght < shortest_length:
                    shortest_length = path_lenght

    print('Shortest path is ' + str(shortest_length) + ' steps long.')


if __name__ == '__main__':
    main()

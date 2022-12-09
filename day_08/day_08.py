import sys

# Print debug messages
DEBUG = True

# Constants
FIELD_INVISIBLE = -1


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def main():
    grid = []
    with open('input_day_08.txt') as file_input:
        for line in file_input:
            line = line.strip()
            # debug(line)
            grid.append([int(x) for x in line])
    debug(grid[-1][-10:])

    # If I test full row and full column for each field
    # then for NxN grid this will take up to 2N*F tests
    # but this would not require any more space for structures

    # Now first of all - all borders are visible
    # then I may be able to progres in circles around the grid
    # and remember the highest points met so far
    # - that would save me from looking at the whole line/column each time
    # but that would also require some more complex structures to save the info

    debug(str(len(grid)))
    debug(str(len(grid[0])))
    debug(str(len(grid) * len(grid[0])))

    # Considering the grid is relatively small
    # I may use any approach and not overthink this

    # So I will just look for all the values in row/column for each field
    # and change the value of invisible fields to -1 while visible will keep their size for following lookups
    for y, row in enumerate(grid[1:-1], 1):
        for x, field in enumerate(row[1:-1], 1):
            left = max(row[:x])
            right = max(row[x+1:])
            column = [r[x] for r in grid]
            up = max(column[:y])
            down = max(column[y+1:])
            if field <= min(left, right, up, down):
                grid[y][x] = FIELD_INVISIBLE
    visible_cnt = 0
    for row in grid:
        debug(''.join([str(x) if x >= 0 else ' ' for x in row]))
        visible_cnt += sum([1 if x >= 0 else 0 for x in row])
    debug(grid[-2][-10:])
    print('Visible trees count: ' + str(visible_cnt))


if __name__ == '__main__':
    main()

import sys

# Print debug messages
DEBUG = False

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

    # debug(str(len(grid)))
    # debug(str(len(grid[0])))
    # debug(str(len(grid) * len(grid[0])))

    # Considering the grid is relatively small
    # I may use any approach and not overthink this

    #
    # Part 2
    #

    top_score = 0
    for y, row in enumerate(grid):
        for x, field in enumerate(row):
            left_side = row[:x]
            right_side = row[x+1:]
            column = [r[x] for r in grid]
            up_side = column[:y]
            down_side = column[y+1:]
            # I want to look for closest tree that fulfills come condition
            # for that, when I look left or up, I will need lists in a reverse order
            left_side.reverse()
            up_side.reverse()
            #
            # FIX:
            #
            # Need to add +1 to the index
            # if the view is blocked immediately by the adjacent field
            # the counted distance should be 1
            # but the index in the list is 0
            #
            # Also there should only be 0 if there are no trees in the direction (only border fields)
            # so if no field is blocking the view, the distance should be the number of fields in that direction
            # and not 0
            left_distance = next((i + 1 for i, v in enumerate(left_side) if v >= field), len(left_side))
            right_distance = next((i + 1 for i, v in enumerate(right_side) if v >= field), len(right_side))
            up_distance = next((i + 1 for i, v in enumerate(up_side) if v >= field), len(up_side))
            down_distance = next((i + 1 for i, v in enumerate(down_side) if v >= field), len(down_side))
            score = left_distance * right_distance * up_distance * down_distance
            # if score != 0:
            #     debug(score)
            if score > top_score:
                top_score = score
                debug(top_score)
    print('Highest scenic score: ' + str(top_score))
    # exit(0)
    #
    # END: Part 2
    #

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

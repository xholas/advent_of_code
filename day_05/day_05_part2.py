import sys

# Print debug messages
DEBUG = False

# Split input lines with crates to chunks of this size
# Chunk size should be number of characters from beginning of one crate to beginning of the other
#
# [J] [S] [N]
#  1   2   3
# Chunks: "[J] ", "[S] "... -> size = 4
CHUNK_SIZE = 4


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def move(crate_stacks, count, from_idx, to_idx):
    """New updated version for CrateMover 9001"""
    debug('-- Move by ' + str(count) + ' --')
    debug('\tBefore:')
    debug('\t\t[' + str(from_idx) + ']: ' + str(crate_stacks[from_idx]))
    debug('\t\t[' + str(to_idx) + ']: ' + str(crate_stacks[to_idx]))

    moving = crate_stacks[from_idx][-count:]
    # debug('\tMoving: ' + str(moving))
    new = crate_stacks[to_idx] + moving
    # debug('\tResult: ' + str(new))
    source = crate_stacks[from_idx][:-count]
    # debug('\tSource: ' + str(source))

    crate_stacks[to_idx] = new
    crate_stacks[from_idx] = source

    debug('\tAfter:')
    debug('\t\t[' + str(from_idx) + ']: ' + str(crate_stacks[from_idx]))
    debug('\t\t[' + str(to_idx) + ']: ' + str(crate_stacks[to_idx]))


def get_top_crates(crate_stacks):
    top_crates = []
    for stack in crate_stacks:
        debug('Stack: ' + str(stack))
        top_crates.append(stack[-1])
        debug('\tTop crate: ' + stack[-1])
    return top_crates


def main():
    with open('input_day_05.txt') as input_file:
        lines_stack = []
        # Read lines until empty line
        for line in input_file:
            line = line.strip()
            if line == "":
                break
            # Save lines to process them based on last line
            lines_stack.append(line)
        # Process the crate stack numbers
        stacks_numbers = lines_stack.pop().split()
        debug(stacks_numbers)
        # Create stacks of crates
        crate_stacks = [[] for _ in range(len(stacks_numbers))]
        while len(lines_stack) > 0:
            line = lines_stack.pop()
            crates = [line[i:i+CHUNK_SIZE] for i in range(0, len(line), CHUNK_SIZE)]
            debug('Crates: ' + str(crates))
            for idx, crate in enumerate(crates):
                name = crate[1]
                if name == ' ':
                    continue
                debug('\tCrate [' + str(idx) + ']: ' + name)
                crate_stacks[idx].append(name)
        # debug(crate_stacks)

        # Move crates according to "the rearrangement procedure"
        for line in input_file:
            line = line.strip()
            # debug(line)

            # Get instructions from input
            # line: "move 1 from 8 to 4"
            # 0: "move", 1: "1", 2: "from", 3: "8", 4: "to", 5: "4"
            instructions = line.split()
            inst_count = int(instructions[1])
            # Instructions use indexing starting by 1, but I use 0 based indexing.
            # I need to convert indexes to internal by subtracting 1
            inst_from = int(instructions[3]) - 1
            inst_to = int(instructions[5]) - 1
            # debug('Instruction: move <' + str(inst_count) + '> from <' + str(inst_from) + '> to <' + str(inst_to) + '>')

            # Move the crates
            move(crate_stacks, inst_count, inst_from, inst_to)

        # Get top crates from final arrangement
        top_crates = get_top_crates(crate_stacks)
        debug('Top crates: ' + str(top_crates))
        top_crates_str = ''.join(top_crates)
        print(top_crates_str)


if __name__ == '__main__':
    main()

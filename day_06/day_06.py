import re
import sys

# Print debug messages
DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def get_pattern_for_len(length):
    # debug(length)
    if length == 1:
        return '(.)'
    return get_pattern_for_len(length - 1) + '(?!' + '|'.join(['\\' + str(x) for x in range(1, length)]) + ')(.)'


def main():
    # Load the buffer
    with open('input_day_06.txt') as input_file:
        buffer = input_file.read()
    debug(buffer)
    # Find the start-of-packet marker sequence
    sequence_match = re.search(r'(.)(?!\1)(.)(?!\1|\2)(.)(?!\1|\2|\3).', buffer)
    debug(sequence_match)
    # Get the length
    length = sequence_match.span()[1]
    print('Chars in buffer to the end of starting marker: ' + str(length))

    # Part 2
    # Create regex pattern for 14 distinct character sequence
    # (Yes, I am sick of this myself. Please, forgive me.)
    pattern = get_pattern_for_len(14)
    debug(pattern)
    # Find the match
    match = re.search(pattern, buffer)
    debug(match)
    # Print the length
    print('Just take the number and stop this evil code ASAP: ' + str(match.span()[1]))


if __name__ == '__main__':
    main()

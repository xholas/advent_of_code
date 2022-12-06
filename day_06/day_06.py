import re
import sys

# Print debug messages
DEBUG = True


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


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


if __name__ == '__main__':
    main()

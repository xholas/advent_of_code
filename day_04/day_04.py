import sys

# Print debug messages
DEBUG = True


class Range:
    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)
        # Start should always be lower than end (or equal)
        if self.start > self.end:
            self.start, self.end = self.end, self.start

    def __str__(self):
        return 'Range: ' + str(self.start) + '-' + str(self.end)

    def does_contain(self, other):
        if not isinstance(other, Range):
            raise Exception('Method <' + Range.does_contain.__name__ + '> can only compare Range with other Range.')
        if self.start <= other.start and other.end <= self.end:
            return True
        return False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def main():
    with open('input_day_04.txt') as file:
        full_overlaps_cnt = 0
        for line in file:
            line = line.strip()
            debug(line)
            # Get ranges
            first_str, second_str = line.split(',', 1)
            first_list = first_str.split('-', 1)
            second_list = second_str.split('-', 1)
            first = Range(first_list[0], first_list[1])
            second = Range(second_list[0], second_list[1])
            debug("\t" + str(first))
            debug("\t" + str(second))
            # Is fully overlapping?
            is_overlap = first.does_contain(second) or second.does_contain(first)
            debug("\tOverlapping: " + str(is_overlap))
            if is_overlap:
                full_overlaps_cnt += 1
    print('Fully overlapping ranges: ' + str(full_overlaps_cnt))


if __name__ == '__main__':
    main()

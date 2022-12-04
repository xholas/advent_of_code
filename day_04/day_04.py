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
        # Fully contained
        # Other starts after self and ends before self (any border may be equal)
        # Self:  -12345-
        # Other: ---345-
        if self.start <= other.start and other.end <= self.end:
            return True
        return False

    def does_overlap(self, other):
        if not isinstance(other, Range):
            raise Exception('Method <' + Range.does_overlap.__name__ + '> can only compare Range with other Range.')
        # No overlap
        # One ends before other starts
        # Self:  -123---    or  -----45-
        # Other: ----45-        -123----
        if self.end < other.start or other.end < self.start:
            return False
        # Everything else is overlap (including one fully contained in the other)
        return True


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def main():
    with open('input_day_04.txt') as file:
        full_overlaps_cnt = 0
        any_overlaps_cnt = 0
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
            debug("\tFull overlap: " + str(is_overlap))
            if is_overlap:
                full_overlaps_cnt += 1
            # Is any overlap?
            is_overlap = first.does_overlap(second)
            debug("\tAny overlap: " + str(is_overlap))
            if is_overlap:
                any_overlaps_cnt += 1
    print('Fully overlapping ranges: ' + str(full_overlaps_cnt))
    print('All overlapping ranges: ' + str(any_overlaps_cnt))


if __name__ == '__main__':
    main()

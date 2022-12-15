import sys

# Print debug messages
DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


class PacketPart:
    type_number = 1
    type_list = 2

    def __init__(self, definition_str):
        if not isinstance(definition_str, str):
            raise Exception('Definition string must be a string. (That seems obvious.)')
        # definition string may be a list starting with [ and ending with matching ]
        # or a number (sequence of numeric chars)
        if definition_str.isnumeric():
            # number
            self.type = self.type_number
            self.value = int(definition_str)
        elif definition_str[0] == '[' and definition_str[-1] == ']':
            # list
            self.type = self.type_list
            self.value = self.parse_list(definition_str)

    def __str__(self):
        if self.type == self.type_number:
            return str(self.value)
        else:
            return '[' + ','.join([str(x) for x in self.value]) + ']'

    def parse_list(self, list_str):
        token_string = list_str[1:-1]  # remove [ and ] around list
        new_list = []
        while len(token_string) != 0:
            first, token_string = self.split_token(token_string)
            new_list.append(PacketPart(first))
        return new_list

    def split_token(self, token_str):
        # from string like 75,14,[...],... get the number before ',' and remaining string after it
        # from string like [[],[4,[2]],2],7 get the whole group as first item and only '7' as remaining
        indent_level = 0
        for idx, char in enumerate(token_str):
            # count 'indentation' - how many levels inside list structure the position is
            if char == '[':
                indent_level += 1
            elif char == ']':
                indent_level -= 1
            # only split if not inside any list
            if indent_level == 0:
                if char == ',':
                    return token_str[:idx], token_str[idx + 1:]
        return token_str, ''


def compare_order(first, second):
    debug('')
    debug(first)
    debug(second)
    # Both values are numbers
    if first.type == second.type == PacketPart.type_number:
        if first.value < second.value:
            debug('Correct order: ' + str(first.value) + ' < ' + str(second.value))
            return 1
        elif first.value == second.value:
            debug('Correct order: ' + str(first.value) + ' == ' + str(second.value))
            return 0
        else:
            debug('Wrong order: ' + str(first.value) + ' > ' + str(second.value))
            return -1
    # Both values are lists
    elif first.type == second.type == PacketPart.type_list:
        for idx in range(min(len(first.value), len(second.value))):
            comp = compare_order(first.value[idx], second.value[idx])
            if comp != 0:
                return comp
        if len(first.value) < len(second.value):
            debug('Correct order: len(' + str(len(first.value)) + ') < len(' + str(len(second.value)) + ')')
            return 1
        elif len(first.value) == len(second.value):
            debug('Correct order: len(' + str(len(first.value)) + ') == len(' + str(len(second.value)) + ')')
            return 0
        else:
            debug('Wrong order: len(' + str(len(first.value)) + ') > len(' + str(len(second.value)) + ')')
            return -1
    # Different types
    else:
        if first.type == PacketPart.type_number:
            return compare_order(PacketPart('[' + str(first.value) + ']'), second)
        else:
            return compare_order(first, PacketPart('[' + str(second.value) + ']'))


def main():
    # with open('input_test.txt') as file_input:
    with open('input_day_13.txt') as file_input:
        contents = file_input.read().strip()
        pairs = contents.split('\n\n')

        correct_cnt = 0
        index_sum = 0
        for idx, pair in enumerate(pairs, start=1):
            first_str, second_str = pair.split('\n')
            # debug('First: ' + first_str)
            first = PacketPart(first_str)
            # debug('Test1: ' + str(first))
            # debug('Second: ' + second_str)
            second = PacketPart(second_str)
            # debug('Test 2: ' + str(second))

            if compare_order(first, second) != -1:
                correct_cnt += 1
                index_sum += idx
    print('Number of pairs in correct order: ' + str(correct_cnt))
    print('Sum of their indexes: ' + str(index_sum))


if __name__ == '__main__':
    main()

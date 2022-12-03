
def get_shared_item(first, second):
    set1 = set(first)
    set2 = set(second)
    shared = set1 & set2
    if len(shared) != 1:
        raise Exception('Exactly one shared item expected but found <' + len(shared) + '>'
                        + ' in <' + first + '> and <' + second + '>')
    return shared.pop()


def get_item_priority(item):
    if ord('a') <= ord(item) <= ord('z'):
        # lowercase a..z
        return ord(item) - ord('a') + 1
    if ord('A') <= ord(item) <= ord('Z'):
        # UPPERCASE A..Z
        return ord(item) - ord('A') + 27
    raise Exception('Item should be lowecase or uppercase letter. Input letter was <' + item + '>')


def main():
    with open('input_day_03.txt') as file:
        priority_sum = 0
        for line in file:
            rucksack_content = line.strip()  # remove end of line
            # print(rucksack_content)

            # Count content size
            item_count = len(rucksack_content)
            half_size = item_count // 2
            # print("\tSize: " + str(item_count) + " half is: " + str(half_size))
            if item_count % 2 == 1:
                raise Exception('Item count should always be even number.')

            # Split to two parts - rucksack compartments
            first_half = rucksack_content[:half_size]
            second_half = rucksack_content[half_size:]
            # print("\t" + first_half)
            # print("\t" + second_half)

            # Find the shared item
            shared_item = get_shared_item(first_half, second_half)
            # print("\tShared: " + shared_item)

            # Get items priority
            priority = get_item_priority(shared_item)
            priority_sum += priority
            # print("\tPriority: " + str(priority))
    print("Sum of priorities: " + str(priority_sum))


if __name__ == '__main__':
    main()

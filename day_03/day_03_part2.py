
# Print debug messages
DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def get_shared_item(rucksack_list):
    shared = set(rucksack_list[0])  # Set up initial set of values to be filtered
    for rucksack in rucksack_list[1:]:  # Skip first rucksack in list as it was assigned above
        item_set = set(rucksack)
        shared = shared & item_set
    if len(shared) != 1:
        raise Exception('Exactly one shared item expected but found <' + str(len(shared)) + '> in list: '
                        + str(rucksack_list))
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
        group_rucksacks = []
        for line in file:
            # Read rucksack from file
            rucksack_content = line.strip()  # remove end of line
            debug(rucksack_content)

            # Remove old group if exists
            if len(group_rucksacks) >= 3:
                group_rucksacks = []
            # Add rucksack to group
            group_rucksacks.append(rucksack_content)

            # If group is not complete, find all rucksacks first
            if len(group_rucksacks) < 3:
                continue

            #
            # Continue here only with completed group
            #

            # Find the shared item
            shared_item = get_shared_item(group_rucksacks)
            debug("\tShared: " + shared_item)

            # Get items priority
            priority = get_item_priority(shared_item)
            priority_sum += priority
            debug("\tPriority: " + str(priority))
    print("Sum of priorities: " + str(priority_sum))


if __name__ == '__main__':
    main()

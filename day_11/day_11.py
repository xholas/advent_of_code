import sys

# Print debug messages
DEBUG = True


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


class Monkey:
    def __init__(self,
                 starting_items,
                 operation_type,
                 operation_amount,
                 test_divisible,
                 target_true,
                 target_false,
                 monkeys_list):
        if not isinstance(starting_items, list):
            raise Exception('Items must be a list of numbers.')
        self.items = starting_items
        self.operation = operation_type
        self.operation_amount = operation_amount
        self.test_divisible = test_divisible
        self.target_true = target_true
        self.target_false = target_false
        self.monkeys_list = monkeys_list

        self.inspected_items = 0

    def __str__(self):
        return 'Monkey ' + str(next(idx for idx, monke in enumerate(self.monkeys_list) if monke is self)) \
               + ' with ' + str(len(self.items)) + ' items. \n' \
               + 'Testing divisibility by ' + str(self.test_divisible) \
               + ' - then throwing to ' + str(self.target_true) + ' or ' + str(self.target_false) + '. \n' \
               + 'You get worried ' + self.operation + ' ' + self.operation_amount + ' every time it picks up an item.'

    def inspect(self, worry_level):
        # Count inspected items
        self.inspected_items += 1

        # What is the operation value?
        if not isinstance(self.operation_amount, str):
            raise Exception('Operation amount must be stored as a string.')
        if self.operation_amount.isnumeric():
            operation_value = int(self.operation_amount)
        elif self.operation_amount == 'old':
            operation_value = worry_level
        else:
            raise Exception('Unknown operation amount <' + self.operation_amount + '>')

        # Based on type, how does the worry level change?
        if self.operation == '+':
            return worry_level + operation_value
        elif self.operation == '*':
            return worry_level * operation_value
        else:
            raise Exception('Unknown operation type <' + self.operation + '>')

    def test(self, worry_level):
        # What is the target based on the divisibility test?
        if worry_level % self.test_divisible == 0:
            return self.target_true
        else:
            return self.target_false

    def turn(self):
        # Turn is when monkey inspects and throws all its items
        while len(self.items) != 0:  # Must not loop over items in changing list
            # Inspect item
            # - take item from list and see the worry level
            # debug('-------------------------------------------------')
            # debug('Monke has: ' + str(self.items))
            item_worry_level = self.items.pop(0)  # Really? pop() pops last item? not first?
            # debug('Monke gets: ' + str(self.items))
            # - raise worry level based on the operation
            item_worry_level = self.inspect(item_worry_level)

            # Relief
            # - the relief causes the worry level to be divided by three and rounded down
            item_worry_level = item_worry_level // 3

            # Test worry level
            target_monkey_idx = self.test(item_worry_level)
            target_monkey = self.monkeys_list[target_monkey_idx]
            if not isinstance(target_monkey, Monkey):
                raise Exception('Monkey! Are you with us?!')

            # Throw an item
            # debug('-------------------------------------------------')
            # debug('Monke has: ' + str(target_monkey.items))
            target_monkey.items.append(item_worry_level)
            # debug('Monke gets: ' + str(target_monkey.items))


def setup_monkey(monkey_info, monkeys_list):
    monkey_name = monkey_info[0].split()
    monkey_number = int(monkey_name[1][:1])
    debug('Monkey number: ' + str(monkey_number))

    monkey_items = [int(x.strip(',')) for x in monkey_info[1].split()[2:]]
    debug('Monkey items: ' + str(monkey_items))

    monkey_operation = monkey_info[2].split()
    monkey_operation_type = monkey_operation[4]
    monkey_operation_value = monkey_operation[5]
    debug('Monkey operation is <' + monkey_operation_type + '> with value <' + monkey_operation_value + '>')

    monkey_test_divisible = int(monkey_info[3].split()[3])
    debug('Monkey tests divisibility by: ' + str(monkey_test_divisible))

    monkey_target_true = int(monkey_info[4].split()[-1])
    monkey_target_false = int(monkey_info[5].split()[-1])
    debug('Monkey throws items to <' + str(monkey_target_true) + '> if condition is true, '
          'otherwise to <' + str(monkey_target_false) + '>')

    if monkey_number != len(monkeys_list):
        raise Exception('Monkeys order is not correct. '
                        'Next monkey index should be <' + str(monkey_number) + '> '
                        'but is <' + str(len(monkeys_list)) + '>')

    monkeys_list.append(Monkey(
        monkey_items,
        monkey_operation_type,
        monkey_operation_value,
        monkey_test_divisible,
        monkey_target_true,
        monkey_target_false,
        monkeys_list
    ))


def main():
    monkeys = []
    # with open('input_test.txt') as file_input:
    with open('input_day_11.txt') as file_input:
        input_all = file_input.read()

    # Split per Monkey
    input_per_monkey = input_all.split('\n\n')
    for monkey_info_str in input_per_monkey:
        # debug('START')
        # debug(monkey_info_str)
        # debug('STOP\n\n')
        monkey_info = monkey_info_str.split('\n')
        debug('\nInfo: ' + str(monkey_info))

        setup_monkey(monkey_info, monkeys)

    debug('\nThere are ' + str(len(monkeys)) + ' monkeys. Last is:')
    debug(monkeys[-1])

    max_rounds = 20
    # Monkeys play for 20 rounds
    for current_round in range(max_rounds):
        # Round is when all monkeys take one turn
        for monkey in monkeys:
            if not isinstance(monkey, Monkey):
                raise Exception('This is no monkey!')
            # Turn is when monkey inspects and throws all its items
            monkey.turn()
        debug('\nAfter round: ' + str(current_round + 1))
        for num, monkey in enumerate(monkeys):
            debug('Monkey ' + str(num) + ': ' + str(monkey.items))

    debug('\nThere are ' + str(len(monkeys)) + ' monkeys. \nFirst is:')
    debug(monkeys[1])

    debug('\nAnd last is:')
    debug(monkeys[-1])

    debug('\nNuber of inspections:')
    for idx, monkey in enumerate(monkeys):
        debug('Monkey ' + str(idx) + ': ' + str(monkey.inspected_items))

    monkey_activity = [monke.inspected_items for monke in monkeys]
    # debug(monkey_activity)

    # First most active monkey
    top_activity = max(monkey_activity)

    # Second most active monkey
    monkey_activity.remove(top_activity)
    second_activity = max(monkey_activity)

    # Monkey business level
    monkey_business_level = top_activity * second_activity
    print('The level of monkey business is ' + str(monkey_business_level))


if __name__ == '__main__':
    main()

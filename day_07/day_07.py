import sys

# Print debug messages
DEBUG = False

# Constants
MAX_DIR_SIZE = 100000


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


class Dir:
    def __init__(self, name, parent=None):
        if parent is not None and not isinstance(parent, Dir):
            raise Exception('Parent of Dir has to be another Dir or None.')
        if parent is self:
            raise Exception('Parent of Dir cannot be the same Dir.')
        self.name = name
        self.content = []
        self.size = 0
        self.parent = parent
        if self.parent is not None:
            self.parent.add(self)

    def __str__(self):
        return self.as_string()

    def as_string(self, indent=0):
        return '\t' * indent + '[' + self.name + ']\t' + '(' + str(self.size) + ')' + '\n' \
               + '\n'.join([x.as_string(indent + 1) for x in self.content])

    def add_size(self, size):
        self.size += size
        if self.parent is not None:
            self.parent.add_size(size)

    def add(self, item):
        if isinstance(item, Dir):
            item.parent = self
        self.content.append(item)
        self.add_size(item.size)


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def as_string(self, indent=0):
        return '\t' * indent + '- ' + self.name + '\t(' + str(self.size) + ')'


# Global
DIR_ROOT = Dir('/')
current_dir = DIR_ROOT


def command(args):
    global current_dir
    if args[1] == 'cd':
        debug('Change dir.')
        if args[2] == '/':
            current_dir = DIR_ROOT
        elif args[2] == '..':
            if current_dir.parent is None:
                raise Exception('No parent Dir for ' + current_dir.name)
            current_dir = current_dir.parent
        else:
            if args[2] not in [x.name for x in current_dir.content]:
                raise Exception('No ' + args[2] + ' in Dir ' + current_dir.name)
            items = list(x for x in current_dir.content if x.name == args[2])
            if len(items) == 0:
                raise Exception('Item ' + args[2] + ' not found in Dir ' + current_dir.name)
            if len(items) > 1:
                raise Exception('Multiple files named ' + args[2] + ' in Dir ' + current_dir.name)
            if not isinstance(items[0], Dir):
                raise Exception('Item ' + args[2] + ' in Dir ' + current_dir.name + ' is not Dir.')
            current_dir = items[0]
    elif args[1] == 'ls':
        debug('List dir.')
        pass  # Just ignore this as it is irrelevant
    else:
        raise Exception('Unknown command: ' + str(args))


def files(args):
    if args[0] == 'dir':
        debug('Directory: ' + args[1])
        current_dir.add(Dir(args[1]))
        return

    try:
        size = int(args[0])
    except ValueError:
        size = None
    if size is not None:
        debug('File size: ' + str(size))
        current_dir.add(File(args[1], size))
    else:
        raise Exception('Unknown file: ' + str(args))


def get_sum(my_dir=DIR_ROOT):
    size_sum = my_dir.size if my_dir.size <= MAX_DIR_SIZE else 0
    for item in my_dir.content:
        if not isinstance(item, Dir):
            continue
        size_sum += get_sum(item)
    debug('get_sum(): Dir: ' + my_dir.name + '\tsize: ' + str(my_dir.size) + '\ttotal size: ' + str(size_sum))
    return size_sum


def main():
    with open('input_day_07.txt') as file_input:
        for line in file_input:
            line = line.strip()

            args = line.split()
            debug('\n' + str(args))

            if args[0] == '$':
                command(args)
            else:
                files(args)
    debug(str(DIR_ROOT))
    # Sum of dir sizes smaller or equal MAX_DIR_SIZE = 100000
    sizes_sum = get_sum()
    print('Sum: ' + str(sizes_sum))


if __name__ == '__main__':
    main()

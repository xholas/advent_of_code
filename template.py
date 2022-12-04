import sys

# Print debug messages
DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


def main():
    pass


if __name__ == '__main__':
    main()

import sys

# Print debug messages
DEBUG = True


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


INST_NOOP = 'noop'
INST_ADDX = 'addx'

CY_STEP = 40
CY_START = 20
CY_CNT = 6
CY_STOP = CY_START + (CY_CNT - 1) * CY_STEP


def main():
    cycle = 0
    inst_type = INST_NOOP
    inst_value = 0
    inst_wait = 0
    reg_x = 1
    score_sum = 0
    # with open('input_test.txt') as file_input:
    with open('input_day_10.txt') as file_input:
        while cycle <= CY_STOP:
            current_cycle = cycle + 1
            debug('Running cycle: ' + str(current_cycle))
            if inst_wait <= 0:
                # Complete the instruction
                debug('\tInstruction complete.')
                if inst_type == INST_ADDX:
                    reg_x += inst_value
                    debug('\tAdded ' + str(inst_value) + ' - new reg value is ' + str(reg_x))

            # BUGFIX: Following code has to run in each cycle UNCONDITIONALLY

            # At this point the value for REG X is valid for this cycle
            debug('--- REG X value: ' + str(reg_x))

            if current_cycle in range(CY_START, CY_STOP + 1, CY_STEP):
                score = current_cycle * reg_x
                debug('  - Cycle ' + str(current_cycle) +
                      ' | REG X value: ' + str(reg_x) +
                      ' | Score: ' + str(score) + ' ---------------------------------------------')
                score_sum += score

            # BUGFIX: But the next part needs the condition again

            if inst_wait <= 0:
                # Load new instruction
                debug('\tLoading next instruction.')
                line = file_input.readline().strip()  # Strip needed - this is probably due to input using CR/LF
                if line == INST_NOOP:
                    inst_type = INST_NOOP
                    inst_wait = 1
                    debug('\tRunning NOOP - finish in 1 cycle')
                else:
                    inst_type = INST_ADDX
                    inst_value = int(line.split(maxsplit=1)[1])
                    inst_wait = 2
                    debug('\tRunning ADDX ' + str(inst_value) + ' - finish in 2 cycles')

            # Complete the cycle
            cycle += 1
            inst_wait -= 1
        print('Signal strength sum: ' + str(score_sum))


if __name__ == '__main__':
    main()

import sys
from letter_map import recognize_letter

# Print debug messages
DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, file=sys.stderr, **kwargs)


INST_NOOP = 'noop'
INST_ADDX = 'addx'

CY_STEP = 40
CY_START = 20
CY_CNT = 6
CY_STOP = CY_START + (CY_CNT - 1) * CY_STEP

CRT_LINES = 6
CRT_COLUMNS = 40

# Using unicode blocks for better visibility
# https://en.wikipedia.org/wiki/Block_Elements
PIX_MODE = 2
if PIX_MODE == 1:
    PIX_LIT = '█'
    PIX_DARK = ' '
elif PIX_MODE == 2:
    PIX_LIT = '▓'
    PIX_DARK = '░'
else:
    PIX_LIT = '#'
    PIX_DARK = '.'


def main():
    cycle = 0
    inst_type = INST_NOOP
    inst_value = 0
    inst_wait = 0
    reg_x = 1
    score_sum = 0

    crt_image = []

    # with open('input_test.txt') as file_input:
    with open('input_day_10.txt') as file_input:
        while cycle < CRT_LINES * CRT_COLUMNS:  # There should be 6 lines with 40 pixels per line - then this may stop
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

            # Draw the image
            crt_line = cycle // 40
            crt_column = cycle % 40
            # Create new image line if needed
            if crt_column == 0:
                debug('' if len(crt_image) == 0 else crt_image[crt_line - 1])  # Debug print previous line
                crt_image.append([])
            # If sprite (REG X value +- 1) under the pixel (current cycle % 40)
            # Draw lit pixel
            if reg_x - 1 <= crt_column <= reg_x + 1:
                crt_image[crt_line].append(PIX_LIT)
            else:
                crt_image[crt_line].append(PIX_DARK)

            if inst_wait <= 0:
                # Load new instruction
                debug('\tLoading next instruction.')
                line = file_input.readline()
                if line == '':
                    # Break the loop at the end of input
                    break
                line = line.strip()  # Strip needed - this is probably due to input using CR/LF
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
        for line in crt_image:
            print(''.join(line))

        # BONUS
        # It seems that letters are 4 pix wide and 6 pix tall
        # (that makes sense, as there should be 8 letters on 40*6 grid - leaving 5 pix width per letter and space)
        crt_string = ''
        for letter_idx in range(8):
            offset = 5 * letter_idx
            letter = [line[0+offset:4+offset] for line in crt_image]
            for line in letter:
                debug(''.join(line))
            char = recognize_letter(letter, PIX_LIT, PIX_DARK)
            debug(char)
            debug('')
            crt_string += char
        print('CRT shows following text: ' + crt_string)


if __name__ == '__main__':
    main()

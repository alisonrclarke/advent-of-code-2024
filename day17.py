import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day17_test_input{suffix}.txt"
else:
    input_file = f"day17_input.txt"

data = utils.input_as_lines(input_file)

reg_a = int(data[0].rsplit(": ")[-1])
reg_b = int(data[1].rsplit(": ")[-1])
reg_c = int(data[2].rsplit(": ")[-1])
programme = [int(n) for n in data[4].rsplit(": ")[-1].split(",")]

p = 0


def get_combo_operand(operand):
    if operand == 4:
        return reg_a
    elif operand == 5:
        return reg_b
    elif operand == 6:
        return reg_c

    return operand


output = []
while p < len(programme):
    opcode = programme[p]
    operand = programme[p + 1]

    jumped = False

    if opcode == 0:
        # adv
        combo_operand = get_combo_operand(operand)
        reg_a = reg_a // (2**combo_operand)
    elif opcode == 1:
        # bxl
        reg_b = reg_b ^ operand
    elif opcode == 2:
        # bst
        reg_b = get_combo_operand(operand) % 8
    elif opcode == 3:
        # jnz
        if reg_a != 0:
            p = operand
            jumped = True
    elif opcode == 4:
        # bxc
        reg_b = reg_b ^ reg_c
    elif opcode == 5:
        # out
        output.append(get_combo_operand(operand) % 8)
    elif opcode == 6:
        # bdv
        combo_operand = get_combo_operand(operand)
        reg_b = reg_a // (2**combo_operand)
    elif opcode == 7:
        # cdv
        combo_operand = get_combo_operand(operand)
        reg_c = reg_a // (2**combo_operand)

    if not jumped:
        p += 2

print("Part 1:", ",".join([str(n) for n in output]))

# Part 2 - needed a lot of hints from reddit here and it's still not optimal
# Because of the % 8 in the ops we can start by finding a value that gives the last value in our programme,
# then multiply that by 8 to start looking for the next value

n_to_match = 1
previous_answer = None

while True:
    print(f"looking for last {n_to_match} values")
    if previous_answer:
        initial_reg_a = previous_answer * 8
    else:
        initial_reg_a = 1

    while True:
        reg_a = initial_reg_a
        output = []

        p = 0
        while p < len(programme):
            opcode = programme[p]
            operand = programme[p + 1]

            jumped = False

            if opcode == 0:
                # adv
                combo_operand = get_combo_operand(operand)
                reg_a = reg_a // (2**combo_operand)
            elif opcode == 1:
                # bxl
                reg_b = reg_b ^ operand
            elif opcode == 2:
                # bst
                reg_b = get_combo_operand(operand) % 8
            elif opcode == 3:
                # jnz
                if reg_a != 0:
                    p = operand
                    jumped = True
            elif opcode == 4:
                # bxc
                reg_b = reg_b ^ reg_c
            elif opcode == 5:
                # out
                output.append(get_combo_operand(operand) % 8)
            elif opcode == 6:
                # bdv
                combo_operand = get_combo_operand(operand)
                reg_b = reg_a // (2**combo_operand)
            elif opcode == 7:
                # cdv
                combo_operand = get_combo_operand(operand)
                reg_c = reg_a // (2**combo_operand)

            if not jumped:
                p += 2

        if output[-n_to_match:] == programme[-n_to_match:]:
            previous_answer = initial_reg_a
            break

        initial_reg_a += 1

    n_to_match += 1
    if n_to_match > len(programme):
        break

print(f"Part 2: {initial_reg_a}")

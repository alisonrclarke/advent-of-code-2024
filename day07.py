import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day07_test_input{suffix}.txt"
else:
    input_file = f"day07_input.txt"

data = utils.input_as_lines(input_file)


def check_op(ans, args):
    if len(args) == 1:
        return ans == args[0]
    elif len(args) == 2:
        return (args[0] + args[1] == ans) or (args[0] * args[1] == ans)
    else:
        start = args[:-1]
        last = args[-1]

        add_ans = check_op(ans - last, start)
        if add_ans:
            return add_ans
        else:
            return check_op(ans / last, start)


total = 0
invalid = []

for line in data:
    ans, args = line.split(": ")
    ans = int(ans)
    args = [int(a) for a in args.split(" ")]

    is_valid = check_op(ans, args)
    if is_valid:
        total += ans
    else:
        invalid.append((ans, args))

print(f"Part 1: {total}")


# Part 2 - use brute force to try every combination
def get_all_answers(args):
    if len(args) <= 1:
        return args
    elif len(args) == 2:
        return {args[0] + args[1], args[0] * args[1], int(str(args[0]) + str(args[1]))}
    else:
        sub_answers = get_all_answers(args[:-1])
        answers = [
            [a + args[-1], a * args[-1], int(str(a) + str(args[-1]))]
            for a in sub_answers
        ]
        return {a2 for a in answers for a2 in a}


for ans, args2 in invalid:
    all_answers = get_all_answers(args2)
    if ans in all_answers:
        total += ans

print(f"Part 2: {total}")

# Advent of Code 2024

## How to set up for a new day

Run:

```
python setup_day.py <day>
```

e.g. for day 7:

```
python setup_day.py 7
```

This will create 3 files (if they don't already exist):

 * **day<day>.py**: the main python script into which you'll write your solution. It will include some basic boilerplate code, importing `utils`, and finding the relevant input file.
 * **day<day>_input.txt: a blank file in which to paste your own puzzle input from the site. This will be ignored by git in accordance with the [request from the Aoc mods](https://www.reddit.com/r/adventofcode/comments/e7khy8/comment/fa13hb9/).
 * **day<day>_test_input.txt: a blank file into which you can paste the text puzzle input from the main puzzle page.

**day<day>.py** is the main python file in which to create your solution. Once it's created just edit it as you wish.

## How to run

To run with the test input, run;

```
python day<day>.py test
```

Make sure to use the 2-digit day number as per the created file name.

And to run with the main input, run:

```
python day<day>.py
```

Sometimes (e.g. for those pesky times when your code works on the test input but not on the full input), you might want to create multiple test input files. If you create them with the naming convention `day<day>_test_input<suffix>.txt` then you can add the suffix to the command line and your new test file will be found, e.g. if you create an additional file `day07_test_input2.txt` then you can run:


```
python day07.py test 2
```

## utils

`utils.py` contains some useful functions for parsing the input file:

 * `input_as_string` returns the content of the input file as a string
 * `input_as_lines` returns a list where each line in the input file is an element of the list
 * `input_as_ints` returns a list where each line in the input file is an element of the list, converted into an integer



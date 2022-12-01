# Advent of Code 2022

## Usage:

* Inside `./YYYY/DD/` create an `input.txt` and `day.py`...
    * `input.txt` contains your puzzle input
    * `day.py` contains...
        * `parse_input(data)` method which parses the data from the list of strings read from `input.txt`
        * `run_part_1(data)` and `run_part_2(data)` methods run and return the result for each part of the day's puzzle
* Update `DAY` in `main.py`
* Run `python main.py`
## Environment:
- Python Version: 3.9.6

## Requirements:
For this challenge, you must create a sort function that will sort a dataset in a hierarchical manner. Use your function to sort the `data/data-big-input.txt` file by `net_sales`, from highest to lowest.

## Dataset Format
The raw datasets are pipe-delimited CSV files / strings. We've attached some examples at the bottom of this gist.

The dataset's columns are:

- Properties:property0, property1, ..., propertyN
- Metrics: any non-property column

## Example
Here's an example dataset input with 2 properties, and one metric (`net_sales`).

|property0|property1|net_sales|
|---------|---------|-----|
| bar     | $total  | -200|
| foo     | sauce   |  300|
| $total  | $total  |  200|
| bar     | sup     | -400|
| foo     | $total  |  400|
| bar     | bro     |  200|
| foo     | lettuce |  100|

The sort function should produce an output that's sorted like this:

|property0|property1|net_sales|
|---------|---------|-----|
| $total  | $total  |  200|
| foo     | $total  |  400|
| foo     | sauce   |  300|
| foo     | lettuce |  100|
| bar     | $total  | -200|
| bar     | bro     |  200|
| bar     | sup     | -400|

## Commands
- run and output to standard out:
```bash
python app.py data/data-small-input.txt -v
```
- run and validate against an output file:
```bash
python app.py data/data-small-input.txt -va data/data-small-output.txt
```
- test:
```bash
python -m pytest
```
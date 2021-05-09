Command line interface tool for calculating serviceability. The application accepts a JSON file containing income and expenses, and uses this information to calculate serviceability. The application logs to serviceability.log.

# Usage

Run the application:

`python3 app.py`

Pass it a json file containing income and expenses:

`python3 app.py -i input.json`

Override the FACTOR via CLI. Let's set it to 3.5:

`python3 app.py -i input.json -f 3.5`

## Parameters

| Parameter | Description | Default Value  |
| :------------- | :------------------ | :-- |
| -h, --help    | Show help messages |     |
| -i, --input  | Pass in a JSON file to calculate serviceability |   |
| -f, --factor | Set the FACTOR | 1.5 |
| -v, --version | Show program's version number |   |

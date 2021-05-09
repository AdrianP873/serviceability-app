"""
Calculates the serviceability of given 'application', where 'application' is represented by a JSON file.
"""

import argparse
import json
import logging
import os
import sys
from datetime import date, datetime

# Set FACTOR. Setting FACTOR via command line will override the value set here.
FACTOR = 1.5

# Configure logging to serviceability.log file.
today = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
logging.basicConfig(filename='serviceability.log', level=logging.INFO)

# Instantiate CLI parser
parser = argparse.ArgumentParser(prog="Serviceability calculator",
                                 description="Calculates the serviceability of given 'application', \
                                 where 'application' is represented by a JSON file.")
parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')
parser.add_argument('-i', '--input', help="Pass in a JSON file to calculate serviceability.")
parser.add_argument('-f', '--factor', help="Set the FACTOR.")
args = parser.parse_args()


def check_file_validity(parser, input):
    """ Checks whether the file exists, and validates the JSON. """
    if not os.path.exists(input):
        logging.error(str(current_time) + " " + str(today) + " " + "The file {} does not exist.".format(input))
        parser.error("The file {} does not exist.".format(input))
    if input.endswith(".json"):
        try:
            with open(input) as f:
                return json.load(f)
        except ValueError as e:
            logging.error(str(current_time) + " " + str(today) + " " + str(e))
            sys.exit("Error: Invalid json: {}".format(e))
    else:
        logging.error(str(current_time) + " " + str(today) + " " + "Error: Please pass in a .json file")
        sys.exit("Error: Please pass in a .json file.")


def calc_yearly_income(yearlyValue):
    """ Calculates monthly income from yearly value. """
    monthly_value = yearlyValue / 12
    return monthly_value


def calc_quarterly_income(quarterlyValue):
    """ Calculates monthly income from quarterly value. """
    monthly_value = quarterlyValue / 3
    return monthly_value


def parse_json(fileName):
    """ Parses the input JSON file and calculates the serviceability. """
    global FACTOR
    total_monthly_income = 0
    total_monthly_expenses = 0
    surplus = 0

    check_file_validity(parser, fileName)

    if args.factor:
        try:
            FACTOR = float(args.factor)
        except ValueError as e:
            logging.error(str(current_time) + " " + str(today) + " " + str(e))
            sys.exit("Error: FACTOR must be a float.")

    try:
        json_file = open(fileName)
        data = json.load(json_file)

    # Calculate monthly income from JSON data
        for item in data['income']:
            if 'frequency' in item:
                frequency = item['frequency']

                if frequency == 'yearly':
                    for i in item.values():
                        if type(i) is float:
                            x = calc_yearly_income(i)
                            total_monthly_income += x
                elif frequency == 'quarterly':
                    for i in item.values():
                        if type(i) is float:
                            x = calc_quarterly_income(i)
                            total_monthly_income += x
                elif frequency == 'monthly':
                    for i in item.values():
                        if type(i) is float:
                            total_monthly_income += i
            else:
                print("Entry must contain frequency. The entry for " + str(item) + " will be ignored.")
                logging.warning("Entry must contain frequency. This entry will be ignored")

        print("Total monthly income: {}".format(total_monthly_income))

        # Calculate monthly expenses from JSON data
        for expenses in data['expenses']:
            for expense in expenses.values():
                assert type(expense) is float, "Expenses must be a float"
                total_monthly_expenses += expense
        print("Total monthly expenses: {}".format(total_monthly_expenses))
    except ValueError as e:
        print("Error: " + str(e))
        logging.error(str(current_time) + " " + str(today) + " " + str(e))

    surplus = total_monthly_income - total_monthly_expenses
    serviceability = surplus * FACTOR
    print("Raw surplus: {}".format(surplus))
    print("Serviceability (surplus * FACTOR): {}".format(serviceability))


if __name__ == '__main__':
    if args.input:
        parse_json(args.input)
    else:
        print("USAGE: Pass in a JSON file with the -i flag. Use -h for more information.")

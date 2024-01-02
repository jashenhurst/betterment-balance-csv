import re
from datetime import datetime
import os.path
import sys


def to_dict(string):
    result = {}
    for i in re.findall(r"Date\(\d{4}, \d{1,2}, \d{1,2}\),\n.*balance: parseFloat\('[0-9.]+", string):
        datestring = re.search('\d{4}, \d{1,2}, \d{1,2}', i).group()
        datelist = datestring.split(', ')

        # These use 0 for December, it's weird
        if datelist[1] == '0':
            datelist[0] = str(int(datelist[0]) - 1)
            datelist[1] = '12'
            datestring = ', '.join(datelist)
        try:
            date = datetime.strptime(datestring, "%Y, %m, %d")
        except ValueError:
            # These also have 31 days for every month
            print(datestring, 'is not a valid date')
        balance = re.search(r'\d+\.\d+', i).group()
        result[date.strftime("%Y-%m-%d")] = balance
    return result

def test():
    teststring = """  createOptions.balanceByDate.push({
        date: new Date(2013, 8, 16),
        balance: parseFloat('24.95'),
        totalInvested: parseFloat('25.0'),
        earned: parseFloat('-0.05')
      });
      createOptions.balanceByDate.push({
        date: new Date(2013, 8, 16),
        balance: parseFloat('24.95'),
        totalInvested: parseFloat('25.0'),
        earned: parseFloat('-0.05')
      });
      createOptions.balanceByDate.push({
        date: new Date(2013, 8, 17),
        balance: parseFloat('25.0'),
        totalInvested: parseFloat('25.0'),
        earned: parseFloat('0.0')
      });
      createOptions.balanceByDate.push({
        date: new Date(2013, 8, 18),
        balance: parseFloat('25.28'),
        totalInvested: parseFloat('25.0'),
        earned: parseFloat('0.28')
      });
      createOptions.balanceByDate.push({
        date: new Date(2013, 8, 19),
        balance: parseFloat('13337.06'),
        totalInvested: parseFloat('13356.65'),
        earned: parseFloat('-19.59')
      });
      createOptions.balanceByDate.push({
        date: new Date(2013, 8, 20),
        balance: parseFloat('13298.96'),
        totalInvested: parseFloat('13356.65'),
        earned: parseFloat('-57.69')
      });
      createOptions.balanceByDate.push({
        date: new Date(2014, 0, 1),
        balance: parseFloat('14473.64'),
        totalInvested: parseFloat('14256.65'),
        earned: parseFloat('216.99')
        });
    """
    date_balance_dict = to_dict(teststring)
    print(date_balance_dict)
    with open('test.csv', 'w') as csvfile:
        csvfile.write("Date,Balance\n")
        for i in date_balance_dict:
            print(str(i) + ',' + date_balance_dict[i], file=csvfile)
        csvfile.close()


if __name__ == '__main__':
    #test()
    for filename in sys.argv[1:]:
        date_balance_dict = {}
        with open(filename, 'r') as file:
            date_balance_dict = to_dict(file.read())
            file.close()
        base_filename = os.path.splitext(filename)[0]
        output_filename = base_filename + ".csv"
        with open(output_filename, 'w') as csvfile:
            csvfile.write('Date,Balance\n')
            for i in date_balance_dict:
                print(str(i) + ',' + date_balance_dict[i], file=csvfile)
            csvfile.close()
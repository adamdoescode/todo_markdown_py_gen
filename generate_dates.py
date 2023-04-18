'''
Generate a set of headers in my usual format used in my todo.md file

Use python calendar module

Format is: "## 30 Thursday (2019-12-12)"
'''

import datetime
import calendar
import argparse
import re
import os

def getInputArgs():
    '''
    Take input arguments from command line
    '''
    parser = argparse.ArgumentParser(
        description='Generate a set of headers in my usual format used in my todo.md file')
    parser.add_argument(
        '-n', '--ndays', type=int, default=10, help='number of days to generate')
    parser.add_argument(
        '-a', '--append', default=False, action='store_true', help='if True, append to todo.md, else print to stdout')
    parser.add_argument(
        '-s', '--startday', type=str, default=None, 
        help='if None, use today, else use the specified day. startDay expects format: (year, month, day) as list or tuple')
    args = parser.parse_args()
    return args

def parseStartDay(startDay):
    '''
    Parse the startDay argument
    '''
    # use re module regex to remove () or [] or {} or <>
    startDay = re.sub(r'[\(\)\[\]\{\}\<\>]', '', startDay)
    startDay = startDay.split(',')
    startDay = [int(i) for i in startDay]
    return startDay

def generateHeaders(nDays=10, append=True, startDay=None):
    '''
    This function generates a set of headers in my usual format used in my todo.md file
    It assumes today already exists
    nDays: number of days to generate
    append: if True, append to todo.md, else print to stdout
    startDay: if None, use today, else use the specified day
    startDay expects format: (year, month, day) as list or tuple
    '''
    if startDay is None:
        startDay = datetime.date.today()
    else:
        startDay = datetime.date(startDay[0], startDay[1], startDay[2])
    # print(today, weekday, month, year, day)
    # print(calendar.month_name[month], day, calendar.day_name[weekday])
    format_string = ''
    for i in range(nDays+1):
        if i > 0:
            startDay = startDay + datetime.timedelta(days=1)
            weekday = startDay.weekday()
            day = startDay.day
            format_string += f'## {day} {calendar.day_name[weekday]} ({startDay})\n\n- [ ] \n\n'
    return format_string

def writeHeaders(format_string):
    with open('todo.md', 'a') as f:
        f.write(format_string)

def backupTodo():
    '''
    Backup todo.md file
    Use bash cp command to copy todo.md to backups/{currentdate-time}todo.md.bak
    '''
    current_date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    os.system(f'cp todo.md backups/{current_date}todo.md.bak')
    

def main():
    args = getInputArgs()
    format_string = generateHeaders(
        args.ndays, args.append, parseStartDay(args.startday)
    )
    if args.append:
        backupTodo()
        writeHeaders(format_string)
    else:
        print(format_string)
    

if __name__ == '__main__':
    main()

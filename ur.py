#!/usr/bin/env python3
'''
   OPS435 Assignment 2 - Winter 2020
    Program: ur_tdavis12.py
    Author: "Theodore Davis"
    The python code in this file ur_tdavis12.py is original work written by
    "Theodore Davis". No code in this file is copied from any other source 
    including any person, textbook, or on-line resource except those provided by the course instructor. I have not shared this python file with anyone or anything except for submission for grading.  
    I understand that the Academic Honesty Policy will be enforced and violators will be reported and appropriate action will be taken.
'''
import os 
import sys
import time
from time import strftime
def get_login_rec(login_recs,args):
    '''
    takes a list with an argument and returns a list of users, or hosts requested from the argument
        '''
    
    argument = str(args.list)

    if "user" in argument:
        users = []
        for item in login_recs:
            split = item.split()
            user = split[0]
            if user not in users:
                users.append(user)
        return(users)
    if "host" in argument:
        hosts = []
        for item in login_recs:
            split = item.split()
            host = split[2]
            if host not in hosts:
                hosts.append(host)
        return(hosts)

def read_login_rec(filelist,args):
    '''
    takes a list of files and arguments to return each line of the file in which the user or host is mentioned
    '''
    if isinstance(filelist, str):
        filelist = [filelist]
    if (args.verbose is True) and (args.user is not None):
        print("usage report for user: " + str(args.user))
        print("usage report type: " + str(args.type[0]))
        print("processing usage report for the following: ")
        print("reading login/logout record files " + str(filelist))
    elif (args.verbose is True) and (args.rhost is not None):
        print("usage report for remote host: " + str(args.rhost))
        print("usage report type: " + str(args.type[0]))
        print("processing usage report for the following: ")
        print("reading login/logout record files " + str(filelist))
    elif (args.verbose is True and args.list):
        print("processing usage report for the following: ")
        print("reading login/logout record files " + str(filelist))
    #add the record to a list 
    unprocessed = []
   
    for fileitem in filelist:
            file = open(fileitem,"r")
            unprocessed.extend(file.read().splitlines())

    processed = []
    if args.rhost is not None:
        rhost = str(args.rhost)
        for item in unprocessed:
                if rhost in item:
                        processed.append(item)
    else:
        processed = unprocessed
    processedfinal = []
    if args.user is not None:
        username = str(args.user)
        for item in processed:
                if username in item:
                        processedfinal.append(item)
    else:
            processedfinal = processed
    login_rec = processedfinal
    return login_rec

def finding_difference(split):
    '''
    finding_difference takes a split of lines and returns the time difference between them
    '''
    dictmonth = {"Jan":"1", "Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}   
    startdate_obj = time.strptime(str((' '.join(split[3:8]))))
    enddate_obj = time.strptime(str((' '.join(split[9:14]))))

    nextday = strftime('%d %m %y',enddate_obj)
    nextday = time.strptime(nextday, '%d %m %y')

    prevday_timediff = int(time.mktime(nextday) - time.mktime(startdate_obj))
    nxtday_timediff = int((time.mktime(enddate_obj) - (time.mktime(nextday))))
    return(prevday_timediff,nxtday_timediff)

def cal_daily_usage(login_recs, args):
    '''
    takes the line generated in read_login_rec to calculate the daily usage of the user or host in the argument and then returns a dictionary 
    '''
    
    timedict = {}
    for item in login_recs:
       
        split = item.split()

        startdate_obj = time.strptime(str((' '.join(split[3:8]))))
        enddate_obj = time.strptime(str((' '.join(split[9:14]))))

        dictmonth = {"Jan":"01", "Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}  

        startdate_dy = strftime("%d", startdate_obj)
        enddate_dy = strftime("%d", enddate_obj)

        if  startdate_dy != enddate_dy:
            timedifferences = finding_difference(split)
            prevday = str(split[7]) + " " + dictmonth.get(str(split[4])) + " " + str(split[5])   

            if prevday in timedict:
                newtime = int(timedict[prevday]) + int(timedifferences[0]) - 2
                timedict[prevday] = newtime
            else:
                timedict[prevday] = int(timedifferences[0])

            nxtday = str(split[13]) + " " + dictmonth.get(str(split[10])) + " " + str(split[11])
            if nxtday in timedict:
                newtime = int(timedict[nxtday]) + int(timedifferences[1])
                timedict[nxtday] = newtime
            else:
                timedict[nxtday] = int(timedifferences[1])
        else:
            month = str(split[4])
            month = dictmonth.get(month)
            dateobject = str(split[7]) + " " + month + " " + str(split[5])

            timediff = str(int((time.mktime(enddate_obj) - time.mktime(startdate_obj))))
            if dateobject in timedict:
                oldtime = timedict[dateobject]
                newtime = int(timediff) + int(oldtime)
                timedict[dateobject] = newtime
            else:
                timedict[dateobject] = str(timediff)
    return(timedict)


def cal_weekly_usage(login_recs,args):
    '''
    takes the lines generated in read_login_rec to calculates the weekly usage of the user or host in the argument and returns a dictionary
    '''
    timedict = {}

    for item in login_recs:
        split = item.split()
        startdate_obj = time.strptime(str((' '.join(split[3:8]))))
        enddate_obj = time.strptime(str((' '.join(split[9:14]))))

        startdate_wk = strftime("%W", startdate_obj)
        enddate_wk = strftime("%W", enddate_obj)

        startdate_dy = strftime("%d", startdate_obj)
        enddate_dy = strftime("%d", enddate_obj)
        recorder = 0
        if startdate_dy != enddate_dy:
            recorder = 1
            timedifferences = finding_difference(split)
            if startdate_wk != enddate_wk:
                prevweek = str(split[13]) + " " + str(startdate_wk)
                if prevweek in timedict:
                    newtime = int(timedict[prevweek]) + int(timedifferences[0]) - recorder
                    timedict[prevweek] = newtime
                else:
                    timedict[prevweek] = int(timedifferences[0])
                nxtwk = str(split[13]) + " " + str(enddate_wk)
                if nxtwk in timedict:
                    newtime = int(timedict[nxtwk]) + int(timedifferences[1])
                    timedict[nxtwk] = newtime
                else:
                    timedict[nxtwk] = int(timedifferences[1])
        dateobject = str(split[13]) + " " + str(startdate_wk)
        timediff = int(time.mktime(enddate_obj) - time.mktime(startdate_obj)) 
        if dateobject in timedict:
            newtime = timediff + timedict[dateobject] - recorder
            timedict[dateobject] = newtime
        else:
            timedict[dateobject] = timediff
    return(timedict)

def cal_monthly_usage(login_recs, args):
    '''
    takes the lines generated in read_login_rec to calculate the monthly usage of user or host in the argument and returns a dictionary
    '''
    timedict = {}
    for item in login_recs:
        split = item.split()
        dictmonth = {"Jan":"1", "Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}
        startdate_obj = time.strptime(str((' '.join(split[3:8]))))
        enddate_obj = time.strptime(str((' '.join(split[9:14]))))
        startdate_dy = strftime("%d", startdate_obj)
        enddate_dy = strftime("%d", enddate_obj)
        startdate_mn = strftime("%m", startdate_obj)
        enddate_mn = strftime("%m", enddate_obj)
        recorder = 0
        if startdate_dy != enddate_dy:
            recorder = 1
            timedifferences = finding_difference(split)
            if startdate_mn != enddate_mn:
                prevmonth = str(split[7]) + " " + startdate_mn
                if prevmonth in timedict:
                    newtime = int(timedict[prevmonth]) + int(timedifferences[0]) - recorder
                    timedict[prevweek] = newtime
                else:
                    timedict[prevweek] = int(timedifferences[0])
                nxtmonth = str(split[13]) + " " + enddate_mn
                if nxtmonth in timedict:
                    newtime = int(timedict[nxtmonth]) + int(timedifferences[1])
                    timedict[nxtmonth] = newtime
                else:
                    timedict[nxtmonth] = int(timedifferences[1])
                break
        dateobject = str(split[13]) + " " + enddate_mn
        timediff = int(time.mktime(enddate_obj) - time.mktime(startdate_obj))
        if dateobject in timedict:
            newtime = timediff + timedict[dateobject] - recorder
            timedict[dateobject] = newtime
        else:
            timedict[dateobject] = timediff
    return(timedict)

def print_statement(dictionary,usertype,subject):
    '''
    print_statement takes the information provided and prints a statement realting the request by the user
    '''
    line = str(usertype) + " Usage Report for " + str(subject)
    eq = len(line)
    print(line)
    print ("=" * eq)  
    if str(args.type) == "daily":
        print("Date     ","Usage in Seconds")
        print()
    if str(args.type) == "weekly":
        print("Week #   ","Usage in Seconds")
        print()
    if str(args.type) == "monthly":
        print("Month    ","Usage in Seconds")
        print()

    total = 0
    for key, value in sorted(dictionary.items(),reverse=True):
        print(str(key),"    " + str(value))
        total = total + int(value)
    print("Total    ","    " + str(total))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(epilog="Copyright 2020 - Theodore Davis", description="Usage Report based on the last command")
    parser.add_argument("-l","--list", choices=("user","host"), help="generate user name or remote host IP from the given files")
    parser.add_argument("-r","--rhost", help="usage report for the given remote host IP")
    parser.add_argument("-t","--type", choices=("daily","weekly","monthly"), help="type of report: daily, weekly, and monthly")
    parser.add_argument("-u", "--user", help="usage report for the given user name")
    parser.add_argument("-v", "--verbose", action="store_true", help="tune on output verbosity")
    parser.add_argument("F", nargs="+", help="list of files to be processed")
    args = parser.parse_args()

    if args is not None:
        if args.list is not None:
            subject = str(sys.argv[2])
            args.file = [str(sys.argv[3])]
            if args.verbose is True:
                print("Files to be processed: ['" + str(args.list[1]) + "']")
                print("Type of args for files <class 'list'>")
            login_rec = read_login_rec(args.file,args)
            userhost_rec = get_login_rec(login_rec,args)
            userhost_rec.sort()
            if args.verbose is True:
                print("Generating list for " + subject)
            item = (str(args.list)).capitalize()  
            line = str(item) + " list for "
            eq = len(line)
            print(line + " " + str(args.F).strip("'[]'"))
            print("=" * eq)
            for user_or_host in userhost_rec:
                print(user_or_host)

        if args.rhost or args.user is not None:
            if args.verbose is True:
                placeholder = []
                placeholder.append(str(sys.argv[5]))
                print("Files to be processed: " + str(placeholder))
                print("Type of args for files " + str(type(placeholder)))
            args.file = [str(sys.argv[5])]
            login_rec = read_login_rec(args.file,args)
            
            schedule = str(sys.argv[4])
            subject = str(sys.argv[2])

            if "daily" in schedule:
                daily_dict  = cal_daily_usage(login_rec,args)
                print_statement(daily_dict,"Daily",subject)

            if "weekly" in schedule:
                weekly_dict = cal_weekly_usage(login_rec,args)
                print_statement(weekly_dict,"Weekly",subject)


            if "monthly" in schedule:
                monthly_dict = cal_monthly_usage(login_rec,args)
                print_statement(monthly_dict,"Monthly",subject)


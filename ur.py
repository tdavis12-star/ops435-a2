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
    This takes a list with an argument and returns a list of users, or hosts requested from the argument
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
    takes a list of files and arguments to return each line of the file in which the user and host are mentioned
    '''
    if logon_reading(filelist, str):
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
    unProcessed = []
   
    for file_item in filelist:
            file = open(file_item,"r")
            unProcessed.extend(file.read().splitlines())

    processed = []
    if args.rhost is not None:
        rhost = str(args.rhost)
        for item in unProcessed:
                if rhost in item:
                        processed.append(item)
    else:
        processed = unProcessed
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

def betweendays(split):
    '''
      split of lines and returns the time difference between them
    '''
    month_dict = {"Jan":"1", "Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}   
    date_started = time.strptime(str((' '.join(split[3:8]))))
    date_end = time.strptime(str((' '.join(split[9:14]))))

    nextday = strftime('%d %m %y',date_end)
    nextday = time.strptime(nextday, '%d %m %y')

    prev_day_timediff = int(time.mktime(nextday) - time.mktime(date_started))
    nt_day_timediff = int((time.mktime(date_end) - (time.mktime(nextday))))
    return(prev_day_timediff,nt_day_timediff)

def cal_daily_usage(login_recs, args):
    '''
    takes the line generated in read_login_rec to calculate the daily usage of the user or host in the argument, then returns a dict  
    '''
    
    time_dict = {}
    for item in login_recs:
       
        split = item.split()

        date_started = time.strptime(str((' '.join(split[3:8]))))
        date_end = time.strptime(str((' '.join(split[9:14]))))

        month_dict = {"Jan":"01", "Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}  

        datestarted_dy = strftime("%d", date_started)
        enddate_dy = strftime("%d", date_end)

        if  datestarted_dy != enddate_dy:
            time_change = betweendays(split)
            prev_day = str(split[7]) + " " + month_dict.get(str(split[4])) + " " + str(split[5])   

            if prev_day in time_dict:
                time_update = int(time_dict[prev_day]) + int(time_change[0]) - 2
                time_dict[prev_day] = time_update
            else:
                time_dict[prev_day] = int(time_change[0])

            nt_day = str(split[13]) + " " + month_dict.get(str(split[10])) + " " + str(split[11])
            if nt_day in time_dict:
                time_update = int(time_dict[nt_day]) + int(time_change[1])
                time_dict[nt_day] = time_update
            else:
                time_dict[nt_day] = int(time_change[1])
        else:
            month = str(split[4])
            month = month_dict.get(month)
            obj_date = str(split[7]) + " " + month + " " + str(split[5])

            timediff = str(int((time.mktime(date_end) - time.mktime(date_started))))
            if obj_date in time_dict:
                oldtime = time_dict[obj_date]
                time_update = int(timediff) + int(oldtime)
                time_dict[obj_date] = time_update
            else:
                time_dict[obj_date] = str(timediff)
    return(time_dict)


def cal_weekly_usage(login_recs,args):
    '''
    This will take the lines generated in read_login_rec to calculate the weekly usage of the user or host in the argument and returns a dict with the and the total time for the week
    '''
    time_dict = {}

    for item in login_recs:
        split = item.split()
        date_started = time.strptime(str((' '.join(split[3:8]))))
        date_end = time.strptime(str((' '.join(split[9:14]))))

        startdate_wk = strftime("%W", date_started)
        enddate_wk = strftime("%W", date_end)

        datestarted_dy = strftime("%d", date_started)
        enddate_dy = strftime("%d", date_end)
        keeper_time = 0
        if datestarted_dy != enddate_dy:
            keeper_time = 1
            time_change = betweendays(split)
            if startdate_wk != enddate_wk:
                prev_week = str(split[13]) + " " + str(startdate_wk)
                if prev_week in time_dict:
                    time_update = int(time_dict[prev_week]) + int(time_change[0]) - keeper_time
                    time_dict[prev_week] = time_update
                else:
                    time_dict[prev_week] = int(time_change[0])
                nt_week = str(split[13]) + " " + str(enddate_wk)
                if nt_week in time_dict:
                    time_update = int(time_dict[nt_week]) + int(time_change[1])
                    time_dict[nt_week] = time_update
                else:
                    time_dict[nt_week] = int(time_change[1])
        obj_date = str(split[13]) + " " + str(startdate_wk)
        timediff = int(time.mktime(date_end) - time.mktime(date_started)) 
        if obj_date in time_dict:
            time_update = timediff + time_dict[obj_date] - keeper_time
            time_dict[obj_date] = time_update
        else:
            time_dict[obj_date] = timediff
    return(time_dict)

def cal_monthly_usage(login_recs, args):
    '''
    takes the lines generated in read_login_rec to calculate the monthly usage of user or host in the argument and returns a dict with the month and the total for the month
    '''
    time_dict = {}
    for item in login_recs:
        split = item.split()
        month_dict = {"Jan":"1", "Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}
        date_started = time.strptime(str((' '.join(split[3:8]))))
        date_end = time.strptime(str((' '.join(split[9:14]))))
        datestarted_dy = strftime("%d", date_started)
        enddate_dy = strftime("%d", date_end)
        startdate_mn = strftime("%m", date_started)
        enddate_mn = strftime("%m", date_end)
        keeper_time = 0
        if datestarted_dy != enddate_dy:
            keeper_time = 1
            time_change = betweendays(split)
            if startdate_mn != enddate_mn:
                prvmonth = str(split[7]) + " " + startdate_mn
                if prvmonth in time_dict:
                    time_update = int(time_dict[prvmonth]) + int(time_change[0]) - keeper_time
                    time_dict[prev_week] = time_update
                else:
                    time_dict[prev_week] = int(time_change[0])
                nt_month = str(split[13]) + " " + enddate_mn
                if nt_month in time_dict:
                    time_update = int(time_dict[nt_month]) + int(time_change[1])
                    time_dict[nt_month] = time_update
                else:
                    time_dict[nt_month] = int(time_change[1])
                break
        obj_date = str(split[13]) + " " + enddate_mn
        timediff = int(time.mktime(date_end) - time.mktime(date_started))
        if obj_date in time_dict:
            time_update = timediff + time_dict[obj_date] - keeper_time
            time_dict[obj_date] = time_update
        else:
            time_dict[obj_date] = timediff
    return(time_dict)

def print_statement(dict,usertype,subj):
    '''
    print_statement takes the information provided and prints a statement realting the request by the user
    '''
    line = str(usertype) + " Usage Report for " + str(subj)
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
    for key, value in sorted(dict.items(),reverse=True):
        print(str(key),"    " + str(value))
        total = total + int(value)
    print("Total    ","    " + str(total))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(epilog="Copyright 2020 - Tdavis12", description="Usage Report based on the last command")
    parser.add_argument("-l","--list", choices=("user","host"), help="generate user name or remote host IP from the given files")
    parser.add_argument("-r","--rhost", help="usage report for the given remote host IP")
    parser.add_argument("-t","--type", choices=("daily","weekly","monthly"), help="type of report: daily, weekly, and monthly")
    parser.add_argument("-u", "--user", help="usage report for the given user name")
    parser.add_argument("-v", "--verbose", action="store_true", help="tune on output verbosity")
    parser.add_argument("F", nargs="+", help="list of files to be processed")
    args = parser.parse_args()

    if args is not None:
        if args.list is not None:
            subj = str(sys.argv[2])
            args.file = [str(sys.argv[3])]
            if args.verbose is True:
                print("Files to be processed: ['" + str(args.list[1]) + "']")
                print("Type of args for files <class 'list'>")
            login_rec = read_login_rec(args.file,args)
            userhost_rec = get_login_rec(login_rec,args)
            userhost_rec.sort()
            if args.verbose is True:
                print("Generating list for " + subj)
            item = (str(args.list)).capitalize()  
            line = str(item) + " list for "
            eq = len(line)
            print(line + " " + str(args.F).strip("'[]'"))
            print("=" * eq)
            for user_or_host in userhost_rec:
                print(user_or_host)

        if args.rhost or args.user is not None:
            if args.verbose is True:
                recorder = []
                recorder.append(str(sys.argv[5]))
                print("Files to be processed: " + str(recorder))
                print("Type of args for files " + str(type(recorder)))
            args.file = [str(sys.argv[5])]
            login_rec = read_login_rec(args.file,args)
            
            availability = str(sys.argv[4])
            subj = str(sys.argv[2])

            if "daily" in availability:
                daily_dict  = cal_daily_usage(login_rec,args)
                print_statement(daily_dict,"Daily",subj)

            if "weekly" in availability:
                weekly_dict = cal_weekly_usage(login_rec,args)
                print_statement(weekly_dict,"Weekly",subj)


            if "monthly" in availability:
                monthly_dict = cal_monthly_usage(login_rec,args)
                print_statement(monthly_dict,"Monthly",subj)


from get_cursor import GetDATAWCursor


def get_schedule_list(quarter, cursor):
    """Output a list of course, room, day, and time entries"""
    cursor.execute(
        "SELECT COURSE_NUMBER, S_SCHEDULE.CRN, ROOM, BEGIN_TIME, " +
        "END_TIME, DAYS " +
        "FROM S_SCHEDULE, S_MEETING " +
        "WHERE S_SCHEDULE.CRN = S_MEETING.CRN " +
        "AND S_SCHEDULE.TERM = S_MEETING.TERM " +
        "AND (S_MEETING.TERM='" + str(quarter) + "' " +
        "AND BUILDING='CF' " +
        "AND ROOM IN ('162','164','404','405','412','414','416','418') " +
        "AND ACTUAL_ENROLL > 0)")
    return cursor.fetchall()


def mil_to_us(time):
    """Convert military time to 12 hour time"""
    if time > 1259:
        ret = str(time/100-12)
    elif time < 100:
        ret = "12"
    else:
        ret = str(time/100)
    if time % 100 < 10:
        ret += ":0" + str(time % 100)
    else:
        ret += ":" + str(time % 100)
    if time > 1159:
        ret += ' PM'
    else:
        ret += ' AM'
    return ret


def schedule_list_to_mediawiki_table(schedule_list):
    """Convert a schedule list to a mediawiki style schedule table"""
    days = ['M', 'T', 'W', 'R', 'F']
    days_dict = {
        'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday',
        'F': 'Friday'}
    hours = range(800, 1900, 100)
    ret = ""
    occupied_rooms = list(set([entry[2] for entry in schedule_list]))
    occupied_rooms.sort()
    for room in occupied_rooms:
        # Output the room header
        ret += '{| class="wikitable" style="text-align:center;'
        ret += ' border-style:solid; width:100%;"\n'
        ret += '|+ CF' + room + '\n|----\n'
        # Output the days column header
        ret += '!scope="col", align="right"| Time\n'
        for day in days:
            ret += '!scope="col"| ' + days_dict[day] + '\n'
        ret += '!scope="col", align="left"| Time\n|----\n'
        # Build the lines for each rooms hour and day entry
        for hour in hours:
            ret += '!scope="row", align="right"|' + str(mil_to_us(hour)) + '\n'
            for day in days:
                # If there is a class in this room, this day, and this hour
                current = [a for a in schedule_list if
                           a[2] == room and
                           int(a[3]) <= hour
                           and int(a[4]) > hour
                           and a[5] == day]
                following = [a for a in schedule_list if
                             a[2] == room and
                             int(a[3]) <= hour+100
                             and int(a[4]) > hour+100
                             and a[5] == day]
                previous = [a for a in schedule_list if
                            a[2] == room and
                            int(a[3]) <= hour-100
                            and int(a[4]) > hour-100
                            and a[5] == day]
                if current:
                    if following and (current[0][0],
                                      current[0][1]) == (following[0][0],
                                                         following[0][1]):
                        ret += '| rowspan=2, style="border-style:solid;" |'
                        ret += current[0][0] + '-' + current[0][1] + '\n'
                    elif previous and (current[0][0],
                                       current[0][1]) != (previous[0][0],
                                                          previous[0][1]):
                        ret += '| style="border-style:solid;" |'
                        ret += current[0][0] + '-' + current[0][1] + '\n'
                else:
                    ret += '| &nbsp;\n'
            ret += '!scope="row", align="left"|' + str(mil_to_us(hour))
            ret += '\n|----\n'
        ret += '|}\n'
    return ret


def schedule_list_to_csv(schedule_list):
    """Convert a schedule list to a csv schedule"""
    # Output csv style schedule
    days = ['M', 'T', 'W', 'R', 'F']
    days_dict = {
        'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday',
        'F': 'Friday'}
    hours = range(800, 1900, 100)
    ret = ""
    occupied_rooms = set([entry[2] for entry in schedule_list])
    for room in occupied_rooms:
        # Output the room header
        ret += 'CF' + room + 6*','
        ret += '\n,'
        # Output the days column header
        for day in days:
            ret += days_dict[day] + ','
        ret += '\n'
        # Build the lines for each rooms hour and day entry
        for hour in hours:
            ret += str(hour) + ","
            for day in days:
                # If there is a class in this room, this day, and this hour
                occupied = [a for a in schedule_list if
                            a[2] == room and
                            int(a[3]) <= hour
                            and int(a[4]) > hour
                            and a[5] == day]
                if occupied:
                    ret += occupied[0][0] + "-" + occupied[0][1]
                    ret += ","
                    ret += str(hour) + "\n"
        ret += ','*7 + '\n'
    return ret


def main():
    quarter = raw_input(("Enter the quarter you want the schedule for (eg. "
                         "for Winter 2011 enter, 201110): "))
    sched = schedule_list_to_mediawiki_table(
        get_schedule_list(quarter, GetDATAWCursor()))
    fname = str(quarter)+".schedule.mediawiki.txt"
    print("Writing output to " + fname)
    with open(fname, "wb") as f:
        f.write(sched)


if __name__ == "__main__":
    main()

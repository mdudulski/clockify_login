from datetime import date
from clockify_api_handler import ClockifyApiHandler
from date_calculate import getlastworkingday, checkifworkingday
from config import email

def main():
    clockify_api_handler = ClockifyApiHandler()
    today = date.today()

    print('Czy dzisiaj jest dzień pracujący ? ' + str(checkifworkingday(today)))
    print('Jaki jest dzień do pobrania danych ?' + str(getlastworkingday(today)))

    if checkifworkingday(today) is True:
        lastworkingday = getlastworkingday(today)
        request_json = clockify_api_handler.clockify_get_time_entries_by_days \
            (email=email
             , start_date=lastworkingday
             , end_date=lastworkingday)

        for task_info in request_json:
            description = task_info['description']
            project_id = task_info['projectId']
            task_id = task_info['taskId']
            start_datetime = today.strftime('%Y-%m-%d')
            end_datetime = today.strftime('%Y-%m-%d')
            clockify_api_handler.clockify_add_new_time_entry(start_datetime
                                                             , end_datetime
                                                             , description
                                                             , project_id
                                                             , task_id)


if __name__ == "__main__":
    # execute only if run as a script
    main()

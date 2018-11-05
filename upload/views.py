from django.shortcuts import render
from upload.models import UploadForm,UploadCsv,ConvertedFile
from django.http import HttpResponseRedirect
from django.urls import reverse
import csv
from django.core.files import File
from datetime import date, timedelta, datetime
from dateutil import relativedelta
from django.contrib import messages

def uploader(request):
    if request.method=="POST":
        file_form = UploadForm(request.POST, request.FILES)
        if file_form.is_valid():
            file_form.save()

            #Get latest upload name
            new_upload=UploadCsv.objects.latest('pk')
            print( 'NEWEST FILE: '+ str(new_upload))

        with open('media/'+str(new_upload),'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            time_stamp = datetime.now().strftime('%Y_%m_%d - %I.%M%p')
            next(csv_file)

            with open(f'media/converted/converted_{time_stamp}.csv','w', newline='') as new_file:
                csv_writer = csv.writer(new_file)
                convertedDB = ConvertedFile(name=f'converted_{time_stamp}.csv',path=f'media/converted/converted_{time_stamp}.csv')
                convertedDB.save()

                csv_writer.writerow(['customer_name','customer_phone','customer_email','start_address','end_address','pickup_date','return_date','account_id','service_type','passengers','driver_notes','dispatcher_notes','customer_notes','driver_name','driver_email'])

                # grabbing data from the uploaded csv - parse to variables
                for line in csv_reader:
                    customer_name = line[0]
                    customer_phone = line[1]
                    customer_email = line[2]
                    start_address = line[3]
                    end_address = line[4]
                    pickup_date = line[12]
                    return_date = line[13]
                    pickup_time = line[5]
                    return_time = line[6]
                    account_id = line[7]
                    service_type = line[8]
                    passengers = line[9]
                    weekdays = line[10]
                    round_trip = line[11]
                    driver_notes = line[16]
                    call_number = line[14] #dispatcher notes
                    customer_notes = ''
                    driver_name = ''
                    driver_email = ''
                    dispatcher_notes=line[17]


                    # Parse data for date range algorithm
                    day_choices = []
                    date_list = []
                    parsed_weekdays = weekdays.split('-')
                    for i in parsed_weekdays:
                        day_choices.append(i)
                    print('Day Choices: ', day_choices)

                    # Loop this dictionary with STRs from day_choices, if match, feed into date algorithm
                    day_codes = {'M' : 0, 'T' : 1, 'W' : 2, 'TH' : 3, 'F' : 4, 'SAT' : 5, 'SUN' : 6}

                    print('pickup_date: ',pickup_date)
                    sd = pickup_date.split('-') # pickup_date is the start date in csv
                    print('sd: ',sd)
                    sd_year = int(sd[0])
                    sd_month = int(sd[1])
                    sd_day = int(sd[2])
                    ed = return_date.split('-') # return_date is the end date in csv
                    ed_year = int(ed[0])
                    ed_month = int(ed[1])
                    ed_day = int(ed[2])
                    d1 = date(sd_year,sd_month,sd_day) # Start date
                    d2 = date(ed_year,ed_month,ed_day) # End date
                    print('Start date: ',d1)
                    print('End date: ',d2)

                    delta = d2 - d1 #timedelta - time between two times

                    ### Date algorithm ###
                    for i in range(delta.days + 1):
                        x = d1 + timedelta(i) # loop dates

                        parsed_day_codes = [] # date numbers that correspond to the date.day method in datetime
                        for i in day_choices:
                            for key, value in day_codes.items():
                                if i == key:
                                    parsed_day_codes.append(value)

                        # match the number of days
                        for i in parsed_day_codes:
                            if x.weekday() == i:
                                print(x)
                                date_list.append(str(x))
                    print('Datelist: ',date_list)
                    print(parsed_day_codes)
                    print('SOMETHING IS HAPPENING')

                    # Write to file
                    # Header

                    for iterdate in date_list:
                        print(iterdate)
                        if round_trip == 'y' or 'Y':
                            csv_writer.writerow([customer_name, customer_phone, customer_email, start_address, end_address, iterdate + ' ' + pickup_time,'', account_id, service_type, passengers, driver_notes  + call_number , dispatcher_notes,'','','' ])
                            csv_writer.writerow([customer_name, customer_phone, customer_email, end_address, start_address, iterdate + ' ' + return_time, '', account_id, service_type, passengers, driver_notes + call_number, dispatcher_notes,'','','' ])
                        elif round_trip == 'n' or 'N':
                            csv_writer.writerow([customer_name, customer_phone, customer_email, start_address, end_address, iterdate + ' ' + pickup_time, iterdate + ' ' + return_time, account_id, service_type, passengers,driver_notes + ' | ' + call_number, dispatcher_notes,'','',''])
                        else:
                            messages.warning(request, 'Something is wrong with a round trip cell in the original file. Please fix it.')

            messages.success(request, 'File successfully converted! You may need to refresh the page.')
            return HttpResponseRedirect(reverse('uploader'))


    else:
        file_form=UploadForm()
        # csv_files=UploadCsv.objects.all().order_by('-upload_date')
        csv_files=ConvertedFile.objects.all().order_by('-upload_date')
        return render(request,'upload/uploader.html',{'file_form':file_form,'csv_files':csv_files})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from . import forms
from .models import FormBasic, Reocurring
from datetime import date, timedelta, datetime
from dateutil import relativedelta
from django.contrib import messages
import datetime
import csv
import googlemaps
import math

# Create your views here.

@login_required(login_url='/accounts/login')
def book_view(request):
    if request.method == 'POST':
        form = forms.CreateBooking(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            #save booking to DB
            instance = form.save(commit=False)
            instance.author= request.user
            instance.save()
            messages.success(request, 'Form Submission Successful')
            return redirect('rides:book') # Make a congratulations app
        else:
            return redirect('rides:book')
    else:
        form = forms.CreateBooking()
        return render(request, 'rides/form.html',{'form': form})

@login_required(login_url='/accounts/login')
def universal_form(request):
    if request.method == 'POST':
        form = forms.UniversalForm(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            #save booking to DB
            instance = form.save(commit=False)
            instance.author= request.user
            instance.save()
            messages.success(request, 'Form Submission Successful')
            return redirect('rides:universal_form') # Make a congratulations app
        else:
            return redirect('rides:universal_form')
    else:
        form = forms.UniversalForm()
        return render(request, 'rides/universal_rides.html',{'form': form})

@login_required(login_url='/accounts/login')
def book_view_reocurring(request):
    next_month = datetime.date.today() + relativedelta.relativedelta(months=1)
    next_month = next_month.strftime("%B %Y")

    if request.method == 'POST':
        form = forms.ReocurringBooking(request.POST,request.FILES)
        print(form.errors)
        if form.is_valid():
            #save booking to DB
            instance = form.save(commit=False)
            instance.author= request.user
            instance.save()
            messages.success(request, 'Form Submission Successful')
            return redirect('rides:multi')
        else:
            return redirect('rides:multi')
    else:
        form = forms.ReocurringBooking()
        return render(request, 'rides/reocurring.html',{'form': form, 'next_month' : next_month})

@user_passes_test(lambda u: u.is_superuser)
def download_page(request,pk=None):
    one_off = FormBasic.objects.all().order_by('-time_stamp')
    reocurring = Reocurring.objects.all().order_by('-time_stamp')
    return render(request, 'rides/download.html', {'one_off' : one_off, 'reocurring' : reocurring})

@login_required(login_url='/accounts/login')
def one_off_dr(request, pk=None):
    if pk:
        print('returned primary key: ',pk)
        db = FormBasic.objects.get(pk=pk)
        fname = db.patient_first_name
        lname = db.patient_last_name
        phone = db.patient_phone
        start_address = db.pickup_address
        end_address = db.destination_address
        pickup_date = (db.appointment_date + ' ' + db.pickup_time)
        return_time = (db.appointment_date + ' ' + db.return_time)
        return_date = ''
        account_id = db.account_number
        service_type = db.service_type
        passengers = db.number_of_passengers
        customer_notes = ''
        driver_name = ''
        driver_notes = ''
        dispatcher_notes = db.call_number
        driver_email = ''

        # Make dl true if dashride button is clicked and user created
        db.downloaded = True
        db.dl_user = str(request.user)
        db.dl_time = datetime.datetime.now().strftime('%m-%d-%Y | %I:%M%p')
        # db.dl_user = str(request.user)
        db.save()


        # Create CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dashride-upload.csv"'

        writer = csv.writer(response)
        writer.writerow(['customer_name','customer_phone','customer_email','start_address','end_address','pickup_date','return_date','account_id','service_type','passengers','driver_notes','dispatcher_notes','customer_notes','driver_name','driver_email'])

        if db.round_trip == True:
            writer.writerow([fname + ' ' + lname,phone,'', start_address, end_address, pickup_date, return_date, account_id, service_type,passengers,driver_notes,dispatcher_notes,customer_notes,driver_name,driver_email])
            writer.writerow([fname + ' ' + lname,phone,'', end_address, start_address, return_time, return_date, account_id, service_type,passengers,driver_notes,dispatcher_notes,customer_notes,driver_name,driver_email])
            return response

        else:
            writer.writerow([fname + ' ' + lname,phone,'', start_address, end_address, pickup_date, return_date, account_id, service_type,passengers,driver_notes,dispatcher_notes,customer_notes,driver_name,driver_email])
            return response


    else:
        print('Something went wrong')
        one_off = FormBasic.objects.all().order_by('-time_stamp')
        reocurring = Reocurring.objects.all().order_by('-time_stamp')
        return render(request, 'rides/download.html', {'one_off' : one_off, 'reoccuring' : reocurring})

@login_required(login_url='/accounts/login')
def one_off_oa(request, pk=None):
    if pk:
        print('returned primary key: ', pk)
        print('ONE OFF OA TRIGGERED')
        db = FormBasic.objects.get(pk=pk)
        fname = db.patient_first_name
        lname = db.patient_last_name
        phone = db.patient_phone
        male_sex = ''
        female_sex = ''
        patient_birthdate = db.patient_birthdate
        start_address = db.pickup_address
        end_address = db.destination_address
        pickup_time = db.pickup_time
        return_time = db.return_time
        appointment_date = db.appointment_date
        account_id = db.account_number
        service_type = db.service_type
        passengers = db.number_of_passengers
        dispatcher_notes = db.call_number
        patientMN = db.patient_med_number
        SCFHP_ID = '24077'
        current_date = db.time_stamp.date()
        npi_number = '1699146175'
        fed_tax_ssn = 'TAX NUMBER'
        vendor_signature = 'Thom Gazay'
        round_trip = db.round_trip

        if db.gender == 'Male':
            male_sex = 'X'
        else:
            female_sex = 'X'

        # Google Maps API Distance Matrix : Solve Miles
        gmaps = googlemaps.Client(key='AIzaSyDoDkPiC9_J8DXevCGej4NPX32uB9ThjYU')
        my_distance = gmaps.distance_matrix(start_address, end_address,units='imperial')['rows'][0]['elements'][0]
        miles = my_distance['distance']['text'].replace('mi','')
        miles = math.ceil(float(miles))
        price_policy = (3 * miles + 25) # CHARGES $25 per pickup, $3 per mile
        charges = price_policy
        units = miles
        print('Miles: ', miles)

        # Create CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="office-ally-upload.csv"'

        writer = csv.writer(response,delimiter='\t')

        if round_trip == False:
            # Write DB data to TSV
            writer.writerow(['','Santa Clara Family Health Plan', SCFHP_ID,'','','','','','','','X','','','','','',patientMN ,
            lname, fname,'', patient_birthdate, male_sex, female_sex, lname, fname, '', start_address, '','','', phone,'self',
            '','','', start_address,'','','', phone,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','',
            '','X','SIGNATURE ON FILE', current_date,'SIGNATURE ON FILE', current_date,'','','','','','','','','','','','','','','G8220',
            '','','','','','','','','','','','','','','', current_date,current_date,'99','','A0130','','','','','1', charges, units,'','NPI',
            npi_number,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''
            ,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','', fed_tax_ssn,'X'
            '','X','', 'X', '', charges, charges, current_date, vendor_signature, current_date,'','','','','','','','','','','','','JustGo Brokerage Inc',
            '545 W Hacienda Ave Suite 101', 'Campbell','CA','95008','Campbell CA 95008','4083181573', npi_number,''])
            return response
        else:
            count = 0
            while count < 2:
                print(count)
                # Write DB data to TSV
                writer.writerow(['','Santa Clara Family Health Plan', SCFHP_ID,'','','','','','','','X','','','','','',patientMN ,
                lname, fname,'', patient_birthdate, male_sex, female_sex, lname, fname, '', start_address, '','','', phone,'self',
                '','','', start_address,'','','', phone,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','',
                '','X','SIGNATURE ON FILE', current_date,'SIGNATURE ON FILE', current_date,'','','','','','','','','','','','','','','G8220',
                '','','','','','','','','','','','','','','', current_date,current_date,'99','','A0130','','','','','1', charges, units,'','NPI',
                npi_number,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''
                ,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','', fed_tax_ssn,'X'
                '','X','', 'X', '', charges, charges, current_date, vendor_signature, current_date,'','','','','','','','','','','','','JustGo Brokerage Inc',
                '545 W Hacienda Ave Suite 101', 'Campbell','CA','95008','Campbell CA 95008','4083181573', npi_number,''])
                count += 1
            return response

    else:
        print('Something went wrong')
        one_off = FormBasic.objects.all().order_by('-time_stamp')
        reocurring = Reocurring.objects.all().order_by('-time_stamp')
        print('Problem with OA view code somewhere')
        return render(request, 'rides/download.html', {'one_off' : one_off, 'reocurring' : reocurring})

@login_required(login_url='/accounts/login')
def reocurring_dr(request, pk=None):

    if pk:
        db = Reocurring.objects.get(pk=pk)
        print('returned primary key: ', pk)
        account_number = db.account_number
        call_number = db.call_number
        service_type = db.service_type
        fname = db.patient_first_name
        lname = db.patient_last_name
        phone = db.patient_phone
        birthdate = db.patient_birthdate
        med_num = db.patient_med_number
        num_pass = db.number_of_passengers
        pickup_address = db.pickup_address
        destination_address = db.destination_address
        pickup_time = db.pickup_time
        return_time = db.return_time
        start_date = db.start_date
        end_date = db.end_date
        round_trip = db.round_trip
        day_choices = []
        for i in db.weekdays:
            day_choices.append(i)
        date_list = []

        # Make dl true if dashride button is clicked and user created
        db.downloaded = True
        db.dl_user = str(request.user)
        db.dl_time = datetime.datetime.now().strftime('%m-%d-%Y | %I:%M%p')
        # db.dl_user = str(request.user)
        db.save()

        # Loop this dictionary with STRs from day_choices, if match, feed into date algorithm
        day_codes = {'Mon' : 0, 'Tue' : 1, 'Wed' : 2, 'Thur' : 3, 'Fri' : 4, 'Sat' : 5, 'Sun' : 6}

        sd = start_date.split('-')
        sd_year = int(sd[0])
        sd_month = int(sd[1])
        sd_day = int(sd[2])
        ed = end_date.split('-')
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

        # Create CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dashride-upload.csv"'

        writer = csv.writer(response)
        writer.writerow(['customer_name','customer_phone','customer_email','start_address','end_address','pickup_date','return_date','account_id','service_type','passengers','driver_notes','dispatcher_notes','customer_notes','driver_name','driver_email'])

        for iterdate in date_list:
            if db.round_trip == True:
                writer.writerow([fname + ' ' + lname, phone, '', pickup_address, destination_address, iterdate + ' ' + pickup_time, '', account_number, service_type, num_pass, '', call_number,'','','' ])
                writer.writerow([fname + ' ' + lname, phone, '', destination_address, pickup_address, iterdate + ' ' + return_time, '', account_number, service_type, num_pass, '', call_number,'','','' ])
            else:
                writer.writerow([fname + ' ' + lname, phone, '', pickup_address, destination_address, iterdate + ' ' + pickup_time, '', account_number, service_type, num_pass, '', call_number,'','','' ])
        return response

    else:
        one_off = FormBasic.objects.all().order_by('-time_stamp')
        reocurring = Reocurring.objects.all().order_by('-time_stamp')
        return render(request, 'rides/download.html', {'one_off' : one_off, 'reocurring' : reocurring})

@login_required(login_url='/accounts/login')
def reocurring_oa(request, pk=None):
    if pk:
        print('returned primary key: ', pk)
        print('Reocurring OA TRIGGERED')
        db = Reocurring.objects.get(pk=pk)
        fname = db.patient_first_name
        lname = db.patient_last_name
        phone = db.patient_phone
        male_sex = ''
        female_sex = ''
        patient_birthdate = db.patient_birthdate
        start_address = db.pickup_address
        end_address = db.destination_address
        pickup_time = db.pickup_time
        return_time = db.return_time
        start_date = db.start_date
        end_date = db.end_date
        account_id = db.account_number
        service_type = db.service_type
        passengers = db.number_of_passengers
        dispatcher_notes = db.call_number
        patientMN = db.patient_med_number
        SCFHP_ID = '24077'
        current_date = db.time_stamp.date()
        npi_number = '1699146175'
        fed_tax_ssn = 'INPUT TAX NUMBER'
        vendor_signature = 'Thom Gazay'
        round_trip = db.round_trip
        if db.gender == 'Male':
            male_sex = 'X'
        else:
            female_sex = 'X'

        # Google Maps API Distance Matrix : Solve Miles
        gmaps = googlemaps.Client(key='AIzaSyDoDkPiC9_J8DXevCGej4NPX32uB9ThjYU')
        my_distance = gmaps.distance_matrix(start_address, end_address,units='imperial')['rows'][0]['elements'][0]
        miles = my_distance['distance']['text'].replace('mi','')
        miles = math.ceil(float(miles))
        price_policy = (3 * miles + 25) # CHARGES $25 per pickup, $3 per mile
        charges = price_policy
        units = miles
        print('Miles: ', miles)

        # DATES PROCESSING
        day_choices = []
        for i in db.weekdays:
            day_choices.append(i)
        date_list = []

        # Loop this dictionary with STRs from day_choices, if match, feed into date algorithm
        day_codes = {'Mon' : 0, 'Tue' : 1, 'Wed' : 2, 'Thur' : 3, 'Fri' : 4, 'Sat' : 5, 'Sun' : 6}

        sd = start_date.split('-')
        sd_year = int(sd[0])
        sd_month = int(sd[1])
        sd_day = int(sd[2])
        ed = end_date.split('-')
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


        # # Create CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="office-ally-upload.csv"'

        writer = csv.writer(response,delimiter='\t')

        if round_trip == False:
            # Write DB data to TSV
            for iterdate in date_list:
                writer.writerow(['','Santa Clara Family Health Plan', SCFHP_ID,'','','','','','','','X','','','','','',patientMN ,
                lname, fname,'', patient_birthdate, male_sex, female_sex, lname, fname, '', start_address, '','','', phone,'self',
                '','','', start_address,'','','', phone,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','',
                '','X','SIGNATURE ON FILE', current_date,'SIGNATURE ON FILE', current_date,'','','','','','','','','','','','','','','G8220',
                '','','','','','','','','','','','','','','', iterdate,iterdate,'99','','A0130','','','','','1', charges, units,'','NPI',
                npi_number,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''
                ,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','', fed_tax_ssn,'X'
                '','X','', 'X', '', charges, charges, current_date, vendor_signature, current_date,'','','','','','','','','','','','','JustGo Brokerage Inc',
                '545 W Hacienda Ave Suite 101', 'Campbell','CA','95008','Campbell CA 95008','4083181573', npi_number,''])
            return response
        else:
            for iterdate in date_list:
                writer.writerow(['','Santa Clara Family Health Plan', SCFHP_ID,'','','','','','','','X','','','','','',patientMN ,
                lname, fname,'', patient_birthdate, male_sex, female_sex, lname, fname, '', start_address, '','','', phone,'self',
                '','','', start_address,'','','', phone,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','',
                '','X','SIGNATURE ON FILE', current_date,'SIGNATURE ON FILE', current_date,'','','','','','','','','','','','','','','G8220',
                '','','','','','','','','','','','','','','', iterdate,iterdate,'99','','A0130','','','','','1', charges, units,'','NPI',
                npi_number,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''
                ,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','', fed_tax_ssn,'X'
                '','X','', 'X', '', charges, charges, current_date, vendor_signature, current_date,'','','','','','','','','','','','','JustGo Brokerage Inc',
                '545 W Hacienda Ave Suite 101', 'Campbell','CA','95008','Campbell CA 95008','4083181573', npi_number,''])

                writer.writerow(['','Santa Clara Family Health Plan', SCFHP_ID,'','','','','','','','X','','','','','',patientMN ,
                lname, fname,'', patient_birthdate, male_sex, female_sex, lname, fname, '', start_address, '','','', phone,'self',
                '','','', start_address,'','','', phone,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','',
                '','X','SIGNATURE ON FILE', current_date,'SIGNATURE ON FILE', current_date,'','','','','','','','','','','','','','','G8220',
                '','','','','','','','','','','','','','','', iterdate,iterdate,'99','','A0130','','','','','1', charges, units,'','NPI',
                npi_number,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''
                ,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','', fed_tax_ssn,'X'
                '','X','', 'X', '', charges, charges, current_date, vendor_signature, current_date,'','','','','','','','','','','','','JustGo Brokerage Inc',
                '545 W Hacienda Ave Suite 101', 'Campbell','CA','95008','Campbell CA 95008','4083181573', npi_number,''])
            return response

    else:
        print('Something went wrong')
        one_off = FormBasic.objects.all().order_by('-time_stamp')
        reocurring = Reocurring.objects.all().order_by('-time_stamp')
        print('Problem with OA view code somewhere')
        return render(request, 'rides/download.html', {'one_off' : one_off, 'reocurring' : reocurring})

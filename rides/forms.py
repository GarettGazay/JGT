from django import forms
from . import models
from django.http import HttpResponse



class CreateBooking(forms.ModelForm):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    SERVICE_TYPES = (('SCFHP Basic', 'SCFHP Basic'), ('SCFHP Bariatric', 'SCFHP Bariatric'),
                     ('SCFHP Ambulatory', 'SCFHP Ambulatory'), ('VMC Wheelchair', 'VMC Wheelchair'),
                     ('VMC Ambulatory', 'VMC Ambulatory'), ('VMC Discharge', 'VMC Discharge'), ('VMC Bariatric', 'VMC Bariatric'), ('HERMAN Wheelchair', 'HERMAN Wheelchair'), ('HERMAN Ambulatory', 'HERMAN Ambulatory'), ('HERMAN Bariatric', 'HERMAN Bariatric'))

    ACCOUNT_NUMBERS = (('SC00001', 'SC00001'), ('Fatima001', 'Fatima001'), ('OLISCC',
                                                                            'OLISCC'), ('KINSCC', 'KINSCC'), ('VICSCC', 'VICSCC'), ('MCDSCC', 'MCDSCC'))

    account_number = forms.ChoiceField(required=True, choices=ACCOUNT_NUMBERS)
    service_type = forms.ChoiceField(required=True, choices=SERVICE_TYPES)



    class Meta:
        model = models.FormBasic
        fields = ['account_number', 'service_type', 'call_number', 'diagnostic_code', 'patient_med_number', 'patient_first_name', 'patient_last_name', 'gender', 'patient_phone',
                  'patient_birthdate', 'number_of_passengers', 'appointment_date', 'pickup_time', 'return_time', 'pickup_address', 'destination_address', 'round_trip', ]
        widgets = {
            'call_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SCFHP Only'}),
            'diagnostic_code' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SCFHP Only'}),
            'patient_first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient First Name'}),
            'patient_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Last Name'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-Digit - Digits Only'}),
            'patient_birthdate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MMDDYYYY'}),
            'patient_med_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SCFHP Only'}),
            'number_of_passengers': forms.NumberInput(attrs={'class': 'form-control'}),
            'appointment_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'YYYY-DD-MM'}),
            'pickup_time': forms.TextInput(attrs={'class': 'form-control','placeholder':'24hr format ex. 13:45'}),
            'return_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'24hr format ex. 16:00 -- Leave blank if one way'}),
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Commas or Special Characters'}),
            'destination_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Commas or Special Characters'}),
            'round_trip': forms.CheckboxInput(),
        }


class ReocurringBooking(forms.ModelForm):
    DAY_CHOICES = (('Mon', 'Mon'), ('Tue', 'Tue'), ('Wed', 'Wed'),
                   ('Thur', 'Thur'), ('Fri', 'Fri'), ('Sat', 'Sat'), ('Sun', 'Sun'))

    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))

    SERVICE_TYPES = (('SCFHP Basic', 'SCFHP Basic'), ('SCFHP Bariatric', 'SCFHP Bariatric'), ('SCFHP Ambulatory',
                    'SCFHP Ambulatory'), ('VMC Wheelchair', 'VMC Wheelchair'), ('VMC Ambulatory',
                    'VMC Ambulatory'), ('VMC Discharge', 'VMC Discharge'), ('HERMAN Wheelchair',
                     'HERMAN Wheelchair'), ('HERMAN Ambulatory', 'HERMAN Ambulatory'), ('HERMAN Bariatric', 'HERMAN Bariatric'))

    ACCOUNT_NUMBERS = (('SC00001', 'SC00001'), ('Fatima001', 'Fatima001'), ('OLISCC',
                        'OLISCC'), ('KINSCC', 'KINSCC'), ('VICSCC', 'VICSCC'), ('MCDSCC', 'MCDSCC'))

    weekdays = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=DAY_CHOICES,
    )

    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES)

    class Meta:
        model = models.Reocurring
        fields = ['account_number', 'service_type', 'call_number','diagnostic_code', 'patient_first_name', 'patient_last_name', 'gender', 'patient_phone', 'patient_birthdate', 'patient_med_number',
                  'number_of_passengers', 'pickup_address', 'destination_address', 'pickup_time', 'return_time', 'start_date', 'end_date', 'weekdays', 'round_trip', ]

        widgets = {
            'call_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SCFHP only'}),
            'diagnostic_code' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SCFHP Only'}),
            'patient_first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient First Name'}),
            'patient_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Last Name'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-Digit - Digits Only'}),
            'patient_birthdate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'patient_med_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SCFHP Only'}),
            'number_of_passengers': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Number of Passengers - Use digits'}),
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Commas or Special Characters'}),
            'destination_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Commas or Special Characters'}),
            'pickup_time': forms.TextInput(attrs={'class': 'form-control','placeholder':'24hr format ex. 13:00'}),
            'return_time': forms.TextInput(attrs={'class': 'form-control','placeholder':'24hr format ex. 16:00 -- Leave blank if one way'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'YYYY-DD-MM'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'YYYY-DD-MM'}),
            'round_trip': forms.CheckboxInput(),

        }

class UniversalForm(forms.ModelForm):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    SERVICE_TYPES = (('VMC Wheelchair','VMC Wheelchair'),('VMC Ambulatory','VMC Ambulatory'),('VMC Discharge','VMC Discharge'),('VMC Bariatric','VMC Bariatric'),('HERMAN Wheelchair','HERMAN Wheelchair'),('HERMAN Ambulatory','HERMAN Ambulatory'),('HERMAN Bariatric','HERMAN Bariatric'))
    ACCOUNT_NUMBERS = (('VMC Basic','VMC Basic'),('Herman Basic','Herman Basic'),('Fatima001','Fatima001'),('OLISCC','OLISCC'),('KINSCC','KINSCC'),('VICSCC','VICSCC'),('MCDSCC','MCDSCC'))

    account_number = forms.ChoiceField(required=True, choices=ACCOUNT_NUMBERS)
    service_type = forms.ChoiceField(required=True, choices=SERVICE_TYPES)
    gender = forms.ChoiceField(required=True, choices=GENDER_CHOICES)

    class Meta:
        model = models.UniversalOneWay
        fields = ['account_number', 'service_type', 'patient_first_name', 'patient_last_name', 'gender', 'patient_phone',
                  'patient_birthdate', 'number_of_passengers', 'appointment_date', 'pickup_time', 'return_time', 'pickup_address', 'destination_address', 'round_trip', ]
        widgets = {
            'patient_first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient First Name'}),
            'patient_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient Last Name'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-Digit - Digits Only'}),
            'patient_birthdate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MMDDYYYY'}),
            'number_of_passengers': forms.NumberInput(attrs={'class': 'form-control'}),
            'appointment_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'YYYY-DD-MM'}),
            'pickup_time': forms.TextInput(attrs={'class': 'form-control','placeholder':'24hr format ex. 13:45'}),
            'return_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'24hr format ex. 16:00 -- Leave blank if one way'}),
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Commas or Special Characters'}),
            'destination_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No Commas or Special Characters'}),
            'round_trip': forms.CheckboxInput(),
        }

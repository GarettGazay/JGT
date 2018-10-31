from django.shortcuts import render

def chooser(request):
    return render(request, 'chooser/chooser.html')
    
def welcome(request):
    return render(request, 'chooser/welcome.html')

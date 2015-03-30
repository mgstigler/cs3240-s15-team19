from django.shortcuts import render
from django.http import HttpResponse
from secure_witness.models import Report, Keyword

# Create your views here.
def report(request):
    return render(request, 'enterreport.html', {})

def submit(request):
    s = request.POST['short_description']
    d = request.POST['detailed_description']
    l = request.POST['location']
    k = request.POST['keywords']
    i = request.POST['incident_date']
    p = request.POST['privacy']

    priv = False
    if p == 'Private':
        priv = True

    rep = Report(short=s, detailed=d, location=l, date=i, keywords=k, private=priv)
    rep.save()
    all = Report.objects.all() #filter(short='short')
    return HttpResponse(str(all))
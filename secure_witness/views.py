from django.shortcuts import render
from secure_witness.models import Report, Keyword
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from secure_witness.forms import UserForm

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


def user_login(request):
    # Process data from POST
    if request.method == 'POST':
        # User .get() method to return None if not present
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if password is valid
        user = authenticate(username=username, password=password)

        # If user != None, then login worked
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponse("Login successful")
                # Link to the post-login screen
                #return HttpResponseRedirect('/secure_witness/')
            else:
                return HttpResponse("Account is disabled. Please contact the admin.")

        # Login not successful
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login information supplied")

    # GET request, create a blank form
    else:
        return render(request, 'secure_witness/login.html', {})

# Create your views here.
def register(request):
    # Indicate status of registration
    registered = False

    # Process data from POST
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if (user_form.is_valid()):
            # Save the user_form to the database
            user = user_form.save()

            # Hash the password with set_password
            user.set_password(user.password)
            user.save()

            # Registration finished successfully
            registered = True

        else:
            print(user_form.errors)

    # GET request, create a blank form
    else:
        user_form = UserForm()

    # Return the appropriate request, created above
    return render(request, 'secure_witness/register.html', {
        'user_form': user_form,
        'registered': registered,
    })

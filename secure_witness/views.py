from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from secure_witness.forms import UserForm

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
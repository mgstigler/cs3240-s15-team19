from django.shortcuts import render
from secure_witness.forms import UserForm

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

    # Get request, create a blank form
    else:
        user_form = UserForm()

    # Return the appropriate request, created above
    return render(request, 'secure_witness/register.html', {
        'user_form': user_form,
        'registered': registered,
    })
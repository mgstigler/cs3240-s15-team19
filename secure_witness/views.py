from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from secure_witness import forms
from secure_witness.models import Report, Keyword, Folder
from secure_witness.forms import UserForm




class ListFolderView(ListView):
    model = Folder
    template_name = 'folder_list.html'

class CreateFolderView(CreateView):

    model = Folder
    template_name = 'edit_folder.html'

    def get_success_url(self):
        return reverse('folders-list')
    def get_context_data(self, **kwargs):

        context = super(CreateFolderView, self).get_context_data(**kwargs)
        context['action'] = reverse('folders-new')

        return context

class UpdateFolderView(UpdateView):

    model = Folder
    template_name = 'edit_folder.html'

    def get_success_url(self):
        return reverse('folders-list')
    def get_context_data(self, **kwargs):

        context = super(UpdateFolderView, self).get_context_data(**kwargs)
        context['action'] = reverse('folders-edit',
                                    kwargs={'pk': self.get_object().id})

        return context

class DeleteFolderView(DeleteView):

    model = Folder
    template_name = 'delete_folder.html'

    def get_success_url(self):
        return reverse('folders-list')

class FolderView(DetailView):

    model = Folder
    template_name = 'folder.html'

class EditFolderFileView(UpdateView):

    model = Folder
    template_name = 'edit_files.html'
    form_class = forms.FolderFileFormSet

    def get_success_url(self):

        return self.get_object().get_absolute_url()



# Create your views here.
def report(request):
    return render(request, 'enter_report.html', {})

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
                # Link to the post-login screen
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Account is disabled. Please contact the admin.")

        # Login not successful
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login information supplied")

    # GET request, create a blank form
    else:
        return render(request, 'login.html', {})

def user_logout(request):
    # User must be logged in to reach this section, so can just logout
    logout(request)

    return HttpResponseRedirect('/')

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
    return render(request, 'register.html', {
        'user_form': user_form,
        'registered': registered,
    })

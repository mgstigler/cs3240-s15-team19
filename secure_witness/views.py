from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from secure_witness import forms
from secure_witness.models import Folder, File
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
    template_name = 'enter_report.html'
    form_class = forms.FolderFileFormSet

    def get_success_url(self):

        return self.get_object().get_absolute_url()

def report(request):
    return render(request, 'enter_report.html', {})

def submit(request):
    s = request.POST.get('short_description')
    d = request.POST.get('detailed_description')
    l = request.POST.get('location')
    k = request.POST.get('keywords')
    i = request.POST.get('incident_date')
    p = request.POST.get('privacy')

    priv = False
    if p == 'Private':
        priv = True

    rep = File(short=s, detailed=d, location=l, keywords=k, today=i, private=priv)
    rep.save()
    all = File.objects.all() #filter(short='short')
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

class GroupListView(ListView):
    context_object_name = "group_list"
    template_name = "group_list.html"

    def get_queryset(self):
        return self.request.user.groups.all()


class GroupDetailView(DetailView):
    model = Group
    context_object_name = "group"
    template_name = "group_detail.html"

    def get_context_data(self, **kwargs):
        context =  super(GroupDetailView, self).get_context_data(**kwargs)
        context['user_list'] = self.object.user_set.all()
        return context

class GroupEditView(UpdateView):
    model = Group
    context_object_name = "group"
    template_name = 'group_edit.html'

    fields = ['name']

    def get_success_url(self):
        return reverse('group-list')

    def get_context_data(self, **kwargs):
        context =  super(GroupEditView, self).get_context_data(**kwargs)
        context['user_list'] = self.object.user_set.all()
        return context

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'group_confirm_delete.html'

class GroupCreateView(CreateView):
    model = Group
    fields = ['name']
    template_name = 'group_edit.html'

    def get_success_url(self):
        return reverse('group-list')

    def form_valid(self, form):
        # Add the current user to the group
        g = form.save()
        g.user_set.add(self.request.user)
        g.save()
        return super(GroupCreateView, self).form_valid(form)

def add_user(request, group_id):
    if request.method == 'POST':
        # Get the username from the request
        username = request.POST.get('username')

        # Retrieve user object with the specified username
        user_list = User.objects.filter(username=username)

        # If user with username exists, add them to the current group
        if len(user_list) > 0:
            user = user_list[0]
            group_id = int(group_id)
            g = Group.objects.get(id=group_id)
            g.user_set.add(user)
        else:
            # TODO HANDLE ERRORS
            print("User not found")

    # Return to the group-edit page
    return HttpResponseRedirect(reverse('group-edit', args=(group_id,)))

def remove_user(request, group_id, user_id):
    group_id = int(group_id)
    user_id = int(user_id)

    # Remove the user from the group
    g = Group.objects.get(id=group_id)
    u = User.objects.get(id=user_id)
    g.user_set.remove(u)

    return HttpResponseRedirect(reverse('group-edit', args=(group_id,)))
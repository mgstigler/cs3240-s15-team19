from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.utils import timezone
from django.template import RequestContext

from secure_witness.models import Folder, Media, Report, UserProfile
from secure_witness.forms import UserForm, ReportForm, RegistrationForm

import hashlib, datetime, random


def search(request):
    query = request.GET.get('q')
    if query:
        results = Report.objects.filter(keywords__icontains=query)
    else:
        results = Report.objects.all()
    return render(request, 'search_result.html', {'results':results})

def saved(request):
    return HttpResponse("saved")

def copy(request, pk):
    fld = Report.objects.get(id=pk)
    fld.pk = None
    fld.id = None
    fld.save()
    return HttpResponseRedirect(reverse('report-detail', args=(fld.id,)))

class JointFolderReportView(View):
    def get(self, request, folder_id):
        # TODO FILTER BASED ON CURRENT USER
        if folder_id:
            # Load reports in a specific folder
            folder_list = []
            # Only retrieve public reports or ones that the user owns
            user_group_list = request.user.groups.all()
            query = Q(private=False) | Q(created_by=self.request.user)
            for g in user_group_list:
                query |= Q(authorized_groups=g)
            report_list = Report.objects.filter(Q(folder__id=folder_id), query).distinct().order_by('short')
            cur_folder_name = Folder.objects.filter(id=folder_id)[0].folder_name
        else:
            # Load all folders and reports
            folder_list = Folder.objects.all().order_by('folder_name')
            # Only retrieve public reports or ones that the user owns
            query = Q(private=False) | Q(created_by=self.request.user)
            report_list = Report.objects.filter(Q(folder__id=None), query).order_by('short')
            cur_folder_name = None

        is_admin = request.user.groups.filter(name='admins').exists()

        # Render the page with the appropriate data
        return render(request, 'combined_folder_report_list.html', {
            'folder_list': folder_list,
            'report_list': report_list,
            'cur_folder_name': cur_folder_name,
            'is_admin': is_admin
        })

class CreateReportView(CreateView):

    model = Report
    template_name = 'report_edit.html'
    form_class = ReportForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(CreateReportView, self).form_valid(form)

    def get_success_url(self):
        # Save each file associated with the report
        for file in self.request.FILES.getlist('files'):
            m = Media(filename=str(file), is_encrypted=self.object.private, content=file, report=self.object,
                      created_by=self.request.user, updated_by=self.request.user)
            m.save()

        # Get the folder id from the object for the reverse url
        if self.object.folder:
            return reverse('browse', args=(self.object.folder.id,))
        else:
            return reverse('browse')

    def get_context_data(self, **kwargs):

        context = super(CreateReportView, self).get_context_data(**kwargs)
        context['action'] = reverse('reports-new')

        return context

class UpdateReportView(UpdateView):

    model = Report
    template_name = 'report_edit.html'
    form_class = ReportForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super(UpdateReportView, self).form_valid(form)

    def get_success_url(self):
        # Save each file associated with the report
        for file in self.request.FILES.getlist('files'):
            m = Media(filename=str(file), is_encrypted=self.object.private, content=file, report=self.object)
            m.save()

        # Get the folder id from the object for the reverse url
        if self.object.folder:
            return reverse('browse', args=(self.object.folder.id,))
        else:
            return reverse('browse')
    def get_context_data(self, **kwargs):
        context = super(UpdateReportView, self).get_context_data(**kwargs)
        context['action'] = reverse('report-edit', kwargs={'pk': self.get_object().id})
        context['file_list'] =  Media.objects.filter(report__id=self.object.id)
        return context

class DeleteReportView(DeleteView):

    model = Report
    template_name = 'delete_report.html'

    def get_success_url(self):
        fid = self.object.folder.id
        if fid:
            return reverse('browse', args=(fid,))
        else:
            return reverse('browse')

class ReportView(DetailView):

    model = Report
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['file_list'] =  Media.objects.filter(report__id=self.object.id)
        return context

class CreateFolderView(CreateView):

    model = Folder
    fields = "__all__"
    template_name = 'edit_folder.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(CreateFolderView, self).form_valid(form)

    def get_success_url(self):
        return reverse('browse')

    def get_context_data(self, **kwargs):

        context = super(CreateFolderView, self).get_context_data(**kwargs)
        context['action'] = reverse('folders-new')

        return context

class UpdateFolderView(UpdateView):

    model = Folder
    fields = "__all__"
    template_name = 'edit_folder.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super(UpdateFolderView, self).form_valid(form)

    def get_success_url(self):
        return reverse('browse')
    def get_context_data(self, **kwargs):

        context = super(UpdateFolderView, self).get_context_data(**kwargs)
        context['action'] = reverse('folders-edit',
                                    kwargs={'pk': self.get_object().id})

        return context

class DeleteFolderView(DeleteView):

    model = Folder
    fields = "__all__"
    template_name = 'delete_folder.html'

    def get_success_url(self):
        return reverse('browse')

class FolderView(DetailView):

    model = Folder
    fields = "__all__"
    template_name = 'folder.html'

"""
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

    # Save each file associated with the Report
    for file in request.FILES.getlist('media'):
        if priv==True:
            new_iv = Random.new().read(DES3.block_size)  # get_random_bytes(8)
            new_key = Random.new().read(DES3.key_size[-1])  # get_random_bytes(16)
            in_filename = str(file)
            spot = in_filename.index(".")
            out_filename = in_filename[0:spot] + ".enc"
            encrypt_file(in_filename, out_filename, 8192, new_key, new_iv)
            Media(filename=in_filename, is_encrypted=p, content=out_filename, report=rep, key=new_key, iv=new_iv).save()
        else:
           Media(filename=str(file), is_encrypted=p, content=file, report=rep, key=0, iv=0).save()

    all = File.objects.all() #filter(short='short')
    return HttpResponse(all)

def encrypt_file(in_filename, out_filename, chunk_size, key, iv):
    des3 = DES3.new(key, DES3.MODE_CFB, iv)
    with open(in_filename, 'rb') as in_file:
        with open(out_filename, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b"\0" * (16 - len(chunk) % 16)
                out_file.write(des3.encrypt(chunk))
"""

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
                return HttpResponseRedirect('/browse/')
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

    return HttpResponseRedirect('/login/')

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

def register_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')
            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = timezone.now() + datetime.timedelta(2)

            # Get the user
            user = User.objects.get(username=username)

            # Create new user profile
            user_profile = UserProfile(user=user, activation_key=activation_key,
                   key_expires=key_expires)
            user_profile.save()

            # Send activation email
            email_subject = 'Account Confirmation'
            email_body = "To activate your account, please visit: \
                http://127.0.0.1:8000/confirm/%s" % (activation_key)

            send_mail(email_subject, email_body, 'sdgennari@gmail.com', [email], fail_silently=False)

            return HttpResponseRedirect('login')

    else:
        args['form'] = RegistrationForm()

    return render_to_response('register.html', args, context_instance=RequestContext(request))

def register_confirm(request, activation_key):
    # If the user is already logged in, stop activation process
    if request.user.is_authenticated():
        HttpResponseRedirect('/browse')

    # Check if a user with the activation_key exists
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # Make sure the user has not expired
    if user_profile.key_expires < timezone.now():
        return HttpResponse("Activation key has expired. Please re-register")

    user = user_profile.user
    user.is_active = True
    user.save()
    return HttpResponse("Account confirmed")

class GroupListView(ListView):
    context_object_name = "group_list"
    template_name = "group_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='admins').exists():
            return Group.objects.all()
        else:
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

    def get_success_url(self):
        return reverse('group-list')

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

class AdminUserManager(View):
    def get(self, request):
        # Load the users onto the page
        user_list = User.objects.all().order_by('username')
        return render(request, 'user_manager_list.html', {
            'user_list': user_list,
        })

def switch_user_active(request, user_id):
    user_id = int(user_id)
    user = User.objects.get(id=user_id)
    user.is_active = (not user.is_active)
    user.save()

    return HttpResponseRedirect('/user-manager/')

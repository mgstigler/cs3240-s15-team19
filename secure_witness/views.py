from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

from secure_witness import forms
from secure_witness.models import Folder, Media, Report
from secure_witness.forms import UserForm, ReportForm


def saved(request):
    return HttpResponse("saved")

class JointFolderReportView(View):
    def get(self, request, folder_id):
        # TODO FILTER BASED ON CURRENT USER
        if folder_id:
            # Load reports in a specific folder
            folder_list = []
            # Only retrieve public reports or ones that the user owns
            query = Q(private=False) | Q(created_by=self.request.user)
            report_list = Report.objects.filter(Q(folder__id=folder_id), query).order_by('short')
            cur_folder_name = Folder.objects.filter(id=folder_id)[0].folder_name
        else:
            # Load all folders and reports
            folder_list = Folder.objects.all().order_by('folder_name')
            # Only retrieve public reports or ones that the user owns
            query = Q(private=False) | Q(created_by=self.request.user)
            report_list = Report.objects.filter(Q(folder__id=None), query).order_by('short')
            cur_folder_name = None

        # Render the page with the appropriate data
        return render(request, 'combined_folder_report_list.html', {
            'folder_list': folder_list,
            'report_list': report_list,
            'cur_folder_name': cur_folder_name,
        })

class ListReportView(ListView):

    model = Report
    template_name = 'report_list.html'
    context_object_name = "report_list"

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
            return reverse('folders-view', args=(self.object.folder.id,))
        else:
            return reverse('folders-list')

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
            return reverse('folders-view', args=(self.object.folder.id,))
        else:
            return reverse('folders-list')
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
            return reverse('folders-view', args=(fid,))
        else:
            return reverse('folders-list')

class ReportView(DetailView):

    model = Report
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['file_list'] =  Media.objects.filter(report__id=self.object.id)
        return context

class ListFolderView(ListView):
    model = Folder
    template_name = 'folder_list.html'

class CreateFolderView(CreateView):

    model = Folder
    template_name = 'edit_folder.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(CreateFolderView, self).form_valid(form)

    def get_success_url(self):
        return reverse('folders-list')

    def get_context_data(self, **kwargs):

        context = super(CreateFolderView, self).get_context_data(**kwargs)
        context['action'] = reverse('folders-new')

        return context

class UpdateFolderView(UpdateView):

    model = Folder
    template_name = 'edit_folder.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super(UpdateFolderView, self).form_valid(form)

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

"""
class EditFolderFileView(UpdateView):

    model = Folder
    template_name = 'enter_report.html'
    form_class = forms.FolderFileFormSet

    def get_success_url(self):

        return self.get_object().get_absolute_url()
"""
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
import os
import zipfile
import io
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

from secure_witness.models import *
from secure_witness.forms import *

import hashlib, datetime, random

from Crypto.Cipher import DES3
import random
import mimetypes

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def search(request):
    query = request.GET.get('q')
    q = Q(private=False) | Q(created_by=request.user)
    user_group_list = request.user.groups.all()
    for g in user_group_list:
        q |= Q(authorized_groups=g)
    if query:
        results = Report.objects.filter(q, Q(short__icontains=query) | Q(detailed__icontains=query) | Q(keywords__icontains=query)).order_by('time')
    else:
        results = Report.objects.filter(q)
    return render(request, 'search_result.html', {'results':results})

def saved(request):
    return HttpResponse("saved")

def copy(request, pk):
    fld = Report.objects.get(id=pk)
    fld.pk = None
    fld.id = None
    fld.save()
    return HttpResponseRedirect(reverse('report-detail', args=(fld.id,)))

def advanced_search(request):

    if request.method == 'POST':
        short = request.POST.get('short_description')
        detailed = request.POST.get('detailed_description')
        keyword = request.POST.get('keywords')
        user_group_list = request.user.groups.all()
        query = Q(private=False) | Q(created_by=request.user)
        for g in user_group_list:
            query |= Q(authorized_groups=g)

        if short or detailed or keyword:
        
            results = Report.objects.filter(query, short__icontains=short, detailed__icontains=detailed, keywords__icontains=keyword).order_by('time') 
        else:
            results = Report.objects.filter(query)
        return render(request, 'search_result.html', {'results':results})
    else:
        return render(request, 'advanced_search.html', {})


class JointFolderReportView(View):
    def get(self, request, folder_id):
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
            user_group_list = request.user.groups.all()
            query = Q(private=False) | Q(created_by=self.request.user)
            for g in user_group_list:
                query |= Q(authorized_groups=g)
            report_list = Report.objects.filter(Q(folder__id=None), query).order_by('short')
            cur_folder_name = None

        # Render the page with the appropriate data
        return render(request, 'combined_folder_report_list.html', {
            'folder_list': folder_list,
            'report_list': report_list,
            'cur_folder_name': cur_folder_name,
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
         # Save each file associated with the report
        for file in self.request.FILES.getlist('files'):
            mimetypes.init()
            mime_type = mimetypes.guess_type(str(file))
            file_type = mime_type[0]
            if self.object.private:
                new_iv = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
                new_key = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for j in range(16))
                des3 = DES3.new(new_key, DES3.MODE_CFB, new_iv)
                enc_filename = str(file) + ".enc"
                with open("media/" + enc_filename, 'wb') as enc_file:
                    for chunk in file.chunks(8192):
                        if len(chunk) == 0:
                            break
                        elif len(chunk) % 16 != 0:
                            chunk += (' ' * (16 - len(chunk) % 16)).encode()
                            enc_file.write(des3.encrypt(chunk))
                        else:
                            enc_file.write(des3.encrypt(chunk))
                        enc_file.seek(0)
                m = Media(filename=str(enc_filename), is_encrypted=self.object.private, content=enc_filename,
                          report=self.object, key=new_key, iv=new_iv, fileType=file_type,
                          created_by=self.request.user, updated_by=self.request.user)
                m.save()
            else:
                m = Media(filename=str(file), is_encrypted=self.object.private, content=file,
                          report=self.object, fileType=file_type,
                          created_by=self.request.user, updated_by=self.request.user)
                m.save()

        # Every report can be seen by admins
        admin_group = Group.objects.get(name="admins")
        self.object.authorized_groups.add(admin_group)

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
         # Save each file associated with the report
        for file in self.request.FILES.getlist('files'):
            mimetypes.init()
            mime_type = mimetypes.guess_type(str(file))
            file_type = mime_type[0]
            if self.object.private:
                new_iv = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
                new_key = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for j in range(16))
                des3 = DES3.new(new_key, DES3.MODE_CFB, new_iv)
                enc_filename = str(file) + ".enc"
                with open("media/" + enc_filename, 'wb') as enc_file:
                    for chunk in file.chunks(8192):
                        if len(chunk) == 0:
                            break
                        elif len(chunk) % 16 != 0:
                            chunk += (' ' * (16 - len(chunk) % 16)).encode()
                            enc_file.write(des3.encrypt(chunk))
                        else:
                            enc_file.write(des3.encrypt(chunk))
                        enc_file.seek(0)
                m = Media(filename=str(enc_filename), is_encrypted=self.object.private, content=enc_filename,
                          report=self.object, key=new_key, iv=new_iv, fileType=file_type,
                          created_by=self.request.user, updated_by=self.request.user)
                m.save()
            else:
                m = Media(filename=str(file), is_encrypted=self.object.private, content=file,
                          report=self.object, fileType=file_type,
                          created_by=self.request.user, updated_by=self.request.user)
                m.save()

        # Every report can be seen by admins
        admin_group = Group.objects.get(name="admins")
        self.object.authorized_groups.add(admin_group)

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
        if self.object.folder:
            return reverse('browse', args=(self.object.folder.id,))
        else:
            return reverse('browse')

class ReportView(DetailView):

    model = Report
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        context['file_list'] =  Media.objects.filter(report__id=self.object.id)

        # Get the list of comments associated with the report
        context['comment_list'] = Comment.objects.filter(report__id=self.object.id).order_by('-created_at')
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

def user_login(request):
    # Process data from POST
    print('Request received')
    if request.method == 'POST':
        print("post-received")
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
                /confirm/%s" % (activation_key)

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

def edit_profile(request):

    #Save the new info into the existing user instance
    if request.method == "POST":
        form = UserForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
        #else:
         #  return HttpResponse("Please enter information for each field.")

        #Keep the user logged in
        # User .get() method to return None if not present
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if password is valid
        sameuser = authenticate(username=username, password=password)

        # If user != None, then login worked
        if sameuser:
            if sameuser.is_active:
                login(request, sameuser)
                # Link to the post-login screen
                return HttpResponseRedirect('/browse/')
            else:
                return HttpResponse("Account is disabled. Please contact the admin.")
        else:
            return HttpResponse("Invalid login information supplied")

    #display the edit form with existing user instance information
    else:
        form = UserForm(instance=request.user)
        return render(request, 'edit_profile.html', {'form': form})

def downloadfiles(request, pk):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    filenames = []


    if Media.objects.filter(id=pk):
        for querydict in Media.objects.filter(id=pk).values():
            path = '/cs3240-s15-team19/group/media/'+querydict[filename]
            if path != '':
                filenames.append(path)

    
    for querydict in Media.objects.filter(id=pk).values():
        path = '/cs3240-s15-team19/group/media/'+querydict['filename']
        if path != '':
            filenames.append(path)


    # The zip compressor
        zf = zipfile.ZipFile('media.zip', "w")
        for x in filenames:
            zf.write(x)

    # Must close zip for all contents to be written
        zf.close()

    # Grab ZIP file from in-memory
        resp = HttpResponse(zf, content_type='application/zip')
    # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % "media.zip"

        return resp
    else:
        return HttpResponseRedirect(reverse('report-detail', args=(pk)))

def add_comment(request, report_id):
    if request.method == 'POST':
        # Get the information from the post
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Get the associated report
        report = Report.objects.get(id=report_id)

        # Create and save a comment with the new info
        comment = Comment(title=title, description=description, report=report)
        comment.created_by = request.user
        comment.updated_by = request.user
        comment.save()

        # Return to the report view
        return HttpResponseRedirect(reverse('report-detail', args=(report_id)))

class CommentUpdateView(UpdateView):
    model = Comment
    fields = "__all__"
    template_name = "comment_edit.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super(CommentUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('report-detail', args=(self.object.report.id,))

class CommentDeleteView(DeleteView):
    model = Comment
    fields = "__all__"
    template_name = "comment_confirm_delete.html"

    def get_success_url(self):
        return reverse('report-detail', args=(self.object.report.id,))

def media_delete(request, report_id, media_id):
    media_id = int(media_id)

    m = Media.objects.get(id=media_id)
    m.delete()

    return HttpResponseRedirect(reverse('report-edit', args=(report_id,)))

# =================================================================
# JSON views/methods for standalone app
# =================================================================
@csrf_exempt
def json_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user and user.is_active:
        resp = {
            'status': 'success',
            'user': {
                'id': user.id,
                'username': user.username,
            }
        }
    else:
        resp = {
            'status': 'failure',
        }

    return JsonResponse(resp)

def json_report_list(request, user_id):
    print("Called")
    # Get the corresponding user
    user = User.objects.get(id=user_id)

    # Get the associated reports
    user_group_list = user.groups.all()
    query = Q(private=False) | Q(created_by=user)
    for g in user_group_list:
        query |= Q(authorized_groups=g)
    report_list = Report.objects.filter(query).distinct().order_by('short')

    report_resp_list = []
    for report in report_list:
        rep_resp = {
            'id': report.id,
            'short': report.short,
        }
        report_resp_list.append(rep_resp)

    response = {'report_list': report_resp_list}

    return JsonResponse(response)


def json_test(request):
    report = Report.objects.get(id=1)
    media_list = Media.objects.filter(report__id=1)
    file_resp = {}
    for i in range(len(media_list)):
        file_str = "file" + str(i)
        file_resp[file_str] = media_list[i].filename
    resp = {
        'short': report.short,
        'detailed': report.detailed,
        'time': report.time,
        'location': report.location,
        'folder': str(report.folder),
        'keywords': str(report.keywords),
        'private': report.private,
        'authorized_groups': str(report.authorized_groups),
        'file_list': file_resp,
    }
    return JsonResponse(resp)
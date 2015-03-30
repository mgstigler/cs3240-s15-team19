from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from secure_witness import forms

from secure_witness.models import Folder
from django.core.urlresolvers import reverse




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
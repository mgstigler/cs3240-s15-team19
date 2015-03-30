from django.forms.models import inlineformset_factory


from secure_witness.models import (
    Folder,
    File,
)


FolderFileFormSet = inlineformset_factory(
    Folder,
    File,
)
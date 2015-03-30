import os
from libs.http import HttpJsonResponse
from sendfile import sendfile
from seeseehome.settings import BASE_DIR
from boards.models import AttachmentFile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseNotFound


@login_required
@csrf_exempt
def file_upload(request, board_id):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        tmp_path = uploaded_file.temporary_file_path()

        file_model = AttachmentFile.objects.create_attachment(request.user, file_name, tmp_path)

        return HttpJsonResponse({'hash_key': file_model.md5_hash, 'file_name': file_name})

    return HttpResponseBadRequest("Bad request")


@login_required
def file_download(request, file_hash_key):
    attachments = AttachmentFile.objects.filter(md5_hash=file_hash_key)[:1]
    if len(attachments) == 1:
        attachment = attachments[0]

        dir_path = os.path.join(BASE_DIR, 'attach_file')
        file_path = os.path.join(dir_path, attachment.md5_hash)

        return sendfile(request, file_path, attachment=True, attachment_filename=attachment.file_name)
    else:
        return HttpResponseNotFound("File not found")

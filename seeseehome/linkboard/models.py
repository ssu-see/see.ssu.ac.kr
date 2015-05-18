import hashlib

from django.db import models
from seeseehome import msg, testdata
from django.core.exceptions import ValidationError
from users.models import User
from django.core.validators import URLValidator
from subprocess import Popen
from os import mkdir
from os.path import join, exists
from seeseehome.settings.settings import BASE_DIR

class LinkPostManager(models.Manager):
    # CREATE

    def _create_linkpost(self, description, url, writer):
        self.validate_description(description)
        if not self.is_valid_writeperm_to_linkpost(writer):
            raise ValidationError(msg.linkboard_linkpost_invalid_writer_perm)
        urlvalidator = URLValidator()
        urlvalidator(url)

        linkpost = self.model(description=description, url=url,
                              writer=writer)

        linkpost.save(using=self._db)

        return linkpost

    def create_linkpost(self, description, url, writer):
        return self._create_linkpost(description=description,
                                     url=url, writer=writer).check_link_thumbnail()

    def validate_description(self, description):
        if not description:
            raise ValueError(msg.boards_linkpost_description_must_be_set)
        elif len(description) > 255:
            raise ValidationError(msg.boards_linkpost_description_at_most_255)

    def is_valid_writeperm_to_linkpost(self, writer):
        #       linkpost is allowed who has the permission higher than 'user'
        return bool(writer.userperm >= testdata.perm_member)

    def is_valid_readperm_to_linkpost(self, reader):
        #       linkboard is allowed who has the permission equal or higher than 'user'
        return bool(reader.userperm >= testdata.perm_user)

##########
# RETRIEVE
    def get_linkpost(self, id):
        try:
            return LinkPost.objects.get(pk=id)
        except LinkPost.DoesNotExist:
            return None

##########
# UPDATE
    def update_linkpost(self, linkpost_id, **extra_fields):
        linkpost = LinkPost.objects.get_linkpost(linkpost_id)
        if 'url' in extra_fields:
            linkpost.url = extra_fields['url']
        if 'description' in extra_fields:
            linkpost.description = extra_fields['description']

        linkpost.save()


class LinkPost(models.Model):
    objects = LinkPostManager()
    writer = models.ForeignKey(User)
    description = models.CharField(
        help_text="A description about the link",
        max_length=255,
    )

    url = models.URLField(
        help_text="An URL for link to some information",
        #           max_length = 200, # default : 200
    )


#   It is used to show date posted in admin page
    date_posted = models.DateTimeField(db_index=True, auto_now_add=True,
                                       help_text="It is used to show date when the link posted")

    def _exists_thumbnail(self):
        
        link_img_dir = join(BASE_DIR, 'static', 'link_img')

        md5 = hashlib.md5()
        md5.update(self.url)

        if not exists(link_img_dir):
            mkdir(link_img_dir)

        save_path = join(link_img_dir, md5.hexdigest() + '.png')

        return (exists(save_path), save_path)

    def _create_link_thumbnail(self):

        is_exists, save_path = self._exists_thumbnail()

        if not is_exists:
            run_capture_path = join(BASE_DIR, 'linkboard', 'worker', 'site_capture.py')        
            Popen(['python', run_capture_path, self.url, save_path])

    def check_link_thumbnail(self):
        self._create_link_thumbnail()

#   for showing description instead of object itself
    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ['-date_posted']

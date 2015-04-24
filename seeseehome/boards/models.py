# -*- coding: utf-8 -*-

import hashlib
import os
import shutil
from seeseehome.settings.partials.application import BASE_DIR
from django.db import models
from users.models import User
from seeseehome import msg
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from multiselectfield import MultiSelectField
from cleartag import ClearTag


class BoardManager(models.Manager):
    # CREATE

    def _create_board(self, boardname):
        self.validate_boardname(boardname)
        self.validate_max_number_of_boards(Board.objects.all().count())
        board = self.model(boardname=boardname)
        board.save(using=self._db)
        return board

    def create_board(self, boardname):
        return self._create_board(boardname)

    def validate_max_number_of_boards(self, num_of_boards):
        #       Number of Boards are already more than or equal to 10?
        if num_of_boards >= 10:
            raise ValidationError(msg.boards_max_number_of_boards)
        return True

    def validate_boardname(self, boardname):
        if not boardname:
            raise ValueError(msg.boards_name_must_be_set)
        elif len(boardname) > 30:
            raise ValidationError(msg.boards_name_at_most_30)
        return True

    def get_board(self, id):
        try:
            return Board.objects.get(pk=id)
        except Board.DoesNotExist:
            return None

    def update_board(self, id, **extra_fields):
        board = Board.objects.get_board(id)
        if 'boardname' in extra_fields:
            self.validate_boardname(extra_fields['boardname'])
            board.boardname = extra_fields['boardname']
        else:
            raise ValueError()
        board.save(using=self._db)

    def delete_board(self, id):
        board = Board.objects.get(id=id)
        board.delete()


class Board(models.Model):
    objects = BoardManager()

    boardname = models.CharField(
        help_text="Board name",
        max_length=255,
        default='',
    )

    readperm = MultiSelectField(
        choices=(('0', 'None'), ('1', 'User'), ('2', 'Member'),
                 ('3', 'Core member'), ('4', 'Graduate'), ('5', 'President')),
        default=['0', '1', '2', '3', '4', '5'],
        max_length=11,
        max_choices=6,
    )

    writeperm = MultiSelectField(
        choices=(
            ('1', 'User'), ('2', 'Member'), ('3', 'Core member'),
            ('4', 'Graduate'), ('5', 'President')),
        default=['0', '1', '2', '3', '4', '5'],
        max_length=9,
        max_choices=5,
    )

    commentperm = MultiSelectField(
        choices=(
            ('1', 'User'), ('2', 'Member'), ('3', 'Core member'),
            ('4', 'Graduate'), ('5', 'President')),
        default=['0', '1', '2', '3', '4', '5'],
        max_length=9,
        max_choices=5,
    )

    def __unicode__(self):
        return self.boardname


class AttachmentFileManager(models.Manager):

    def create_attachment(self, uploader, file_name, tmp_file_path):
        return self._create_attachment(uploader, file_name, tmp_file_path)

    def _create_attachment(self, uploader, file_name, tmp_file_path):
        attachment = self.model(uploader=uploader, file_name=file_name)
        attachment.md5_hash = self.hashfile(tmp_file_path)

        dir_path = os.path.join(BASE_DIR, 'attach_file')
        file_path = os.path.join(dir_path, attachment.md5_hash)

        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        if not os.path.isfile(file_path):
            shutil.move(tmp_file_path, file_path)

        attachment.save()

        return attachment

    def hashfile(self, file_path, hasher=None, blocksize=65536):
        if hasher is None:
            hasher = hashlib.md5()
        with open(file_path) as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)

        return hasher.hexdigest()

    def file_by_hash_key(self, hash_key):
        file_list = self.filter(md5_hash=hash_key)[:1]
        if len(file_list) > 0:
            return file_list[0]
        else:
            return None


class AttachmentFile(models.Model):
    objects = AttachmentFileManager()
    uploader = models.ForeignKey(User)

    file_name = models.CharField(
        help_text="Attachment file's name",
        max_length=255,
        default='',
    )

    md5_hash = models.CharField(
        help_text="Attachment file's name",
        max_length=255,
        default='',
        db_index=True,
    )

    timestamp = models.DateTimeField(auto_now_add=True,
                                     help_text="Uploaded time")

    def __unicode__(self):
        return self.file_name


class PostManager(models.Manager):

    clear = ClearTag()

    # CREATE
    def _create_post(self, board, writer, subject, **extra_fields):
        is_valid_content = False
        is_valid_writer = False

#       board
        try:
            Board.objects.get_board(board.id)
        except ObjectDoesNotExist:
            raise ValidationError(msg.boards_boards_arg_does_not_exist)

#       writer
        is_valid_writer = self.is_valid_writeperm(
            board=board,
            writer=writer
        )
        if not is_valid_writer:
            raise ValidationError(msg.boards_writer_perm_error)

#       subject escape
        subject = PostManager.clear.clear_tag(subject)

#       subject
        self.validate_subject(subject)

#       content
        if 'content' in extra_fields:
            content = extra_fields['content']
            content = PostManager.clear.clear_tag(content)  # escape content
            is_valid_content = self.validate_content(content)

#       post save ( caution : board is not parameter for post model )
        post = self.model(board=board, writer=writer, subject=subject)

        if is_valid_content:
            post.content = content

#       is_notice
        if 'is_notice' in extra_fields:
            is_notice = extra_fields['is_notice']
            if is_notice == "option1":
                post.is_notice = True

        post.save(using=self._db)
        return post

    def create_post(self, board, subject, writer, **extra_fields):
        return self._create_post(board=board, subject=subject, writer=writer,
                                 **extra_fields)

    def validate_subject(self, subject):
        if not subject:
            raise ValueError(msg.boards_post_subject_must_be_set)
        elif len(subject) > 255:
            raise ValidationError(msg.boards_post_subject_at_most_255)

    def validate_content(self, content):
        # if len(content) > 65535:
        #      raise ValidationError(msg.boards_post_content_at_most_65535)
        # else:
        return True

    def is_valid_writeperm(self, board, writer):
        return bool(str(board.writeperm).find(writer.userperm) >= 1)

        """
        Following code is more simple and operates well,
        but it occurs some problems in the test codes
        ( double wrapping of unicode & list )
        """
#        return bool(writer.userperm in board.writeperm)

    ##########
    # RETRIEVE
    def get_post(self, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

    ##########
    # UPDATE
    def update_post(self, post_id, **extra_fields):
        post = Post.objects.get_post(post_id)
        if 'subject' in extra_fields:
            post.subject = PostManager.clear.clear_tag(extra_fields['subject'])
        if 'content' in extra_fields:
            post.content = PostManager.clear.clear_tag(extra_fields['content'])
        if 'is_notice' in extra_fields:
            post.is_notice = extra_fields['is_notice']
        if 'attachment_file' in extra_fields:
            post.attachments.add(extra_fields['attachment_file'])

        post.save()

    def hit_count(self, post_id):
        post = Post.objects.get_post(post_id)
        post.hit_count += 1
        post.save()


class Post(models.Model):
    objects = PostManager()
    writer = models.ForeignKey(User)
    board = models.ForeignKey(Board)
    subject = models.CharField(
        help_text="Post subject",
        max_length=255,
        default='',
    )

    content = models.TextField(
        help_text="Post content",
        # max_length = 65535,
        default='',
    )

#   It is used to show date posted in admin page
    date_posted = models.DateTimeField(db_index=True, auto_now_add=True,
                                       help_text="It is used to show the date posted in admin page")

    is_notice = models.BooleanField(
        help_text="Is this post a notice?",
        default=False
    )

    hit_count = models.IntegerField(
        help_text="counting of watched",
        default=0,
    )
    attachments = models.ManyToManyField(AttachmentFile, blank=True)

    def __unicode__(self):
        return ('Writer: ' + self.writer.username + ", " +
                "Subject: " + self.subject)

    class Meta:
        ordering = ['-is_notice', '-date_posted']


class CommentManager(models.Manager):
    # CREATE

    def _create_comment(self, writer, board, post, comment):
        is_valid_commenter = self.is_valid_comment_perm(
            board=board,
            commenter=writer
        )
        if not is_valid_commenter:
            raise ValidationError("")

#       post
        try:
            post = Post.objects.get_post(post.id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(msg.boards_comment_post_does_not_exist)

#       board
        try:
            board = Board.objects.get_board(board.id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(msg.boards_comment_board_does_not_exist)

#       comment
        self.validate_comment(comment)

#       commentobject save
        commentobject = self.model(writer=writer, post=post, board=board,
                                   comment=comment)

        commentobject.save(using=self._db)

        return commentobject

    def create_comment(self, writer, board, post, comment):
        return self._create_comment(writer=writer, board=board, post=post,
                                    comment=comment)

    def validate_comment(self, comment):
        if not comment:
            raise ValueError(msg.boards_comment_must_be_set)
        elif len(comment) > 255:
            raise ValidationError(msg.boards_comment_at_most_255)

    def is_valid_comment_perm(self, board, commenter):
        return bool(str(board.commentperm).find(commenter.userperm) >= 1)

    ##########
    # RETRIEVE
    def get_comment(self, id):
        try:
            return Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            return None

    ##########
    # UPDATE
    def update_comment(self, comment_id, **extra_fields):
        commentobject = Comment.objects.get_comment(comment_id)
        if 'comment' in extra_fields:
            comment = extra_fields['comment']
            self.validate_comment(comment)
            commentobject.comment = comment

        commentobject.save()


class Comment(models.Model):
    objects = CommentManager()
    writer = models.ForeignKey(User)
    board = models.ForeignKey(Board)
    post = models.ForeignKey(Post)

    comment = models.CharField(
        help_text="Comment",
        max_length=255,
    )

    date_commented = models.DateTimeField(db_index=True, auto_now_add=True,
                                          help_text="It is used to show the date commented")

#   for showing comment information instead of object itself
    def __unicode__(self):
        return ('Writer: ' + self.writer.username + ", " +
                "Comment: " + self.comment)

# -*- coding: utf-8 -*-
from django.test import TestCase
from boards.models import Board, Post, Comment
from django.core.exceptions import ValidationError
from seeseehome import testdata
from users.models import User


class CommentManagerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.board = Board.objects.create_board(
            boardname=testdata.boards_valid_name,
        )

        self.post = Post.objects.create_post(
            board=self.board,
            subject=testdata.posts_valid_subject,
            writer=self.user,
            content=testdata.posts_valid_content,
        )

    def test_create_comment(self):
        self.assertIsNotNone(
            Comment.objects.create_comment(
                writer=self.user,
                board=self.board,
                post=self.post,
                comment=testdata.comments_valid_comment,
            )
        )

    def test_get_comment(self):
        commentobject = Comment.objects.create_comment(
            writer=self.user,
            board=self.board,
            post=self.post,
            comment=testdata.comments_valid_comment,
        )
        self.assertIsNotNone(Comment.objects.get_comment(commentobject.id))

    def test_create_comment_with_comment_more_than_max_length(self):
        self.assertRaises(
            ValidationError,
            Comment.objects.create_comment,
            writer=self.user,
            board=self.board,
            post=self.post,
            comment=testdata.comments_comment_more_than_max_length,
        )

    def test_create_comment_with_no_comment(self):
        self.assertRaises(
            ValueError,
            Comment.objects.create_comment,
            writer=self.user,
            board=self.board,
            post=self.post,
            comment="",
        )

    def test_create_comment_with_user_who_does_not_have_write_perm(self):
        self.board.commentperm = testdata.perm_member
        self.assertRaises(
            ValidationError,
            Comment.objects.create_comment,
            writer=self.user,
            board=self.board,
            post=self.post,
            comment="comment should not be blank",
        )

    def test_update_comment(self):
        commentobject = Comment.objects.create_comment(
            writer=self.user,
            board=self.board,
            post=self.post,
            comment=testdata.comments_old_comment,
        )
        self.assertEqual(commentobject.comment, testdata.comments_old_comment)
        Comment.objects.update_comment(
            comment_id=commentobject.id,
            comment=testdata.comments_new_comment
        )
        commentobject_updated = Comment.objects.get_comment(commentobject.id)
        self.assertEqual(
            commentobject_updated.comment,
            testdata.comments_new_comment
        )

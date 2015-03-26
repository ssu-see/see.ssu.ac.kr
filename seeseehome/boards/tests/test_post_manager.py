#-*- coding: utf-8 -*-
from django.test import TestCase
from boards.models import Board, Post
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from seeseehome import testdata
from users.models import User


class PostManagerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username=testdata.users_valid_name,
            email=testdata.users_valid_email,
            password=testdata.users_valid_password,
        )
        self.board = Board.objects.create_board(
            boardname=testdata.boards_valid_name,
        )

    def test_create_post(self):
        self.assertIsNotNone(
            Post.objects.create_post(
                board=self.board,
                subject=testdata.posts_valid_subject,
                writer=self.user,
                content=testdata.posts_valid_content,
            )
        )

    def test_get_post(self):
        post = Post.objects.create_post(
            board=self.board,
            subject=testdata.posts_valid_subject,
            writer=self.user,
            content=testdata.posts_valid_content,
        )

        self.assertIsNotNone(
            Board.objects.get_board(
                id=post.id
            )
        )

    def test_writer_who_does_not_have_perm_to_post_in_specific_board(self):
        """
        - Scenario
        An user who does not have member permission cannot write
        the board that only allow the user does have member perm to post
        """
        self.board.writeperm = list(unicode(testdata.perm_member))
        self.assertRaises(
            ValidationError,
            Post.objects.create_post,
            board=self.board,
            subject=testdata.posts_valid_subject,
            writer=self.user,
            content=testdata.posts_valid_content,
        )

#-*- coding: utf-8 -*-
# All apps
# permission
perm_anonymous = '0'
perm_user = '1'
perm_member = '2'
perm_coremember = '3'
perm_graduate = '4'
perm_president = '5'

# users
users_valid_email = "test@example.com"
users_available_email = "available_email@example.com"
users_second_valid_email = "secondtest@example.com"
users_superuser_email = "superuser@example.com"
users_valid_password = "test_password123!"
users_pwd_without_special_char = "test_password123"
users_pwd_without_alphabet_char = "123123!"
users_pwd_under_6_characters = "a" * 3 + "1" + "!"
users_pwd_over_255_characters = "a" * 254 + "1" + "!"
users_not_created_user_email = "nouser@example.com"
users_not_created_user_id = 0
users_name_under_1_char = ""
users_name_over_30_char = "a" * 31
users_old_name = "OldName1233-_"
users_new_name = "NewName1234-_"
users_name_with_special_char = "NewName1234!@#$"
users_new_over_length_name = "a" * 31
users_contact_number = "010-0000-0000"
# The following email is not sign-in yet
users_valid_name = "Available_-123User-Name"
users_invalid_name_exceed_the_maximum = "a" * 31
users_name_with_special_char = "invalid_name!@#"

# boards
boards_old_name = "OldName1233-_!@#"
boards_new_name = "NewName1234-_!@#"
boards_new_over_length_name = "a" * 31
# The following email is not sign-in yet
boards_valid_name = "Available_-123Board-Name!@#$"
boards_invalid_name_exceed_the_maximum = "a" * 31
boards_name_over_30_char = "a" * 31
boards_name_under_1_char = ""

# posts
posts_valid_subject = "123!@#asdASDㅁㄴㅇㄲㄸㅆ _-!"
posts_valid_content = "123!@#asdASDㅁㄴㅇㄲㄸㅆ _-!"

# comments
comments_valid_comment = "123!@#asdASDㅁㄴㅇㄲㄸㅆ _-!"
comments_comment_more_than_max_length = "1" * 256
comments_old_comment = "Old Comment!ASAF올드"
comments_new_comment = "New Comment!ASAF새거"


# linkboard
linkboard_valid_description = "123!@#asdASDㅁㄴㅇㄲㄸㅆ _-!"
linkboard_valid_url = "https://github.com"

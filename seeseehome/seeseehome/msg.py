# All apps
# users
# user permission level
perm_anonymous = 0
perm_user = 1
perm_member = 2
perm_coremember = 3
perm_graduate = 4
perm_president = 5

# edit personalinfo
users_editpersonalinfo_error = "ERROR : Edit personal info"
users_editpersonalinfo_success = "SUCCESS: Edit personal info"

# edit password
users_change_pwd_error = "ERROR : Change Password"
users_change_pwd_success = "SUCCESS : Change Password"
users_change_pwd_success_info = "Password was changed successfully.\n" + \
    "Please Log in again with your new password"
users_pwd_not_correct = "Password you entered is incorrect."


# password
users_pwd_at_least_6 = "User password length should be at least 6"
users_pwd_at_most_255 = "User password max length is 255"
users_pwd_no_numeric_char = "User password must contain numeric character"
users_pwd_no_alphabet_char = "User password must contain alphabet character"
users_pwd_no_special_char = "User password must contain special character"

# email
users_email_already_exist = "The user E-mail already exist"

# username
users_username_already_exist = "The user name already exist"
users_name_must_be_set = "User name must be set"
users_name_at_most_30 = "User name length is limited to 30.\n"
users_invalid_name = "User name should be Korean Character (or Alphabet)\n" +\
    "And it cannot contain special characters " + \
    "except for under bar_ , hyphen -"
users_username_does_not_exist = "Searched user name does not exist."

# contact number
users_invalid_contact_number = "Invalid contact number"

# update user
users_update_without_any_required_fields = \
    "Possible update field : username, email"
sers_update_is_admin_must_be_bool_type = \
    "The type of is_admin argument is must be bool"

# userperm
users_userperm_validation_error = "userperm is must be either 1,2,3,4,5"
# signup
users_signup_error = "ERROR : Sign Up"
users_signup_success = "SUCCESS : Sign Up"
users_signup_success_info = "You can login now"
users_exist_email = "The user email already exist"
users_invalid_email = \
    "Invalid Email.\n" + \
    "It must have user part and domain part between '@'\n" + \
    "Or It might contain invalid special character"
users_exist_name = "The user name already exist"
users_invalid_pwd = \
    "Invalid password.\n" + \
    "password length is in range 6 ~ 255\n" + \
    "And it should contain numeric character, alphabet character"
users_confirm_pwd_error = \
    "Password you entered is different with password confirmation.\n" + \
    "Please check password"

# login
users_login_error = "ERROR : Login"
users_login_success = "SUCCESS : Login"
users_non_exist_email = "The email does not exist. Please check Email"
users_login_success_info = "Successfully Login"
users_deactivated = "Deactivated User"
users_invalid = "Invalid email or password"
users_invalid_password = "Invalid user password"

# logout
users_logout_error = "ERROR : Logout"
users_logout_success = "SUCCESS : Logout"
users_logout_error_info = \
    "Logout failed. It seems you accessd the URL without Logged in"
users_logout_success_info = "Successfully Logout"
users_already_logged_in = "You are logging-in already"

# board
# create board
boards_max_number_of_boards = "Max number of boards : " + "10"
boards_name_must_be_set = "Board name must be set"
boards_name_at_most_30 = "Board name is limited to 30"

# get board
boards_board_arg_does_not_exist = "This board argument does not exist"

# createpost
# create post
boards_post_subject_must_be_set = "Subject must be set"
boards_post_subject_at_most_255 = "Subject is limited to 255"
boards_post_content_at_most_65535 = "Content is limited to 63335"

# create board posts
boards_board_arg_error = \
    "Board argument must be Board object"
boards_post_arg_error = \
    "Post argument must be Post object"

# write view
boards_write_error = "ERROR : Write Error"
boards_write_success = "SUCCESS : Write Success"
boards_write_success_info = "You posted successfully"
baords_anonymous_user_write = "Only logged-in user can write a text"
boards_access_perm = "You don't have the permission to access this board"
boards_writer_perm_error = "You cannot write in this board ( pemission )"

# board read permission
boards_read_error = "ERRROR : Read Error"
boards_read_error_info = \
    "You don't have permission to access this board and read posts"
oards_reader_perm_error = \
    "You cannot access this board and read posts( pemission )"

# search post
boards_search_post_error = "ERROR : Search specific posts"

# comment
boards_comment_error = "ERROR : Comment Error"
boards_comment_must_be_set = "Comment must be set"
boards_comment_at_most_255 = "Comment max length : 255"
boards_comment_post_does_not_exist = "The Post does not exist"
boards_comment_board_does_not_exist = "The Board does not exist"

# linkboard
linkboard_linkpost_invalid_writer_perm = \
    "You don't have permission to write in this board"
linkboard_read_error = "ERRROR : Read Error"
linkboard_anonymous_user_read = \
    "Only logged-in user can access this board and read posts"

# linkpost
linkboard_linkpost_success = "SUCCESS : Link Post"
linkboard_linkpost_error = "ERROR : Link Post"
linkboard_linkpost_invalid = "The URL is invalid"
linkboard_linkpost_unicode_error = "The URL has invalid domain part"

# delete comment
boards_delete_comment_error = "ERROR : Delete Comment"
boards_delete_comment_auth_error = \
    "You don't have permission to delete this comment"

boards_delete_post_error = "ERROR : Delete Post"
boards_delete_post_auth_error = \
    "You don't have permission to delete this post"

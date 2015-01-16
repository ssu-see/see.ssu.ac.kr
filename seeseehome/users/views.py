from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, request
from users.models import User
from seeseehome import msg
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.core.validators import validate_email
from django.core.urlresolvers import reverse
from django.contrib.auth import login as _login, logout as _logout
from django.contrib.auth.decorators import login_required
from boards.models import Board

# I couldn't solve built-in authenticate problem yet
# So I use custom authenticate(But It is almost same as built-in authenticate)
# It can authenticate username and email
def authenticate(username=None, password=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None        
    
    if user.check_password(password):
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        return user

def signin(request):
#	If is the user already logged in?

    if request.user.is_authenticated():
        messages.error(request, msg.users_login_error)
        messages.info(request, msg.users_already_logged_in)
        return HttpResponseRedirect(reverse("home"))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                _login(request, user)
                messages.success(request, msg.users_login_success)
                messages.info(request, msg.users_login_success_info)
    
                next = ""
                if 'next' in request.GET:
                    next = request.GET['next']
                
                if next == "" or next == "/":
                    return HttpResponseRedirect(reverse("home"))
                else:
                    return HttpResponseRedirect(next)
        else:
            messages.error(request, msg.users_login_error)
            messages.info(request, msg.users_invalid)
            return HttpResponseRedirect(reverse("users:singin"))
    else:
        next = ''
        if 'next' in request.GET:
            next = request.GET['next']
        boardlist = Board.objects.all()
        return render(request, "users/signin.html", {'next' : next, 
                'boardlist' : boardlist})

def logout(request):
    if request.user.__class__.__name__ is 'AnonymousUser':
        messages.error(request, msg.users_logout_error)
        messages.info(request, msg.users_logout_error_info)
    else:
        _logout(request)
        messages.success(request, msg.users_logout_success)
        messages.info(request, msg.users_logout_success_info)

    return HttpResponseRedirect(reverse("home"))

def signup(request):
    is_contact_number = False
    ### username
    if request.method == 'POST':
        username = request.POST['username']
#       username validator
        try:
            User.objects.validate_username(username)
        except ValidationError:
          messages.error(request, msg.users_signup_error)
          messages.info(request, msg.users_invalid_name)
          return HttpResponseRedirect(reverse("users:signup"))
        
#       username unique check
        try:
            User.objects.get(username = username)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_exist_name)
            return HttpResponseRedirect(reverse("users:signup"))
            
#       email
        email = request.POST['email']
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_invalid_email)
            return HttpResponseRedirect(reverse("users:signup"))
        
#       email unique check
        try:
            User.objects.get(email = email)
        except ObjectDoesNotExist:
            pass
        else:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_exist_email)
            return HttpResponseRedirect(reverse("users:signup"))
        
#       password
        password = request.POST['pwd']
        password_confirmation = request.POST['confirm_pwd']
        
        if password != password_confirmation:
            messages.error(request, msg.users_signup_error)
            messages.info(request, msg.users_confirm_pwd_error)
            return HttpResponseRedirect(reverse("users:signup"))
        else:
            try:
                User.objects.validate_password(password)
            except ValidationError:
                messages.error(request, msg.users_signup_error)
                messages.info(request, msg.users_invalid_pwd)
                return HttpResponseRedirect(reverse("users:signup"))
        
#       contact number
        if ('contact_number' in request.POST) and \
            (str(request.POST['contact_number']) != ""):
            contact_number = request.POST['contact_number']
            try:
                User.objects.validate_contact_number(contact_number)
            except ValidationError:
                messages.error(request, msg.users_signup_error)
                messages.info(request, msg.users_invalid_contact_number)
                return HttpResponseRedirect(reverse("users:signup"))
            else:
                is_contact_number = True

#       User Registration
        user = User.objects.create_user(username = username, email = email,
                                password = password)
        
        if is_contact_number:
            User.objects.update_user(user.id, contact_number = contact_number)

        messages.success(request, msg.users_signup_success)
        messages.info(request, msg.users_signup_success_info)
        return HttpResponseRedirect(reverse("users:signin"))

    boardlist = Board.objects.all()
    return render(request, "users/signup.html", {'boardlist' : boardlist})

@login_required
def personalinfo(request):
    boardlist = Board.objects.all()
    return render(request, "users/personalinfo.html", 
            {'boardlist' : boardlist})

@login_required
def editpersonalinfo(request):

    if request.method == 'POST':
        username = request.POST['username']

#       Is there difference in user name?        
        if (request.user.username != username) and \
          (str(username) != ""):
#          username validator
            try:
                User.objects.validate_username(username)
            except ValidationError:
              messages.error(request, msg.users_editpersonalinfo_error)
              messages.info(request, msg.users_invalid_name)
              return HttpResponseRedirect(reverse("users:editpersonalinfo"))

#           username unique check
            try:
                User.objects.get(username = username)
            except ObjectDoesNotExist:
                pass
            else:
                messages.error(request, msg.users_editpersonalinfo_error)
                messages.info(request, msg.users_exist_name)
                return HttpResponseRedirect(reverse("users:editpersonalinfo"))
        
            User.objects.update_user(
                request.user.id, 
                username = username
            )
           
#       email
        email = request.POST['email']
#       Is there difference in email?
        if (request.user.email != email) and ((str(email) != "")):
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, msg.users_editpersonalinfo_error)
                messages.info(request, msg.users_invalid_email)
                return HttpResponseRedirect(reverse("users:editpersonalinfo"))

#           email unique check
            try:
                User.objects.get(email = email)
            except ObjectDoesNotExist:
                pass
            else:
                messages.error(request, msg.users_editpersonalinfo_error)
                messages.info(request, msg.users_exist_email)
                return HttpResponseRedirect(reverse("users:editpersonalinfo"))
 
            User.objects.update_user(
                request.user.id, 
                email = email,
            )

#       contact number
        contact_number = request.POST['contact_number']
#       Is there difference in contact number
        if (request.user.contact_number != contact_number) and \
          ((str(contact_number) != "")):
            try:
                User.objects.validate_contact_number(contact_number)
            except ValidationError:
                messages.error(request, msg.users_editpersonalinfo_error)
                messages.info(request, msg.users_invalid_contact_number)
                return HttpResponseRedirect(reverse("users:editpersonalinfo"))
            else:
                User.objects.update_user(
                    request.user.id, 
                    contact_number = contact_number,
                )
        messages.success(request, msg.users_editpersonalinfo_success)
        return HttpResponseRedirect(reverse("users:personalinfo"))

    boardlist = Board.objects.all()
    return render(request, "users/editpersonalinfo.html", 
            {'boardlist' : boardlist})

@login_required
def editpassword(request):
    if request.method == 'POST':
#       password
        password = request.POST['pwd']
#       check present password
        if not request.user.check_password(password):
            messages.error(request, msg.users_change_pwd_error)
            messages.info(request, msg.users_pwd_not_correct)
            return HttpResponseRedirect(reverse("users:editpwd"))

#       check if new password is equal to new password confirmation
        new_password = request.POST['confirm_new_pwd']
        new_password_confirmation = request.POST['confirm_new_pwd']
        
        if new_password != new_password_confirmation:
            messages.error(request, msg.users_change_pwd_error)
            messages.info(request, msg.users_confirm_pwd_error)
            return HttpResponseRedirect(reverse("users:editpwd"))
        else:
#       check if new password is valid            
            try:
                User.objects.validate_password(new_password)
            except ValidationError:
                messages.error(request, msg.users_change_pwd_error)
                messages.info(request, msg.users_invalid_pwd)
                return HttpResponseRedirect(reverse("users:editpwd"))

#       set new password            
        request.user.set_password(new_password)
        request.user.save()
        _logout(request)
        messages.success(request, msg.users_change_pwd_success)
        messages.info(request, msg.users_change_pwd_success_info)
        return HttpResponseRedirect(reverse("users:singin"))

    boardlist = Board.objects.all()
    return render(request, "users/editpwd.html", {'boardlist' : boardlist})


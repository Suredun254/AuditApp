from django.shortcuts import render, redirect
from django.contrib import messages, auth 
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login,logout
from accounts.models import UserAccount
from django.conf import settings
from datetime import date


#account and email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here 

def signup(request):
    """
    This function allows users to sign up.

    :param request: This is the user request object.
    
    :return: renders an html page with content.
    """

    if request.method == 'POST':
            # Get form values
      
        email = request.POST['email'] 
        name = request.POST['name']
        password_one = request.POST['password_one']
        password_two = request.POST['password_two']

        # Check if passwords match
        if password_one == password_two:
                # Check username
                if UserAccount.objects.filter(email=email).exists():
                    messages.error(request, 'That Email is taken')
                    return redirect('accounts:signup')
                
                else:
                    # Looks good
                    user=UserAccount.objects.create_user(email=email, password=password_one,name=name,
                                                                )
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('accounts:login')
        else:
                messages.error(request, 'Passwords do not match')
                return redirect('accounts:signup')            

    return render(request, 'accounts/register.html')
      


def login(request):
    """
    This function handles the login logic.

    :param request: This is the user request object.
    
    :return: renders an html page with content.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
                    
            return redirect('audits:home') 
                     
        else:
            messages.error(request, 'Invalid credentials')
            message="Invalid credentials"
            context={
                        'message':message
                    }
            return render(request, 'accounts/login.html',context)
    else:
        print('here 45')
        
        return render(request, 'accounts/login.html')
 


def logout_view(request):
    """
    This function handles the log out logic.

    :param request: This is the user request object.
    
    :return: renders an html page with content.
    """
     #should use a post request typcally AND NOT A GET
    logout(request)
    messages.success(request, 'You are now logged out') 
    return redirect(reverse('accounts:login'))

      
      


def forgotPassword(request):
    """
    This function initializes the password reset process.

    :param request: This is the user request object.
    
    :return: renders an html page with content.
    """
    if request.method == 'POST':
        email = request.POST['email']
        if UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your FeedbackApp Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('accounts:forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    """
    This function validatesreset password link.

    :param request: This is the user request object.
    
    :return: renders an html page with content.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAccount._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('accounts:resetPassword')
    else:
        messages.error(request, 'This link has expired!')
        return redirect('accounts:login')

def resetPassword(request):
    """
    This function allows users to reset their passwords.

    :param request: This is the user request object.
    
    :return: renders an html page with content.
    """
    if request.method == 'POST':
        password = request.POST['password_one']
        confirm_password = request.POST['password_two']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = UserAccount.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('accounts:resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

       
def error_404_view(request,exception):
    """
    This function handles error 404.

    :param request: This is the user request object.
    :param exception: This is the pagr error.
    
    :return: renders an html page with content.
    
    
    """
    return render(request,'404.html')


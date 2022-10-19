from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.conf import Settings
from verify_email.email_handler import send_verification_email
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage  
from django.contrib import messages

MESSAGE_TAGS = {
    messages.INFO: '',
    50: 'critical',
}


# Create your views here.
emails_to_include = ["@metu.edu.tr"]

def register(response):
    
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            if form.cleaned_data.get("email").endswith("@metu.edu.tr"):
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()  
                # to get the domain of the current site  
                current_site = get_current_site(response)  
                mail_subject = 'Activation link has been sent to your email id'  
                message = render_to_string('verification/acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':account_activation_token.make_token(user),  
                })  
                to_email = form.cleaned_data.get('email')  
                email = EmailMessage(  
                            mail_subject, message, to=[to_email]  
                )  
                email.send() 
                messages.success(response, f"We have sent an email to ({to_email}) to verify your email adress and activate your account")
            else:
                messages.warning(response, f"Metu mail ile üye olmanız gerekmektedir ", extra_tags='danger')

    else:  
        form = RegisterForm()  

    return render(response, "register/register.html", {"form" : form})

def activate(response, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True
        user.save()  
        return render(response,'verification/Email.html',{'msg':'Thank you for your email confirmation. Now you can login your account.'})  
    else:  
        return render(response, 'verification/Email.html',{'msg':'Activation link is invalid!'})  

    
    


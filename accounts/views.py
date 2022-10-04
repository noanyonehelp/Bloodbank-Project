from time import sleep, time
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from app.models import BloodBank
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def signup(request):
    
    first_name = None
    last_name = None
    username = None
    email = None
    password = None
    
    if request.method == 'POST' and 'btnsignup' in request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'هذا البريد مستخدم من قبل.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'اسم المستخدم مستخدم من قبل.')
        else:
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                password = make_password(password=password),
            )
            user.save()
            messages.success(request, 'تم إنشاء الحساب بنجاح')
    context = {'title': 'إنشاء حساب جديد', 'first_name':first_name, 'last_name':last_name, 'email':email, 'username':username, 'password':password}
    return render(request, 'accounts/signup.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('bloodbanks')


def account_profile(request, id, username):
    bloodbankEXISTS = None
    bloodbank = None
    profileBlood = None
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.username in request.path:
        bloodbankEXISTS = BloodBank.objects.filter(user=request.user).exists()
        if bloodbankEXISTS:
            bloodbank = BloodBank.objects.get(user=request.user)
    user_adds = None
    user_profile = User.objects.get(id=id, username=username)

    if bloodbank is None:
        profileBlood = BloodBank.objects.get(user=user_profile)
    return render(request, 'accounts/account_profile.html', {'user_profile': user_profile, 'title': 'الصفحة الشخصية', 'user_adds': user_adds, 'bloodbankEXISTS':bloodbankEXISTS, 'bloodbank':bloodbank, 'alertMessage':'هل فعلا تريد حذف الحساب؟', 'profileBlood':profileBlood})

@login_required
def edit_account(request, id, username):
    user_account = User.objects.get(id=id, username=username)
    if request.method == 'POST':
        user_account.first_name = request.POST['fname']
        user_account.last_name = request.POST['lname']
        user_account.username = request.POST['username']
        user_account.email = request.POST['email']
        user_account.save()
        return render(request, 'partials/backto.html', {'user_profile': user_account, 'page':'عودة إلى الصفحة الشخصية', 'text':'تم تعديل البيانات بنجاح', 'title': 'الصفحة الشخصية', 'url': 'account_profile'})
    return render(request, 'accounts/edit-account.html', {'user_account': user_account})

def login_view(request):
    bloodbanks = BloodBank.objects.all()
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح')
        else:
            messages.error(request, 'خطأ في اسم المستخدم أو كلمة السر!')

    context = {'title':'تسجيل الدخول', 'bloodbanks':bloodbanks}
    return render(request, 'accounts/login.html', context)

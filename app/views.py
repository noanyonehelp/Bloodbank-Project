from urllib import response
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import redirect, render
from .models import BloodBank
from datetime import date
import time
from .forms import BloodBankCreationForm, CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

# Create your views here.

def bloodbanks(request):
    bloodbankEXISTS = None
    count = None
    bloodbanks = BloodBank.objects.all()
    latestBloodbanks = BloodBank.objects.all().order_by('-id')[:3]
    if bloodbanks is not None:
        count = BloodBank.objects.all().count()
    if request.user.is_authenticated and not request.user.is_anonymous:
        bloodbankEXISTS = BloodBank.objects.filter(user=request.user).exists()
    if 'deleteAll' in request.GET:
        bloodbanks = bloodbanks.delete()

    bloodbank_name = None
    count_search = None
    sort = None
    status = None
    countJoger = None
    countKorama = None
    countA1 = None
    countA2 = None
    countB1 = None
    countB2 = None
    countAB1 = None
    countAB2 = None
    countO1 = None
    countO2 = None
    count_three_filters = None
    sort_city = None
    sort_type = None
    sort_ready = None
    if request.method == 'GET' and 'three_filters' in request.GET:
        sort_city = request.GET.get('sort_city')
        sort_type = request.GET.get('sort_type')
        sort_ready = request.GET.get('sort_ready')
        bloodbanks = BloodBank.objects.filter(city=sort_city, type=sort_type, ready_to_donation=sort_ready)
        count_three_filters = bloodbanks.count()
        if sort_city is not None and sort_type is not None and sort_ready is not None:
            status = 'تم الفرز حسب منطقة: ' + sort_city + ', والفصيلة: ' + sort_type + ', و' + sort_ready + ' للتبرع، ' + 'وعدد نتائج البحث: ' + str(count_three_filters)

    if request.method == 'GET':
        sort = request.GET.get('sort')
        if sort == 'joger':
            bloodbanks = bloodbanks.filter(city='جوجر')
            countJoger = str(bloodbanks.filter(city='جوجر').count())
            status = 'تم الفرز حسب فصائل جوجر، وعدد الفصائل: ' + countJoger

        elif sort == 'korama':
            status = 'تم الفرز حسب فصائل ميت الكرماء'
            bloodbanks = bloodbanks.filter(city='ميت الكرماء')
            countKorama = str(bloodbanks.filter(city='ميت الكرماء').count())
            status = 'تم الفرز حسب فصائل ميت الكرماء، وعدد الفصائل: ' + countKorama

        elif sort == 'A+':
            status = 'تم الفرز حسب فصائل A+'
            bloodbanks = bloodbanks.filter(type='A+')
            countA1 = str(bloodbanks.filter(type='A+').count())
            status = 'تم الفرز حسب فصائل A+ ، وعدد الفصائل: ' + countA1


        elif sort == 'A-':
            status = 'تم الفرز حسب فصائل A-'
            bloodbanks = bloodbanks.filter(type='A-')
            countA2 = str(bloodbanks.filter(type='A-').count())
            status = 'تم الفرز حسب فصائل A- ، وعدد الفصائل: ' + countA2



        elif sort == 'B+':
            status = 'تم الفرز حسب فصائل B+'
            bloodbanks = bloodbanks.filter(type='B+')
            countB1 = str(bloodbanks.filter(type='B+').count())
            status = 'تم الفرز حسب فصائل B+ ، وعدد الفصائل: ' + countB1



        elif sort == 'B-':
            status = 'تم الفرز حسب فصائل B-'
            bloodbanks = bloodbanks.filter(type='B-')
            countB2 = str(bloodbanks.filter(type='B-').count())
            status = 'تم الفرز حسب فصائل B- ، وعدد الفصائل: ' + countB2



        elif sort == 'AB+':
            status = 'تم الفرز حسب فصائل AB+'
            bloodbanks = bloodbanks.filter(type='AB+')
            countAB1 = str(bloodbanks.filter(type='AB+').count())
            status = 'تم الفرز حسب فصائل AB+ ، وعدد الفصائل: ' + countAB1


        elif sort == 'AB-':
            status = 'تم الفرز حسب فصائل AB-'
            bloodbanks = bloodbanks.filter(type='AB-')
            countAB2 = str(bloodbanks.filter(type='AB-').count())
            status = 'تم الفرز حسب فصائل AB- ، وعدد الفصائل: ' + countAB2


        elif sort == 'O+':
            status = 'تم الفرز حسب فصائل O+'
            bloodbanks = bloodbanks.filter(type='O+')
            countO1 = str(bloodbanks.filter(type='O+').count())
            status = 'تم الفرز حسب فصائل O+ ، وعدد الفصائل: ' + countO1


        elif sort == 'O-':
            status = 'تم الفرز حسب فصائل O-'
            bloodbanks = bloodbanks.filter(type='O-')
            countO2 = str(bloodbanks.filter(type='O-').count())
            status = 'تم الفرز حسب فصائل O- ، وعدد الفصائل: ' + countO2

        elif sort == 'all':
            status = 'تم الفرز حسب جميع الفصائل'
            bloodbanks = BloodBank.objects.all()
            countAll = str(BloodBank.objects.all().count())
            status = 'تم الفرز حسب جميع الفصائل، وعدد الفصائل: ' + countAll


    today = date.today().year

    if 'search_bloodbank' in request.GET:
        bloodbank_name = request.GET['search_bloodbank']
    if bloodbank_name:
        bloodbanks = BloodBank.objects.filter(bloodbank_name__icontains=bloodbank_name)
        count_search = BloodBank.objects.filter(bloodbank_name__icontains=bloodbank_name).count()

     #Start Paginator
    bloodbanks_list = BloodBank.objects.all()
    paginator = Paginator(bloodbanks_list, 18)
    page = request.GET.get('page', 1)

    # Start Paginator After Search Query
    if bloodbanks:
        paginator = Paginator(bloodbanks, 18)
        page = request.GET.get('page')
        try :
            bloodbanks = paginator.page(page)
        except PageNotAnInteger:
            bloodbanks = paginator.page(1)
        except EmptyPage:
            bloodbanks = paginator.page(paginator.num_pages)
    # End Paginator After Search Query


    bloodbanks_list = paginator.get_page(page)
    try :
        bloodbanks = paginator.page(page)
    except PageNotAnInteger:
        bloodbanks = paginator.page(1)
    except EmptyPage:
        bloodbanks = paginator.page(paginator.num_pages)
    #End Paginator

    
    return render(request,'bloodbanks/bloodbanks.html',{"title": 'فصائل الدم', 'bloodbanks':bloodbanks, 'today':today, 'bloodbanks_list':bloodbanks_list, 'count':count, 'count_search':count_search, 'sort':sort, 'status': status, 'countA1':countA1, 'countJoger':countJoger, 'countKorama':countKorama, 'countA2': countA2, 'countB1':countB1, 'countB2':countB2, 'countAB1':countAB1, 'countAB2':countAB2, 'countO1':countO1,'countO2':countO2, 'sort_city':sort_city, 'sort_type': sort_type, 'sort_ready':sort_ready, 'count_three_filters':count_three_filters, 'latestBloodbanks':latestBloodbanks, 'bloodbankEXISTS':bloodbankEXISTS, 'bloodbank_name':bloodbank_name, 'alertMessage':'هل فعلا تريد حذف بيانات فصيلة الدم الخاصة بك؟'})


def bloodbank_profile(request, id):

    is_favourite = False
    is_like_bloodbank = False

    commentForm = CommentForm()
    profile = BloodBank.objects.get(id=id)

    total_likes = profile.total_likes()
    if profile.favourite.filter(id= request.user.id).exists():
        is_favourite = True

    if profile.likeBloodbank.filter(id= request.user.id).exists():
        is_like_bloodbank = True

    comments = profile.comments.all()

    # Calc Views Through Session Key
    session_key = 'view_profile_{}'.format(profile.id)
    if not request.session.get(session_key, False):

        profile.count_views = profile.count_views +1
        profile.save()
        request.session[session_key] = True
    

    new_comment = None
    if request.method == 'POST':
        from .models import Comment
        comment = request.POST.get('comment')
        new_comment = Comment.objects.create(
            comment = comment,
            bloodbank = profile,
            userProfile = request.user
            # bloodbank is the related field in Comment model

        )
        new_comment.save()
        
    return render(request, 'bloodbanks/profilebloodbank.html',{'profile':profile, 'title': profile.bloodbank_name, 'comments':comments, 'commentForm':commentForm, 'count_views':profile.count_views, 'is_favourite':is_favourite, 'is_like_bloodbank': is_like_bloodbank, 'total_likes':total_likes, 'alertMessage':'هل فعلا تريد حذف هذا التعليق؟'})

@login_required
def addnewbloodbank(request):
    form = BloodBankCreationForm()
    if request.method == 'POST':
        form = BloodBankCreationForm(request.POST)
        bloodbank = BloodBank.objects.create(
            bloodbank_name = request.POST.get('bloodbank_name'),
            bloodbank_addr = request.POST.get('bloodbank_addr'),
            mobile = request.POST.get('mobile'),
            type = request.POST.get('type'),
            city = request.POST.get('city'),
            user = request.user,
            last_donation = request.POST.get('last_donation'),
            ready_to_donation = request.POST.get('ready_to_donation')
        )
        bloodbank.save()
        return redirect('/#{}'.format(bloodbank.id))
    else:
        form = BloodBankCreationForm()
    return render(request, 'bloodbanks/addnewbloodbank.html', {'form': form, 'title':"تسجيل فصيلة دم جديدة"})

@login_required
def delete(request, id):

    bloodbank = BloodBank.objects.get(id=id)
    bloodbank.delete()
    return render(request, 'partials/deletedsuccess.html', {'url':'bloodbanks', 'page':'فصائل الدم'})

@login_required
def edit(request, id):

    bloodbank = BloodBank.objects.get(id=id)
    if request.method == 'POST':
        bloodbank.bloodbank_name = request.POST.get('bloodbank_name')
        bloodbank.bloodbank_addr = request.POST.get('bloodbank_addr')
        bloodbank.mobile = request.POST.get('mobile')
        bloodbank.last_donation = request.POST.get('last_donation')
        if 'type' in request.POST: bloodbank.type = request.POST.get('type')
        else: bloodbank.type = bloodbank.type

        if 'city' in request.POST: bloodbank.city = request.POST.get('city') 
        else: bloodbank.city = bloodbank.city

        if 'ready_to_donation' in request.POST: bloodbank.ready_to_donation = request.POST.get('ready_to_donation')
        else: bloodbank.ready_to_donation = bloodbank.ready_to_donation

        bloodbank.save()
        return redirect('/profile/{}'.format(bloodbank.id))


    return render(request, 'bloodbanks/editblood.html', {'bloodbank':bloodbank, 'title':'تعديل بيانات فصيلة الدم'})

@login_required
def favourite_bloodbank(request, id):
    is_favourite = False

    bb_obj = BloodBank.objects.get(id=id)
    if bb_obj.favourite.filter(id= request.user.id).exists():
        is_favourite = True
        bb_obj.favourite.remove(request.user)
    else:
        bb_obj.favourite.add(request.user)
    return HttpResponseRedirect(bb_obj.get_absolute_url())

@login_required
def bloodbank_favourite_list(request, username, id):

    user = request.user
    favourites_bloodbank = user.favourite.all()
    return render(request, 'bloodbanks/bloodbank_favourites_list.html', {'favourites_bloodbank':favourites_bloodbank, 'title': 'المفضلة'})


@login_required
def like_bloodbank(request, id):
    is_like_bloodbank = False
    bloodbank_obj = BloodBank.objects.get(id=id)
    if bloodbank_obj.likeBloodbank.filter(id= request.user.id).exists():
        is_like_bloodbank = True
        bloodbank_obj.likeBloodbank.remove(request.user)
    else:
        bloodbank_obj.likeBloodbank.add(request.user)
    return HttpResponseRedirect(bloodbank_obj.get_absolute_url())

@login_required
def bloodbank_like_list(request, username, id):
    
    user = request.user
    likes_bloodbank = user.likeBloodbank.all()
    return render(request, 'bloodbanks/bloodbank_likes_list.html', {'likes_bloodbank':likes_bloodbank, 'title': 'الإعجابات'})

def error404(request, exception):
    return render(request, 'partials/404.html', {'exception': exception})


def deleteCommentBloodbank(request, profileID, userID, commentID):
    from django.contrib.auth.models import User
    from .models import Comment
    profileID = BloodBank.objects.get(id=profileID)
    userID = User.objects.get(id=userID)
    commentID = Comment.objects.get(id=commentID)

    if request.method == 'GET':
        commentID.delete()
        return render(request, 'partials/deletedComment.html', {'profile':profileID, 'url': 'profilebloodbank', 'page': profileID.bloodbank_name})

    return render(request, 'partials/deletedComment.html', {'profile':profileID, 'url': 'profilebloodbank', 'page': profileID.bloodbank_name})


def editCommentBloodbank(request, bloodbankID, userID, commentID):
    from django.contrib.auth.models import User
    from .models import Comment
    bloodbankID = BloodBank.objects.get(id=bloodbankID)
    userID = User.objects.get(id=userID)
    commentID = Comment.objects.get(id=commentID)

    if request.method == 'POST':
        commentID.comment = request.POST.get('editcomment')
        commentID.save()

    return render(request, 'partials/editComment.html', {'profile':bloodbankID, 'page': 'فصيلة دم: '  + bloodbankID.bloodbank_name, 'comment':commentID, 'url': 'profilebloodbank'})
    
def deleteAccount(request, userID):
    
    userID = request.user.id
    logout(request)
    deleteUSer = User.objects.get(id=userID)
    deleteUSer.delete()
    return redirect('bloodbanks')
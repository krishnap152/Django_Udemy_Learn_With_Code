from django.shortcuts import render, HttpResponseRedirect, Http404
from .forms import EmailForm, JoinForm
from .models import Join
from django.conf import settings

# Create your views here.

def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META['REMOTE_ADDR']
    except:
        ip = ""
    return ip
import uuid

def get_ref_id():
    ref_id = str(uuid.uuid4())[:11].replace('-','').lower()
    try:
        id_exists = Join.objects.get(ref_id=ref_id)
        get_ref_id()
    except:
        return ref_id

def share(request,ref_id):
    #print(ref_id)
    try:
        join_obj = Join.objects.get(ref_id=ref_id)
        friends_referred = Join.objects.filter(friend=join_obj)
        #count = obj.count()
        count = join_obj.referral.all().count()
        ref_url = settings.SHARE_URL+ str(join_obj.ref_id)
        context = {"ref_id":join_obj.ref_id,"count":count,"ref_url":ref_url}
        template = "share.html"
        return render(request,template,context)
    #except Join.DoesNotExist:
     #   raise Http404
    except:
        raise Http404

def home(request):
    #print(request.META['REMOTE_ADDR'])
    #print(request.META['HTTP_X_FORWARDED_FOR'])
    # print(request.POST['email'])

    ## This is using regular django form
    # form = EmailForm(request.POST or None)
    # if form.is_valid():
    #     email = form.cleaned_data['email']
    #     new_join, created = Join.objects.get_or_create(email=email)
    #     print(new_join,created)
    #     print(new_join.timestamp)
    #     if  created:
    #         print("this object was created")


    try:
        join_id = request.session['join_id_ref']
        obj = Join.objects.get(id=join_id)
        print("the id is "+ str(obj.email))
    except:
        obj = None

    ## This is using model forms
    form  = JoinForm(request.POST or None)
    if form.is_valid():
        new_join = form.save(commit=False)
        email = form.cleaned_data['email']
        new_join_old,created = Join.objects.get_or_create(email=email)
        if created:
            
            new_join_old.ref_id = get_ref_id()
            if not obj == None:
                new_join_old.friend = obj
            new_join_old.ip_address=get_ip(request)
            new_join_old.save()
        #new_join.ip_address = get_ip(request)
        #new_join.save()
        ## printing all friends that joined as a result of main sharer
        #print(Join.objects.filter(friend=obj)).count()
        #print(Join.objects.all().filter(friend=obj)).filter(active=True)
        #print(obj.referral.all())
        return HttpResponseRedirect("/%s" %new_join_old.ref_id)

    context = {"form":form}
    template = "home.html"
    return render(request,template,context)



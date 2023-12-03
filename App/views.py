from django.shortcuts import render,redirect
from .models import PostModel,CategoryModel,CommentModel
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .forms import SingupForm




# Create your views here.
@login_required(login_url='login')
def postCreate(request):
    if request.method == "GET":
        category = CategoryModel.objects.all()
        return render(request,'postCreate.html',{'category':category})
    if request.method == "POST":
        category_id = request.POST.get('category')
        newcat = request.POST.get('newcat')
        if category_id != 'none':
            category = CategoryModel.objects.get(id=category_id)
        elif newcat != '':
            category, created = CategoryModel.objects.get_or_create(name=newcat)
        else:
            category = None

        posts = PostModel.objects.create(
            category=category,
            title=request.POST.get('title'),
            body= request.POST.get('body'),
            created_at=datetime.now(),
            image = request.FILES.get('image'),
            author_id = request.user.id
            )
            
        
        posts.save()
        messages.success(request, "The post has been CREATED successfully.")
        return redirect('/')

def Home(request):
    people = User.objects.all()
    cat = request.GET.get('category')
    if cat == None:
        posts = PostModel.objects.all().order_by('-created_at')
    else:
        posts = PostModel.objects.filter(category__name__contains=cat).order_by('-created_at')

    category = CategoryModel.objects.all()

    return render(request, 'home.html', {'posts':posts,'categories':category,'people':people})

def postDetail(request,post_id):
    post = PostModel.objects.get(id=post_id)
    user = User.objects.get(id=post.author_id)
    comments = CommentModel.objects.filter(post_id = post_id)
    context = {'post':post,'author':user,'comments':comments}
    return render(request, 'postDetail.html',context)

    
@login_required(login_url='login')
def postUpdate(request, post_id):
    if request.method == 'GET':
        post = PostModel.objects.get(id=post_id)
        post.created_at =  post.created_at.strftime('%Y-%m-%dT%H:%M')
        category = CategoryModel.objects.all()
        return render(request, 'postUpdate.html',{'post':post,'category':category})
    if request.method == 'POST':
        post = PostModel.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.created_at = datetime.now()
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.save()
        messages.info(request, "The post has been UPDATED successfully.")
        return redirect('/')
        
@login_required(login_url='login')
def postDelete(request,post_id):
    post = PostModel.objects.get(id=post_id)
    if post.image:
        post.image.delete()
    if post.body:
        post.delete()
    messages.error(request, "The post has been DELETED successfully.")
    return redirect('/')
        
# ABOVE IS CRUD 

# LOGIN STUFF 

def signin(request):
    if request.method=='GET':
        return render(request,'login.html')
    if request.method=='POST':
        user = request.POST.get('username')
        pas  = request.POST.get('password')
        loger =authenticate(username=user,password=pas)
        print(loger)
        # return render(request,'login.html')
        if loger:
            login(request,loger)
            messages.success(request, "You are now logged in as "+ user)
            return redirect('/')
        else:   
            messages.error(request, "Username or Password is incorrect!")
            return render(request,'login.html')
            


def singout(request):
    logout(request)
    return redirect('/login/')


def register(request):
    form = SingupForm()
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            user = request.POST.get('username')
            pas  = request.POST.get('password2')
            form.save()
            loger =authenticate(username=user,password=pas)
            if loger:
                login(request,loger)
                messages.success(request, "You are now logged in as "+ user)
                return redirect('/')

    return render(request,'register.html',{'form':form})



# LOGIN STUFF 

def cmtcreate(request,post_id):
    if request.method == 'POST':
        post = PostModel.objects.get(id=post_id)
    
        comment = CommentModel.objects.create(
            content=request.POST.get('content'),
            author_id = request.user.id,
            post_id = post_id,
            created_at = datetime.now()
        )
        comment.save()
        messages.success(request, f"{comment.author} Commented on {post.author}'s post")
        return redirect('/detail/' + str(post_id) +'/')



def cmtupdate(request, cmt_id, post_id):
    if request.method=='GET':
        comment = CommentModel.objects.get(id=cmt_id)
        post = PostModel.objects.get(id=post_id)
        print(comment)
        return render(request, 'cmtUpdate.html',{'comment':comment,'post':post})
    if request.method == 'POST':
        comment = CommentModel.objects.get(id=cmt_id)
        comment.content = request.POST.get('content')
        comment.save()
        return redirect('/detail/' + str(post_id) +'/')


def cmtdelete(request,cmt_id,post_id):
    comment = CommentModel.objects.get(id=cmt_id)
    comment.delete()
    return redirect('/detail/' + str(post_id) +'/')

def search_by(request):
    search = request.GET.get('search')
    if search:
        posts = PostModel.objects.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
            )
        return render(request, 'home.html', {'posts': posts})
    else:
        posts = PostModel.objects.all().order_by('-created_at')




# profile 
def profile(request,id):
    user = User.objects.get(id=id)
    visitor = request.GET.get('visitor')
    posts = PostModel.objects.filter(author=id)
    return render(request, 'profile.html',{'user':user,'posts':posts,'visitor':visitor})


def editprofile(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method=='POST':
        user.username = request.POST.get('name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('/profile/'+str(user_id) +'/')
    return render(request, 'editprofile.html',{'user':user})


    


# profile 

from django.shortcuts import render ,HttpResponse ,redirect,reverse
from .models import contact , post , postComments , Profile ,Category
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .tamplettags import extras
from django.views.generic import CreateView ,UpdateView,DeleteView
from django.core.files.storage import FileSystemStorage
from .forms import  UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.mixins import  LoginRequiredMixin , UserPassesTestMixin
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    return render(request,'index.html')


def home(request):
    posts = post.objects.all().order_by('-timeStamp')
    category = Category.objects.all()
    paginator = Paginator(posts,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html',{'page_obj':page_obj,'category':category})

def search(request):
    category = Category.objects.all()
    query = request.GET['q']
    ids = Category.objects.filter(name=query.upper()).first()
    if len(query)>78:
        posts = []
    else:
        posts = (post.objects.filter(title__icontains=query)) or (post.objects.filter(content__icontains=query)) or (post.objects.filter(category=ids))
    return render(request,'search.html',{'posts':posts,'query':query,'category':category})


def category(request,cate):
    category = Category.objects.all()
    id = Category.objects.filter(name=cate).first()
    if Category.objects.filter(name=cate).exists():
        pos = post.objects.filter(category=id)
    else:
        return render(request,'404.html')
    return render(request,'category.html',{'pos':pos,'cate':cate,'category':category})

class PostCreateView(CreateView):
    model = post
    fields = ['title','content','img','category','slug']
    template_name = 'ask-questions.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title','content','img','category','slug']
    template_name = 'ask-questions.html'
    

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = post
    template_name = 'delete-post.html'
    success_url = '/home/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def Contact(request):
    
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        if len(name)<2 or len(email)<5 or len(content)<10:
            messages.error(request,"Please fill the form correctly ")
        else:
            contac = contact(name=name,email=email,content=content)
            contac.save()
            messages.success(request,"Thanku for submission")
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def signin(request):
    if request.method == "POST":
        loginuser = request.POST['userlogin']
        psw = request.POST['loginpsw']
        user = authenticate(username=loginuser,password=psw)
        if user is not None:
            login(request,user)
            messages.success(request,"Succesfull Login")
            return redirect('home')
        else:
            messages.error(request,"Please check Creadentials")
            
    return render(request,"signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        psw = request.POST['psw']
        psw2 = request.POST['psw2']
        if (username == '')or (fname == "")or(lname == "")or(email == "")or(psw == "")or(psw2 == ""):
            messages.error(request,"Please fill the from correctly")
        elif psw != psw2:
            messages.error(request,"Both Password Does't Matched")
        elif User.objects.filter(username=username).exists():
            messages.error(request,"Username Already Used please choose differen username")
        elif User.objects.filter(email=email).exists():
            messages.warning(request,"You are already member please login")
            return redirect('signup')
        else:
            myuser = User.objects.create_user(username=username,email=email,first_name=fname,last_name=lname,password=psw)
            myuser.save()
            return redirect('signin')
    return render(request, 'signup.html')

def notAvailable(request,slug):
    return render(request,'404.html')

def posts(request,slug):
    if post.objects.filter(slug=slug).exists():
        pos = post.objects.filter(slug=slug).first()
        use = User.objects.filter(username=pos.author).first()
    else:
       return render(request,'404.html')
    comments = postComments.objects.filter(postcomment=pos,parent=None).order_by("-timestamp")
    replies = postComments.objects.filter(postcomment=pos).exclude(parent=None).order_by("-timestamp")
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    likes = postComments.objects.all()
    dislike = postComments.objects.all()
    return render(request, 'posts.html',{'pos':pos,'use':use,'comments':comments,'likes':likes,'dislike':dislike,'replyDict':replyDict})




def logouthandel(request):
    logout(request)
    messages.success(request,"Successfully Logout")
    return redirect('home')

def profile(request,username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request,f"  Account Updated")
            return redirect(f'../profile/{request.user}')
    else:
        u_form =UserUpdateForm(instance=request.user)
        p_form =ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    if User.objects.filter(username=username).exists():
        profile = User.objects.filter(username=username).first()
    elif username == '':
        profile = User.objects.filter(username=request.user).first()
    else:
        messages.error(request,f"User {username} not available please create your account.")
        return redirect('signup')
    return render(request,'profile.html',{'context':context,'profile':profile,'username': username})

def blogComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get("postSno")
        posta = post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comments = postComments(comment=comment,user=user,postcomment=posta)
            comments.save()
        else:
            parent = postComments.objects.get(sno=parentSno)
            comments = postComments(comment=comment,user=user,postcomment=posta,parent=parent)
            comments.save()
        messages.success(request,"Your comment is added")
    return redirect(f'/{posta.slug}')

def document(request):
    return render(request,'documentations.html')


def license(request):
    return render(request,'license.html')

def privacy(request):
    return render(request,'privacy.html')





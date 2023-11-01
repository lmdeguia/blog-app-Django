from django.shortcuts import render

from blog.forms import UserForm, UserMediaForm, PostForm, CommentForm
from blog.models import Post, Comment, UserMedia

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')


def post_list(request):
    post = Post.objects.filter(draft__exact=False).order_by('-created_date')
    return render(request, 'blog/post_list.html', {'post':post})





def post_detail(request, pk):
    post = Post.objects.get(pk__exact=pk)
    media = UserMedia()
    try:
        comments = Comment.objects.filter(post__exact=pk)
    except:
        comments = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid() and 'comment' in request.POST:
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return HttpResponseRedirect(request.path_info)
        elif 'publish' in request.POST:
            temp = not post.draft
            post.draft = temp
            post.save()
            return HttpResponseRedirect(reverse('blog:post_list'))
        elif 'delete' in request.POST:
            post.delete()
            return HttpResponseRedirect(reverse('blog:post_list'))
        elif 'del_comment' in request.POST:
            dic1 = request.POST
            cpk = int(dic1['del_comment'])
            target = Comment.objects.get(id__exact=cpk)
            target.delete()
            print('del button was pressed')
        elif 'update_comment' in request.POST:
            dic3 = request.POST
            cpk = int(dic3['update_comment'])
            comment = comments.get(id__exact=cpk)
            comment.text = str(request.POST['text'])
            print(f'After: {str(comment.text)}')
            comment.save()
            print('comment saved!')
            return HttpResponseRedirect(request.path_info)
        elif 'edit_comment' in request.POST:
            dic2 = request.POST
            edit = True
            cpk = int(dic2['edit_comment'])
            print(f'edit button was pressed: \n {dic2} id={cpk}')
            instance = Comment.objects.get(id__exact=cpk)
            update = CommentForm(instance=instance)
            return render(request, 'blog/post_detail.html', 
            {'post':post, 'form':form, 'comments':comments,
             'request':request, 'edit':edit, 'update':update, 
             'media':media, 'cpk':cpk})
        elif 'reply_comment' in request.POST:
            dic4 = request.POST
            cpk_target, author_target = dic4['reply_comment'].split(', ')
            cpk_target = int(cpk_target)
            replying = True
            commentform = CommentForm()
            return render(request, 'blog/post_detail.html',
            {'post':post, 'form':form, 'comments':comments, 
            'request':request, 'media':media, 'replying':replying, 
            'cpk_target':cpk_target, 'commentform':commentform})
        elif form.is_valid() and 'submit_reply' in request.POST:
            dic5 = request.POST
            cpk_target = int(dic5['submit_reply'])
            target_comment = comments.get(id__exact=cpk_target)
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.replyto_id = target_comment
            comment.replyto_text = target_comment.text
            comment.save()
            return HttpResponseRedirect(request.path_info)

    else:
        form = CommentForm() 
    return render(request, 'blog/post_detail.html',
    {'post':post, 'form':form, 'comments':comments, 
    'request':request, 'media':media})
    


def edit_post(request, pk):
    post = Post.objects.get(pk__exact=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        if 'delete' in request.POST:
            post.delete()
            return HttpResponseRedirect(reverse('blog:post_list'))
        elif 'update' in request.POST:
            update = PostForm(instance=post, data=request.POST)
            update.save(commit=True)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'blog/edit_post.html', {'post':post, 'form':form})



def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        media_form = UserMediaForm(data=request.POST)

        if user_form.is_valid() and media_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = media_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            
            profile.save()

            registered = True
        else:
            print(user_form.errors, media_form.errors)

    else:
        user_form = UserForm()
        media_form = UserMediaForm()

    return render(request, 'blog/registration.html', 
                {'user_form':user_form, 
                'media_form':media_form,
                'registered':registered})



def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Failed login attempt using the following credentials:")
            print(f"Username: {username} and password: {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'blog/login.html', {})




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



@login_required
def profile_page(request, user):
    user_obj = User.objects.get(username__exact=user)
    posts = Post.objects.filter(author__exact=user_obj).order_by("-created_date")
    comments = Comment.objects.filter(author__exact=user_obj).order_by("-created_date")
    return render(request, 'blog/profile_page.html', {'posts':posts, 'comments':comments, 'user':user_obj})



@login_required
def new_user_post(request):
    post_form = PostForm()
    if request.method == 'POST':
        filled_form = PostForm(request.POST)

        if filled_form.is_valid():
            post = filled_form.save(commit=False)
            post.author = request.user
            if 'draft' in request.POST:
                post.draft = True
                post.save()
                return HttpResponseRedirect(reverse('blog:view_draft'))
            elif 'publish' in request.POST:
                post.draft = False
                post.publish()
                post.save()
                return HttpResponseRedirect(reverse('blog:post_list'))
                      

    return render(request, 'blog/new_post.html', {'post_form':post_form})


@login_required
def view_user_draft(request):
    post = Post.objects.filter(draft__exact=True).filter(author__exact=request.user.pk)
    return render(request, 'blog/post_draft.html', {'post':post})
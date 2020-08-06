from django.shortcuts import render,redirect, get_object_or_404
from .models import Blog, Comment

# Create your views here.
def main(request):
    blog = Blog.objects.all().order_by('-id')
    return render(request, 'main.html', {'blog':blog})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comment=Comment.objects.filter(post=blog.id)
    return render(request, 'detail.html', {'blog':blog, 'comment':comment})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.user = request.user
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.save()
    return redirect('/detail/'+str(blog.id))

def renew(request, blog_id):
    blog = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'renew.html', {'blog':blog})

def update(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.save()
    return redirect('/detail/'+ str(blog.id))

def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/')

def comment_create(request, blog_id):
    if request.method=='POST':
        comment = Comment()
        comment.user = request.user
        comment.post = Blog.objects.get(id=blog_id)
        comment.content = request.POST['comment']
        anonymous = request.POST.get('anonymous', True)
        if anonymous=="y":
            comment.anonymous=False
        comment.save()
        return redirect('/detail/'+str(blog_id))

def delete_comment(request, blog_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect('/detail/'+str(blog_id))
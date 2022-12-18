from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import  HttpResponse, Http404
# Create your views here.
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import  send_mail
from taggit.models import Tag

from django.views.decorators.http import require_POST

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])
    paginator = Paginator(posts_list, 2)
    page_number = request.GET.get("page", 1)
    try:
        posts =paginator.page(page_number)
    except PageNotAnInteger:
        posts =paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
    #try:
    #    post = Post.published.get(id=id)
    #except Post.DoesNotExist:
   #     raise Http404("No post found")

    post = get_object_or_404(Post,  status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug = post
                             )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    return  render(request, "blog/post/detail.html", {"post": post, "form": form, "comments": comments})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recomienda que leas {post.title}"
            message = f"Read {post.title} at {post_url}"
            send_mail(subject, message, "admin@gmail.com", [f"{cd['to']}"])
            sent=True
    else:
        form = EmailPostForm()
    return  render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, "blog/post/comment.html", {"post": post, "form": form, "comment": comment})
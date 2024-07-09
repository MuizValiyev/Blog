from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Post, Coment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmilPostForm, ComentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from taggit.models import Tag
from django.db.models import Count

def post_list(request, tag_slug=None):
    post = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])

    paginator = Paginator(post, 3)
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(1)
    context = {
        'posts':posts
    }
    return render(request, 'main/posts/list.html', context)


def post_detail(request, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post)
    
    comments = post.comments.filter(active=True)
    form = ComentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request, 'main/posts/detail.html', {'post':post, 'comments':comments, 'form':form, 'similar_posts': similar_posts })

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmilPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comment']}"
            html_message = render_to_string('main/emailPost.html', {
                'post': post,
                'post_url': post_url,
                'name': cd['name'],
                'comments': cd['comment']
            })
            send_mail(subject, message, 'valiyevmuiz0407@gmail.com', [cd['to']], html_message=html_message)
            sent = True
    else:
        form = EmilPostForm()
    return render(request, 'main/posts/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = ComentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'main/posts/comment.html', {'post': post, 'form': form, 'comment': comment})
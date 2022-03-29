from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from taggit.models import Tag

from blog.forms import CommentForms, ShareForm, SearchForm
from blog.models import Post

"""
to do :
    * simple test 
    * create sample
    * ściągnięcie tekstu w Txt 
    * audio słuchanie 
"""

def post_list(request, tag_slug=None):
    objects_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        objects_list = objects_list.filter(tags__in=[tag])
    #paginator
    paginator = Paginator(objects_list, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts,
                  'page': page, 'tag':tag })

def post_detai(request, category, id):
    post = get_object_or_404(Post,
                              category=category,
                              id=id)
    #comments
    comments = post.comments.filter(active=True)

    #POST COMMENT
    if request.method == 'POST':
        comment_form = CommentForms(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForms()

    # similar post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]




    return render(request, 'blog/post/detail.html', {
                                                    'post': post,
                                                    'similar_posts': similar_posts,
                                                    'comments': comments,
                                                    'comment_form': comment_form,
                                                })


def post_share(request, category, post_id):
    post = get_object_or_404(Post, id= post_id,
                             category=category)
    sent = False
    if request.method == 'POST':
        share_form = ShareForm(request.POST)
        if share_form.is_valid():
            cd = share_form.cleaned_data
        # email text
        post_url = request.build_absolute_uri( post.get_absolute_url() )
        subject = '{} recommend you read "{}"'.format(cd['name'], post.title)
        message = "Could you read this article '{}' for this page: {}\n\nExtra comment for {}: \n{}"\
            .format(post.title, post_url, cd['name'], cd['message'])
        send_mail(subject,
                  message,
                  'tester19spam@wp.pl',
                  [cd['to']],
                  fail_silently=False)
        sent = True
        # if sent:
        #     return HttpResponse("<h2>Thank you for support us ;)\n Message was send </h2>")
    else:
        share_form = ShareForm()
    return render(request, "blog/post/share.html", {"post": post,
                                                    "form": share_form,
                                                    "sent": sent})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(
                Q(title__contains= query) |
                Q(body__contains=query)
            )
    return render(request, "blog/post/search.html", {"form": form,
                                                     'query': query,
                                                     "results": results})




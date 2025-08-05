from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from blogApp.models import postModel,commentModel
from blogApp.forms import postForm,commentForm
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import openai
from django.http import JsonResponse,HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

# Create your views here.
class aboutView(TemplateView):
    template_name='blogApp/about.html'


class postListView(ListView):
    model = postModel
    context_object_name = 'posts'
    def get_queryset(self):
        return postModel.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')

class postDetails(DetailView):
    model = postModel
    context_object_name = 'post_detail'

class createPost(LoginRequiredMixin,CreateView):
    login_url ='login/'
    redirect_field_name = 'blogApp/post_detail.html'
    form_class = postForm
    model = postModel

class updatePost(LoginRequiredMixin,UpdateView):
    login_url ='login/'
    redirect_field_name = 'blogApp/post_detail.html'
    form_class = postForm
    model = postModel
    
class deletePost(DeleteView):
    model = postModel
    success_url = reverse_lazy('blog_app:post-list')

class draftListView(LoginRequiredMixin,ListView):
    login_url ='login/'
    redirect_field_name = 'blogApp/post_detail.html'
    model = postModel

    def get_queryset(self):
        return postModel.objects.filter(publish_date__isnull=True).order_by('created_date')
    template_name = 'blogApp/draft_list.html' 
    context_object_name='drafts'


# Function Based Views For All The Actions


def add_comment_post(request,pk):
    if request.method == 'POST':
        post = get_object_or_404(postModel,pk=pk)
        form = commentForm(request.POST)
        if(form.is_valid()):
            comment = form.save(commit=False)
            comment.post     = post
            comment.save()
            return redirect('blog_app:post-detail',pk=pk)

    else:
        form = commentForm()
    return render(request,'blogApp/commentmodel_form.html',{'form':form})

@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(commentModel,pk=pk)
    comment.approve()
    return redirect('blog_app:post-detail',pk=comment.post.pk)

@login_required
def reject_comment(request,pk):
    comment = get_object_or_404(commentModel,pk=pk)
    post_id = comment.post.pk
    comment.delete()
    return redirect('blog_app:post-detail',pk=post_id)

@login_required
def publish_post(request,pk):
    post = get_object_or_404(postModel,pk=pk)
    post.publish()
    return redirect('blog_app:post-list')

#OPEN AI API INTEGRATE
openai.api_key = settings.OPENAI_API_KEY


def chat_page(request):
    # Just render the chat page template (GET)
    return render(request, 'blogApp/chat.html')

@csrf_exempt
def chat_with_gpt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

          

            response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

            reply = response.choices[0].message.content
            return JsonResponse({'reply': reply})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # Return 405 Method Not Allowed for other HTTP methods
        return HttpResponseNotAllowed(['POST'])
   
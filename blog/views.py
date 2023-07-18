from django.shortcuts import render, get_object_or_404

# Create your views here.

def homepage(request):
    return render(request, 'blog/base.html')
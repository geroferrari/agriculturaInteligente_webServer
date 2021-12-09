from django.shortcuts import render
from irrigation.models import Post

def irrigation(request):
    return render(request, "irrigation/irrigation.html", {"posts": posts})
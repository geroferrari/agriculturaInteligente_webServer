from django.shortcuts import render

def dashboards(request):
    return render(request, "dashboards/dashboards.html", {"posts": posts})
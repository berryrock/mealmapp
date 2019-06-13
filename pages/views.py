from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Page

def main_page(request, pk):
	page = get_object_or_404(Page, pk=pk)
	return render(request, 'pages/main_page.html', {'page': page})
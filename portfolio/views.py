from django.shortcuts import render
from django.views.generic import TemplateView
from portfolio.models import AboutMe, Education, Experience


def index(request):
    return render(request, 'index.html')


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_me'] = AboutMe.objects.select_related('user').first()
        context['experiences'] = Experience.objects.filter(about_me=context['about_me'])
        context['education'] = Education.objects.filter(about_me=context['about_me'])
        return context
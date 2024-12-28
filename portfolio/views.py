from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from portfolio.models import AboutMe, Education, Experience, Project
from portfolios import settings


def index(request):
    return render(request, 'index.html')


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_me'] = AboutMe.objects.select_related('user').first()
        context['experiences'] = Experience.objects.filter(about_me=context['about_me']).order_by('-id')
        context['educations'] = Education.objects.filter(about_me=context['about_me'])
        return context

class CredentialsView(TemplateView):
    template_name = 'credentials.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_me = AboutMe.objects.select_related('user').first()

        context['about_me'] = about_me
        context['experiences'] = Experience.objects.filter(about_me=about_me) if about_me else []
        context['educations'] = Education.objects.filter(about_me=about_me) if about_me else []
        context['social_media'] = about_me.social_media if about_me else {}
        context['skills'] = about_me.skills.all() if about_me else []
        return context


class WorksView(ListView):
    model = Project
    template_name = 'works.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.prefetch_related('images').order_by('year')


class WorkDetailView(DetailView):
    model = Project
    template_name = 'work_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.prefetch_related('images').order_by('year')
    
    def get_object(self, queryset = None):
        slug = self.kwargs.get('slug')
        try:
            return Project.objects.prefetch_related('images').get(slug=slug)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_me = AboutMe.objects.select_related('user').first()

        context['about_me'] = about_me
        context['social_media'] = about_me.social_media if about_me else {}
        return context
    
    def post(self, request):
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        bot_token = settings.BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        telegram_message = (
            f"**New Contact Message**\n\n",
            f"Name: {full_name}\n",
            f"Email: {email}\n",
            f"Message: {message}"
        )
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": telegram_message,
            'parse_mode': 'HTML'
        }
        response = request.post(url, data=payload)

        if response.status_code == 200:
            message.success(request, "Your message has been sent successfully")
        else:
            message.error(request, "Failed to send your message. Please try again later")
        return render('/')
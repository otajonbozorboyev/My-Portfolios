from portfolio.models import AboutMe

def global_about_context(request):
    return {
        'abouts': AboutMe.objects.all()
    }

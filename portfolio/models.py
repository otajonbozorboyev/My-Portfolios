from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from tinymce.models import HTMLField


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'


class AboutMe(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about_me = HTMLField(null=True, blank=True, help_text = "Write something about yourself")
    image = models.ImageField(upload_to='about_me/image', blank=True, null=True)
    skills = models.ManyToManyField("Skill", blank=True, null=True, help_text='Add your skills')
    my_name = models.CharField(max_length=100, help_text="Enter your name")
    job = models.CharField(max_length=100, help_text="Enter your job. E.g.: Software Engineer")
    social_media = models.JSONField(null=True, blank=True, help_text="Add your social media links")

    def __str__(self):
        return self.my_name


class Education(models.Model):
    about_me = models.ForeignKey(AboutMe, on_delete=models.CASCADE)
    start_year = models.CharField(max_length=4, help_text="Enter the start year, E.g.: 2005")
    end_year = models.CharField(max_length=4, help_text="Enter the end year, E.g.: 2009")
    degree = models.CharField(max_length=100, help_text="Enter the degree, E.g.: Bachelor of Science")
    university = models.CharField(max_length=100, help_text="Enter the university, E.g.: University of Science")
    description = HTMLField(help_text="Write something about your education, E.g.: Bachelor of Computer Science")

    def __str__(self):
        return f"{self.degree} at {self.university} ({self.start_year}-{self.end_year})"


class Experience(models.Model):
    about_me = models.ForeignKey(AboutMe, on_delete=models.CASCADE)
    start_year = models.CharField(max_length=4, help_text="Enter the start year, E.g.: 2005")
    end_year = models.CharField(max_length=4, help_text="Enter the end year, E.g.: 2009")
    position = models.CharField(max_length=100, help_text="Enter the position, E.g.: Software Engineer")
    company = models.CharField(max_length=100, help_text="Enter the company, E.g.: Google")
    description = HTMLField(help_text="Write something about your experience, E.g.: Worked on Google Search Engine")

    def __str__(self):
        return f"{self.position} at {self.company} ({self.start_year}-{self.end_year})"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Enter the skill name, E.g.: Python")

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100, help_text="Enter the project title")
    year = models.CharField(max_length=4, help_text="Enter the year")
    client = models.CharField(max_length=100, help_text="Enter the client name")
    service = models.CharField(max_length=100, help_text="Enter the service name")
    project_type = models.CharField(max_length=50, help_text="Enter the project type, E.g.: Web Development")
    description = HTMLField(blank=True, null=True, help_text="Write something about the project")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug} - {counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.year})"


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project/image', help_text="Upload project image")

    def __str__(self):
        return f"Image for {self.project.title}"


class YoutubeVideo(models.Model):
    title = models.CharField(max_length=100, help_text="Enter the video title")
    link = models.URLField(help_text="Enter the video link")
    thumbnail = models.ImageField(upload_to='image/youtube_thumbnail', help_text="Enter the video thumbnail")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=100, help_text="Enter the service. E.g.: Web Development Service")
    description = models.TextField()
    icon = models.ImageField(upload_to='images/services', help_text="Enter the service icon")

    def __str__(self):
        return self.title



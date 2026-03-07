from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=120)
    headline = models.CharField(max_length=180)
    summary = models.TextField()
    tagline = models.CharField(max_length=120, blank=True)
    about = models.TextField(blank=True, help_text="Extended About Me paragraph shown in the About section.")

    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    photo = models.ImageField(upload_to="profile/", blank=True, null=True)
    cv_file = models.FileField(upload_to="cv/", blank=True, null=True)

    def __str__(self):
        return self.full_name


class Experience(models.Model):
    EMPLOYMENT_TYPES = [
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Contract", "Contract"),
        ("Internship", "Internship"),
        ("Freelance", "Freelance"),
    ]

    title = models.CharField(max_length=150)
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES, blank=True)
    company = models.CharField(max_length=150)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)

    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.company}"


class Education(models.Model):
    program = models.CharField(max_length=150)
    school = models.CharField(max_length=150)
    start_year = models.CharField(max_length=10)
    end_year = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.program} - {self.school}"


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    link = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to="projects/", blank=True, null=True)

    tech_stack = models.CharField(max_length=200, blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)

    featured = models.BooleanField(default=False)
    created_at = models.DateField(blank=True, null=True)

    @property
    def tech_list(self):
        return [t.strip() for t in (self.tech_stack or "").split(",") if t.strip()]

    def __str__(self):
        return self.title


class Skill(models.Model):
    SKILL_TYPES = [
        ("Technical", "Technical"),
        ("Security", "Security"),
        ("Soft", "Soft"),
    ]

    name = models.CharField(max_length=80)
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES, default="Technical")

    def __str__(self):
        return self.name


class Certificate(models.Model):
    title = models.CharField(max_length=150)
    issuer = models.CharField(max_length=120, blank=True)
    year = models.CharField(max_length=10, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=120, blank=True)
    organization = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.organization}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.email})"
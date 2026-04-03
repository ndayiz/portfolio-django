import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Profile, Experience, Education, Project,
    Skill, Certificate, Testimonial, ContactMessage
)


def _company_duration(roles):
    earliest = min(r.start_date for r in roles)
    latest = max((r.end_date if r.end_date else datetime.date.today()) for r in roles)
    months = (latest.year - earliest.year) * 12 + (latest.month - earliest.month) + 1
    if months < 1:
        return "< 1 mo"
    years, mos = divmod(months, 12)
    if years and mos:
        return f"{years} yr {mos} mo{'s' if mos > 1 else ''}"
    if years:
        return f"{years} yr{'s' if years > 1 else ''}"
    return f"{mos} mo{'s' if mos > 1 else ''}"


def home(request):
    profile = Profile.objects.first()

    featured_projects = Project.objects.filter(featured=True).order_by("order", "-id")[:5]
    projects = Project.objects.all().order_by("order", "-id")

    _experiences = Experience.objects.all().order_by("-currently_working", "-start_date")
    _grouped = {}
    for exp in _experiences:
        if exp.company not in _grouped:
            _grouped[exp.company] = []
        _grouped[exp.company].append(exp)

    experiences = [(company, roles, _company_duration(roles)) for company, roles in _grouped.items()]
    education = Education.objects.all().order_by("-start_year")

    technical_skills = Skill.objects.filter(skill_type="Technical").order_by("order", "name")
    security_skills = Skill.objects.filter(skill_type="Security").order_by("order", "name")
    soft_skills = Skill.objects.filter(skill_type="Soft").order_by("order", "name")

    certificates = Certificate.objects.all().order_by("-issued_date")
    testimonials = Testimonial.objects.all().order_by("-id")[:3]

    # Total years of experience (earliest start date across all experiences)
    all_exps = Experience.objects.all()
    if all_exps.exists():
        earliest = min(e.start_date for e in all_exps)
        total_months = (datetime.date.today().year - earliest.year) * 12 + (datetime.date.today().month - earliest.month) + 1
        total_exp_years = max(1, round(total_months / 12))
    else:
        total_exp_years = 0

    if request.method == "POST":
        # Honeypot check — bots fill hidden fields, humans don't
        if request.POST.get("website", ""):
            return redirect("home")

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_txt = request.POST.get("message", "").strip()

        if not name or not email or not message_txt:
            messages.error(request, "Please fill Name, Email and Message.")
            return redirect("home")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_txt
        )

        try:
            send_mail(
                subject=f"Portfolio Contact: {subject or 'New message'} — from {name}",
                message=f"Name: {name}\nEmail: {email}\n\n{message_txt}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )
        except Exception:
            pass  # message is saved to DB even if email fails

        messages.success(request, "Thanks! Your message has been sent.")
        return redirect("home")

    return render(request, "portfolio/home.html", {
        "profile": profile,
        "featured_projects": featured_projects,
        "projects": projects,
        "experiences": experiences,
        "education": education,
        "technical_skills": technical_skills,
        "security_skills": security_skills,
        "soft_skills": soft_skills,
        "certificates": certificates,
        "testimonials": testimonials,
        "total_exp_years": total_exp_years,
    })


def project_detail(request, pk):
    profile = Profile.objects.first()
    project = get_object_or_404(Project, pk=pk)
    return render(request, "portfolio/project_detail.html", {
        "profile": profile,
        "project": project
    })


def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)


def robots_txt(request):
    content = "User-agent: *\nAllow: /\nSitemap: {}://{}/sitemap.xml\n".format(
        request.scheme, request.get_host()
    )
    return HttpResponse(content, content_type="text/plain")


def sitemap_xml(request):
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{request.scheme}://{request.get_host()}/</loc>
  </url>
</urlset>"""
    return HttpResponse(xml, content_type="application/xml")

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from .models import (
    Profile, Experience, Education, Project,
    Skill, Certificate, Testimonial, ContactMessage
)


def home(request):
    profile = Profile.objects.first()

    featured_projects = Project.objects.filter(featured=True).order_by("-id")[:5]
    projects = Project.objects.all().order_by("-id")

    experiences = Experience.objects.all().order_by("-id")
    education = Education.objects.all().order_by("-id")

    technical_skills = Skill.objects.filter(skill_type="Technical").order_by("name")
    security_skills = Skill.objects.filter(skill_type="Security").order_by("name")
    soft_skills = Skill.objects.filter(skill_type="Soft").order_by("name")

    certificates = Certificate.objects.all().order_by("-id")
    testimonials = Testimonial.objects.all().order_by("-id")[:3]

    if request.method == "POST":
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
    })


def project_detail(request, pk):
    profile = Profile.objects.first()
    project = get_object_or_404(Project, pk=pk)
    return render(request, "portfolio/project_detail.html", {
        "profile": profile,
        "project": project
    })


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
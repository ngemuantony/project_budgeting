from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site

def send_project_status_email(request, project):
    """
    Send an email notification when a project's status is updated.
    """
    context = {
        'project': project,
        'site_url': f"https://{get_current_site(request).domain}",
    }
    
    # Render email templates
    html_message = render_to_string('account/email/project_status_update.html', context)
    plain_message = render_to_string('account/email/project_status_update.txt', context)
    
    # Send email
    send_mail(
        subject=f'Project Status Update - {project.name}',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[project.owner.email],
        html_message=html_message,
    )

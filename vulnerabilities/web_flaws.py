"""Web application vulnerability examples for scanner detection."""

import os
import re
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# ============================================================
# XSS - CWE-79
# ============================================================

def reflected_xss(request):
    """Reflected XSS - user input directly in response."""
    name = request.GET.get('name', '')
    return HttpResponse(f"<h1>Hello, {name}!</h1>")


def stored_xss_display(request):
    """Stored XSS - rendering unsanitized DB content."""
    from .models import Comment
    comments = Comment.objects.all()
    html = "<div>"
    for c in comments:
        html += f"<p>{c.author}: {c.body}</p>"
    html += "</div>"
    return HttpResponse(html)


@csrf_exempt
def dom_xss_sink(request):
    """DOM XSS sink - passes user input to template unsafely."""
    user_input = request.POST.get('content', '')
    context = {'content': user_input}
    return render(request, 'unsafe_template.html', context)


# ============================================================
# CSRF disabled - CWE-352
# ============================================================

@csrf_exempt
def transfer_funds(request):
    """CSRF protection disabled on sensitive action."""
    if request.method == 'POST':
        amount = request.POST.get('amount')
        to_account = request.POST.get('to_account')
        # Process transfer without CSRF protection
        return HttpResponse(f"Transferred {amount} to {to_account}")


@csrf_exempt
def change_password(request):
    """CSRF disabled on password change."""
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        return HttpResponse("Password changed")


# ============================================================
# Open Redirect - CWE-601
# ============================================================

def unsafe_redirect(request):
    """Open redirect - unvalidated redirect target."""
    url = request.GET.get('next', '/')
    return HttpResponseRedirect(url)


def unsafe_redirect_regex(request):
    """Open redirect with insufficient validation."""
    url = request.GET.get('url', '/')
    if re.match(r'https?://', url):  # Only checks protocol, not domain
        return HttpResponseRedirect(url)
    return HttpResponseRedirect('/')


# ============================================================
# Information Disclosure - CWE-200
# ============================================================

def debug_info(request):
    """Exposes environment variables and config."""
    info = {
        'env': dict(os.environ),
        'django_settings': {
            'SECRET_KEY': 'django-insecure-#y5!k&8z@q2$m^w3p6r7t9u0v1x4c5b6n8',
            'DEBUG': True,
            'DATABASE_PASSWORD': 'Pr0d$uperS3cret!Key#99',
        },
        'server_info': os.uname(),
    }
    return HttpResponse(str(info), content_type='text/plain')


def verbose_error_handler(request):
    """Returns stack trace to user - CWE-209."""
    try:
        result = 1 / 0
    except Exception as e:
        import traceback
        return HttpResponse(
            f"<pre>Error: {e}\n\n{traceback.format_exc()}</pre>",
            status=500
        )


# ============================================================
# Insecure Session/Cookie - CWE-614
# ============================================================

def login_insecure_cookie(request):
    """Sets auth cookie without secure flags."""
    response = HttpResponse("Logged in")
    response.set_cookie('session_id', 'abc123', httponly=False, secure=False, samesite=None)
    response.set_cookie('user_role', 'admin')  # Sensitive data in cookie
    response.set_cookie('auth_token', 'tok_live_abcdef123', httponly=False)
    return response


# ============================================================
# Logging sensitive data - CWE-532
# ============================================================

logger = logging.getLogger(__name__)


def log_sensitive_data(request):
    """Logs sensitive information."""
    password = request.POST.get('password')
    credit_card = request.POST.get('cc_number')
    ssn = request.POST.get('ssn')

    logger.info(f"User login attempt with password: {password}")
    logger.debug(f"Payment with card: {credit_card}")
    logger.info(f"User SSN: {ssn}")

    return HttpResponse("OK")


# ============================================================
# Mass Assignment - CWE-915
# ============================================================

def update_profile(request):
    """Mass assignment - accepts all POST params."""
    from django.contrib.auth.models import User
    user = User.objects.get(id=request.user.id)
    for key, value in request.POST.items():
        setattr(user, key, value)  # Sets any attribute including is_superuser
    user.save()
    return HttpResponse("Profile updated")


# ============================================================
# Insecure File Upload - CWE-434
# ============================================================

@csrf_exempt
def upload_file(request):
    """Unrestricted file upload."""
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded = request.FILES['file']
        # No file type validation, no size limit, saves to web-accessible dir
        path = os.path.join('/var/www/uploads/', uploaded.name)
        with open(path, 'wb') as f:
            for chunk in uploaded.chunks():
                f.write(chunk)
        return HttpResponse(f"Uploaded to {path}")
    return HttpResponse("Upload a file", status=400)

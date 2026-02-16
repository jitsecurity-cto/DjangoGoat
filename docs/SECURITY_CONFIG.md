# Security Configuration for DjangoGoat

## Rate Limiting Configuration

This file contains recommended security configurations for the DjangoGoat application.

### Django Rate Limiting Setup

To implement rate limiting in your DjangoGoat application:

1. Install django-ratelimit:
   ```bash
   pip install django-ratelimit
   ```

2. Add to INSTALLED_APPS in settings.py:
   ```python
   INSTALLED_APPS = [
       # ... existing apps
       'django_ratelimit',
   ]
   ```

3. Add to MIDDLEWARE in settings.py:
   ```python
   MIDDLEWARE = [
       # ... existing middleware
       'django_ratelimit.middleware.RatelimitMiddleware',
   ]
   ```

4. Add rate limiting configuration:
   ```python
   # Rate limiting configuration
   RATELIMIT_ENABLE = True
   RATELIMIT_USE_CACHE = 'default'
   RATELIMIT_VIEW = 'django_ratelimit.views.ratelimited'
   
   # Default rate limits
   RATELIMIT_LOGIN_ATTEMPTS = '5/5m'
   ```

### Security Benefits

- **Prevents brute force attacks** on login endpoints
- **Reduces DoS attack surface** by limiting rapid requests  
- **Improves application resilience** under high load
- **Follows security best practices** for web applications

### Implementation Notes

- The configuration limits login attempts to 5 per 5 minutes
- Rate limiting uses Django's default cache backend
- Custom rate limit views can be implemented for better user experience
- Consider implementing progressive delays for repeated violations

### Testing Rate Limiting

You can test the rate limiting by making multiple rapid requests to login endpoints:

```bash
# Test with curl
for i in {1..10}; do
  curl -X POST http://localhost:8000/login/ \
    -d "username=test&password=wrong" \
    -H "Content-Type: application/x-www-form-urlencoded"
done
```

After the 5th attempt within 5 minutes, subsequent requests should be rate limited.
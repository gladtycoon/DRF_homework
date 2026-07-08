from rest_framework.serializers import ValidationError

allowed_links = ["youtube.com"]

def validate_allowed_links(value):
    allowed_links = ["youtube.com"]
    if not any(domain in value.lower() for domain in allowed_links):
        raise ValidationError("Можно использовать только ссылки на YouTube (youtube.com)")
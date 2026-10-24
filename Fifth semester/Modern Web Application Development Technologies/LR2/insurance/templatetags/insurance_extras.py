from django import template
from django.templatetags.static import static

register = template.Library()

# External hosts that often fail offline / in lab networks
_BLOCKED_PREFIXES = (
    "https://picsum.photos/",
    "http://picsum.photos/",
)


@register.simple_tag
def picture_src(path: str, fallback_static: str) -> str:
    """
    Resolve image path for <img src>.
    - Empty or blocked URL -> local static fallback
    - insurance/images/foo.svg -> {% static %}
    - http(s)://... -> as-is
    """
    path = (path or "").strip()
    if not path or any(path.startswith(p) for p in _BLOCKED_PREFIXES):
        return static(fallback_static)
    if path.startswith(("http://", "https://")):
        return path
    return static(path)

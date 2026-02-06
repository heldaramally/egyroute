from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_localized_field(context, obj, field_name):
    """
    Get the localized version of a field
    Usage: {% get_localized_field place 'name' %}
    """
    lang = context.get('LANGUAGE_CODE', 'ar')
    method_name = f'get_{field_name}'
    
    # Check if object has the method
    if hasattr(obj, method_name) and callable(getattr(obj, method_name)):
        return getattr(obj, method_name)(lang)
    
    # Fallback to direct field access
    field_en = f'{field_name}_en'
    if lang == 'en' and hasattr(obj, field_en):
        value_en = getattr(obj, field_en)
        if value_en:
            return value_en
    
    # Return default field
    if hasattr(obj, field_name):
        return getattr(obj, field_name)
    
    return ''


@register.filter
def get_field(obj, field_name):
    """
    Get field value from object
    Usage: {{ place|get_field:'name' }}
    """
    if hasattr(obj, field_name):
        return getattr(obj, field_name)
    return ''

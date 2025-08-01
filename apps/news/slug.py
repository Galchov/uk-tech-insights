import uuid
from django.utils.text import slugify


def generate_unique_slug(instance, field_value, slug_field_name='slug', max_length=100, suffix_length=6):
    """
    Generates a unique slug for a Django model instance.

    Args:
        instance (models.Model): The model instance.
        field_value (str): The base string to slugify (usually the title).
        slug_field_name (str): The name of the slug field on the model.
        max_length (int): Maximun length of the slug field.
        suffix_length (int): Length of the random hex suffix to append on collision.

    Returns:
        slug_candidate (str): A unique slug.
    """

    base_slug = slugify(field_value)[:max_length]
    slug_candidate = base_slug

    ModelClass = instance.__class__
    existing = ModelClass.objects.filter(**{slug_field_name: slug_candidate})

    if instance.pk:
        existing = existing.exclude(pk=instance.pk)

    if existing.exists():
        suffix = uuid.uuid4().hex[:suffix_length]
        trunc_length = max_length - (len(suffix) + 1)
        slug_candidate = f"{base_slug[:trunc_length]}-{suffix}"

    return slug_candidate

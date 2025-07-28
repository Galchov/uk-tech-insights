import os

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileExtensionValidator:
    def __init__(self, allowed_extensions=None):
        self.allowed_extensions = allowed_extensions or ['.pdf', '.doc', '.docx']

    def __call__(self, value):
        extension = os.path.splitext(value.name)[1].lower()

        if extension not in self.allowed_extensions:
            raise ValidationError(
                f"Unsupported file extension '{extension}'. Allowed types: {', '.join(self.allowed_extensions)}"
            )
    
    def __eq__(self, other):
        return isinstance(other, FileExtensionValidator) and self.allowed_extensions == other.allowed_extensions
    

@deconstructible
class FileSizeValidator:
    def __init__(self, max_mb=5):
        self.max_mb = max_mb

    def __call__(self, value):
        filesize = value.size
        if filesize > self.max_mb * 1024 * 1024:
            raise ValidationError(
                f"File size exceeds the limit of {self.max_mb}MB."
            )

    def __eq__(self, other):
        return isinstance(other, FileSizeValidator) and self.max_mb == other.max_mb

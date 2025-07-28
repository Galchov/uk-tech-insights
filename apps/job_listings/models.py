import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings


from .managers import JobPostQuerySet
from .validators import FileExtensionValidator, FileSizeValidator


file_validators = [
    FileExtensionValidator(allowed_extensions=['.pdf', '.doc', '.docx']),
    FileSizeValidator(max_mb=5),
]


class JobPost(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = 'full_time', _('Full-time')
        PART_TIME = 'part_time', _('Part-time')
        SELF_EMPLOYED = 'self_employed', _('Self-employed')
        CONTRACT = 'contract', _('Contract')
        INTERNSHIP = 'internship', _('Internship')
        APPRENTICESHIP = 'apprenticeship', _('Apprenticeship')
        FREELANCE = 'freelance', _('Freelance')
        VOLUNTEER = 'volunteer', _('Volunteer')

    class EmploymentMode(models.TextChoices):
        ON_SITE = 'on_site', _('On-site')
        REMOTE = 'remote', _('Remote')
        HYBRID = 'hybrid', _('Hybrid')

    class ExperienceLevel(models.TextChoices):
        INTERN = 'intern', _('Intern')
        ENTRY = 'entry', _('Entry Level')
        JUNIOR = 'junior', _('Junior')
        MID = 'mid', _('Mid-Level')
        SENIOR = 'senior', _('Senior')
        LEAD = 'lead', _('Lead')
        PRINCIPAL = 'principal', _('Principal')
        ARCHITECT = 'architect', _('Architect')
        MANAGER = 'manager', _('Manager')
        DIRECTOR = 'director', _('Director')
        EXECUTIVE = 'executive', _('Executive / CTO')

    class Currencies(models.TextChoices):
        GBP = 'GBP', _('GBP')
        USD = 'USD', _('USD')
        EUR = 'EUR', _('EUR')
        AUD = 'AUD', _('AUD')
        CAD = 'CAD', _('CAD')
        NZD = 'NZD', _('NZD')
        ZAR = 'ZAR', _('ZAR')
        HKD = 'HKD', _('HKD')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'),
    )
    title = models.CharField(
        max_length=150,
        verbose_name=_('Job post title'),
        help_text=_("The main heading of the job post."),
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        verbose_name=_('Slug'),
        help_text=_("Automatically generated from the title."),
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='job_posts',
        verbose_name=_('Registered Company'),
        help_text=_("Link to a registered company in the database (optional)."),
    )
    company_name_raw = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Company Name (Text)'),
        help_text=_("Used when the company is not registered. Will be ignored if a registered company is selected."),
    )
    location = models.ForeignKey(
        'locations.City',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('City'),
        help_text=_("Job's location."),
    )
    job_type = models.CharField(
        max_length=30,
        choices=JobType,
        default=JobType.FULL_TIME,
        verbose_name=_('Job Type'),
        help_text=_("Job contract type."),
    )
    employment_mode = models.CharField(
        max_length=30,
        choices=EmploymentMode,
        default=EmploymentMode.ON_SITE,
        verbose_name=_('Employment Mode'),
        help_text=_("Defining the place of work."),
    )
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel,
        default=ExperienceLevel.ENTRY,
        verbose_name=_('Experience Level'),
        help_text=_("Required experience for the position."),
    )
    description = models.TextField(
        verbose_name=_('Job Description'),
        help_text=_("Summary about the position.")
    )
    responsibilities = models.TextField(
        blank=True,
        verbose_name=_('Responsibilities'),
        help_text=_("What will employee's responsibilities be at work."),
    )
    requirements = models.TextField(
        blank=True,
        verbose_name=_('Requirements'),
        help_text=_("Requirements in terms of knowledge and skillset."),
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Minimum Salary'),
        help_text=_("Lowest expected salary (optional)."),
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Maximum Salary'),
        help_text=_("Highest expected salary (optional)."),
    )
    currency = models.CharField(
        max_length=5,
        choices=Currencies,
        default=Currencies.GBP,
        verbose_name=_('Currency'),
        help_text=_('Some contracts can come from abroad.')
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Job Visibility'),
        help_text=_('Shows whether the job is still available.')
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Published At'),
        help_text=_("Automatically published when meets the conditions in the other fields.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At'),
        help_text=_("When the job post is updated."),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='job_posts_created',
        verbose_name=_("Created By"),
        help_text=_("User who created this job post. Null if imported from an external source."),
    )
    source = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("External Source"),
        help_text=_("If job was imported, specify the API or service name, e.g., Indeed, LinkedIn."),
    )
    external_reference = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("External Reference ID"),
        help_text=_("Unique job ID from external API source (if applicable). Useful for updates and sync."),
    )

    objects = JobPostQuerySet.as_manager()

    class Meta:
        ordering = ['-published_at']
        verbose_name = _('Job Post')
        verbose_name_plural = _('Job Posts')
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['published_at']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(salary_min__lte=models.F('salary_max')), name='salary_min_lte_max'),
            models.UniqueConstraint(
                fields=['source', 'external_reference'],
                name='unique_external_job',
                condition=models.Q(source__isnull=False, external_reference__isnull=False)
            )
        ]
    
    def __str__(self):
        return f"{self.title} at {self.company or self.company_name_raw or _('Unkown Company')}"
    
    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug_candidate = base_slug

            if JobPost.objects.filter(slug=slug_candidate).exists():
                unique_suffix = uuid.uuid4().hex[:6]
                slug_candidate = f"{base_slug}-{unique_suffix}"
            
            self.slug = slug_candidate

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.salary_min and self.salary_max:
            if self.salary_min > self.salary_max:
                raise ValidationError(_("Minimum salary cannot be greater than maximum salary."))
            
        if not self.company and not self.company_name_raw:
            raise ValidationError(_("You must either select a registered company or enter a raw company name."))
        
        if self.company and self.company_name_raw:
            raise ValidationError(_("Please choose either a registered company or enter a raw company name, not both."))


class JobApplication(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'),
    )
    job = models.ForeignKey(
        to=JobPost,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Job Post'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='job_applications',
        verbose_name=_("User (optional)"),
        help_text=_("If the applicant is a registered user."),
    )
    email = models.EmailField(
        verbose_name=_("Email Address"),
        help_text=_("Used to confirm application or for employer contact."),
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Phone Number"),
    )
    message = models.TextField(
        blank=True,
        verbose_name=_("Cover Message"),
        help_text=_("Optional message or motivation."),
    )
    cover_letter = models.FileField(
        upload_to='applications/letters/',
        validators=file_validators,
        verbose_name=_("Cover Letter"),
        help_text=_("Optional letter or motivation. If you preffer sending a file."),
    )
    cv = models.FileField(
        upload_to='applications/cvs/',
        validators=file_validators,
        verbose_name=_("CV / Résumé"),
        help_text=_("Upload your CV in PDF or DOCX format."),
    )
    submitted_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Submitted At"),
    )

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = _('Job Application')
        verbose_name_plural = _('Job Applications')
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name() if self.user else self.email} -> {self.job.title}"
    
    def get_absolute_url(self):
        return reverse('jobs:application_detail', kwargs={'pk': self.pk})


class JobPostUpdateHistory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
    )
    job_post = models.ForeignKey(
        to=JobPost,
        on_delete=models.CASCADE,
        related_name='edit_history',
        verbose_name=_("Job Post"),
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Edited By"),
    )
    edit_summary = models.TextField(
        blank=True,
        verbose_name=_("Edit Summary"),
        help_text=_("Optional notes about what was changed."),
    )
    edited_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Edited At"),
    )

    class Meta:
        ordering = ['-edited_at']
        verbose_name = _("Job Post Edit History")
        verbose_name_plural = _("Job Post Edit Histories")

    def __str__(self):
        return f"{self.job_post.title} edited by {self.edited_by} on {self.edited_at:%Y-%m-%d %H:%M}"

from django.db import models
from django.utils.safestring import mark_safe
from django_crypto_fields.fields import EncryptedCharField
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, TelephoneNumber
from edc_base.model_validators.date import date_not_future, datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, YES_NO_DOESNT_WORK, YES_NO_NA
from edc_locator.model_mixins.subject_contact_fields_mixin import SubjectContactFieldsMixin
from edc_locator.model_mixins.subject_indirect_contact_fields_mixin import SubjectIndirectContactFieldsMixin
from edc_locator.model_mixins.subject_work_fields_mixin import SubjectWorkFieldsMixin
from edc_locator.model_mixins.locator_methods_model_mixin import LocatorMethodsModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from .model_mixins import SearchSlugModelMixin


class LocatorManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class CaregiverLocator(SiteModelMixin, SubjectContactFieldsMixin,
                       SubjectIndirectContactFieldsMixin,
                       SubjectWorkFieldsMixin, LocatorMethodsModelMixin,
                       SearchSlugModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_before_study_start, datetime_not_future])

    screening_identifier = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        blank=True,
        null=True,)

    study_maternal_identifier = models.CharField(
        verbose_name="Study Caregiver Subject Identifier",
        max_length=50,
        unique=True)

    locator_date = models.DateField(
        verbose_name='Date Locator Form signed',
        validators=[date_not_future])

    first_name = FirstnameField(
        null=True, blank=False)

    last_name = LastnameField(
        verbose_name="Last name",
        null=True, blank=False)

    health_care_infant = models.CharField(
        verbose_name=('Health clinic where your infant will'
                      ' receive their routine care'),
        max_length=35,
        blank=True,
        null=True)

    may_call = models.CharField(
        max_length=25,
        choices=YES_NO_NA,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study '
            'staff to call her for follow-up purposes during the study?'))

    may_visit_home = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study staff <b>to '
            'make home visits</b> for follow-up purposes during the study??'))

    has_caretaker = models.CharField(
        verbose_name=(
            "Has the participant identified someone who will be "
            "responsible for the care of the baby in case of her death, to "
            "whom the study team could share information about her baby's "
            "health?"),
        max_length=25,
        choices=YES_NO,
        help_text="")

    caretaker_name = EncryptedCharField(
        verbose_name="Full Name of the responsible person",
        max_length=35,
        help_text="include firstname and surname",
        blank=True,
        null=True)

    may_call_work = models.CharField(
        max_length=25,
        choices=YES_NO_DOESNT_WORK,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study staff '
            'to contact her at work for follow up purposes during the study?'))

    subject_work_phone = EncryptedCharField(
        verbose_name='Work contact number',
        blank=True,
        null=True)

    caretaker_cell = EncryptedCharField(
        verbose_name="Cell number",
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True)

    caretaker_tel = EncryptedCharField(
        verbose_name="Telephone number",
        max_length=8,
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    history = HistoricalRecords()

    objects = LocatorManager()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Locator'

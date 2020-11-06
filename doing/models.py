from django.db import models
from django.utils.translation import gettext as _
from djangotoolbox.fields import EmbeddedModelField, ListField

from ikwen.accesscontrol.models import Member
from ikwen.core.constants import GENDER_CHOICES
from ikwen.core.utils import get_service_instance, add_database
from ikwen.core.models import Model, AbstractConfig, Service
from ikwen.core.fields import MultiImageField, FileField


class Category(Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
       return self.name


class Competitor(Model):
    member = models.ForeignKey(Member)
    birth_town = models.CharField(_('Town of birth'), max_length=100)
    residence = models.CharField(_('Residence'), max_length=100)
    occupation = models.CharField(_('Occupation'), null=True, blank=True, max_length=100)
    school = models.CharField(_('Occupation'), null=True, blank=True, max_length=100)
    study_field = models.CharField(_('Field of study'), null=True, blank=True, max_length=100)

    def __unicode__(self):
        return self.member.first_name


class Project(Model):
    name = models.CharField(max_length=150)
    promoter = models.ForeignKey(Competitor, null=True, blank=True)
    category = models.ForeignKey(Category, null=True)
    team_mate_list = ListField(EmbeddedModelField('accesscontrol.Member'), null=True, blank=True)
    description = models.TextField(_('Describe your project'), max_length=100)
    attachment = FileField(_('Attachment'), allowed_extensions=['doc', 'docx', 'pdf', 'ppt', 'odt'], upload_to='Projects')

    def __unicode__(self):
        return "%s - %s" % (self.name, self.promoter.member.full_name)

    # def get_obj_details(self):
    #     if self.team_mate_list:
    #         team_mates = ",".join([mate for mate in self.team_mate_list])
    #         return "Team-mates: " + team_mates

    def get_obj_details(self):
        vote_count = self.vote_set.count()
        if vote_count > 0:
            return "%d people reacted" % vote_count
        else:
            return "No reaction"


class Vote(Model):
    voter = models.ForeignKey(Member)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "%s voted for %s" % (self.voter.full_name, self.project.name)


class Reaction(Model):
    member = models.ForeignKey(Member)
    project = models.ForeignKey(Project)
    comment = models.CharField(max_length=400, blank=True, null=True)
    liked = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s reacted on %s" % (self.member.full_name, self.project.name)


class Partnership(Model):
    UPLOAD_TO = 'Partnerships'
    partner = models.ForeignKey(Member)
    contract = FileField(_('Contract'), allowed_extensions=['doc', 'pdf', 'docx', 'odt'], upload_to=UPLOAD_TO)

    def __unicode__(self):
        return self.partner


class TrainingModule(Model):
    UPLOAD_TO = 'Training_docs'
    name = models.CharField(_("Training module's name"), max_length=250)
    document = FileField(_('Training document'), allowed_extensions=['doc', 'pdf', 'docx', 'odt'],
                         upload_to=UPLOAD_TO + '/Images')
    duration = models.PositiveIntegerField(_('Training module'), help_text=_('Rated in hours'), default=0)


class ChallengeStep(Model):
    UPLOAD_TO = 'ChallengeSteps'
    resume = models.TextField(_('Resume'))
    image = FileField(blank=True, null=True, allowed_extensions=['jpg', 'jpeg', 'png', 'heic'],
                      upload_to=UPLOAD_TO + '/Images', help_text=_("Upload a single image file here"))
    video = FileField(blank=True, null=True, allowed_extensions=['mp4', 'avi', 'webm', 'mov', 'ogg', 'wmv'],
                      upload_to=UPLOAD_TO + '/Videos', help_text=_("Upload a single video file here"))

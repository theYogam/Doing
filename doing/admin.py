from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.utils.translation import gettext as _


class ProjectAdmin(admin.ModelAdmin):
    fields = ('name', 'category', 'promoter', 'description')
    list_display = ('name', 'category', 'promoter', 'description', 'attachment')
    readonly_fields = ('promoter', 'category',)


class ReactionAdmin(admin.ModelAdmin):
    fields = ('member', 'comment', 'liked')


class VoteAdmin(admin.ModelAdmin):
    fields = ('voter', 'project')


class TrainingModuleAdmin(admin.ModelAdmin):
    fields = ('name', 'document', 'duration')


class ChallengeStepAdmin(admin.ModelAdmin):
    fields = ('resume', 'image', 'video')


class CompetitorAdmin(admin.ModelAdmin):
    fields = ('member', 'birth_town', 'residence', 'occupation', 'school', 'study_field')


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)

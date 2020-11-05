import json
import logging
from threading import Thread


from django.utils.translation import activate, ugettext as _
from django.shortcuts import render, get_object_or_404


from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView

from ikwen.accesscontrol.backends import UMBRELLA
from ikwen.accesscontrol.models import Member

from ikwen.core.views import HybridListView, ChangeObjectBase, logger
from ikwen.core.utils import get_model_admin_instance, get_preview_from_extension, get_service_instance, add_database, \
    get_mail_content, send_push

from conf import settings
from doing.models import Project, Vote, TrainingModule, ChallengeStep, Competitor, Category, Reaction
from doing.admin import ProjectAdmin, VoteAdmin, TrainingModuleAdmin, \
    ChallengeStepAdmin, CompetitorAdmin, CategoryAdmin, ReactionAdmin

logger = logging.getLogger('ikwen')


class Welcome(TemplateView):
    template_name = 'doing/welcome.html'


class Home(TemplateView):
    template_name = 'doing/home.html'


class DownloadGuide(TemplateView):
    template_name = 'doing/download_guide.html'


class VoteList(HybridListView):
    model = Vote
    model_admin = VoteAdmin


class SubmitVote(ChangeObjectBase):
    model = Vote
    model_admin = VoteAdmin
    template_name = 'doing/submit_vote.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        comment = request.GET.get('comment')
        project_id = request.GET.get('project_id')
        is_vote = request.GET.get('is_vote')
        if project_id:
            project = Project.objects.get(pk=project_id)
            if comment:
                try:
                    Reaction.objects.get(member=user, project=project)
                    return HttpResponse(json.dumps({'error': True}), content_type='application/json')
                except:
                    Reaction.objects.create(member=user, project=project, comment=comment)
                    return HttpResponse(json.dumps({'success': True}), content_type='application/json')
            if is_vote:
                try:
                    Vote.objects.get(voter=user, project=project)
                    return HttpResponse(json.dumps({'error': True}), content_type='application/json')
                except:
                    Vote.objects.create(voter=user, project=project)
                    return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        return super(SubmitVote, self).get(request, *args, **kwargs)


class ProjectList(HybridListView):
    model = Project
    model_admin = ProjectAdmin
    list_filter = ('category',)
    html_results_template_name = "doing/snippets/project_list_results.html"


class ChangeProject(ChangeObjectBase):
    model = Project
    model_admin = ProjectAdmin


class SubmitProject(ChangeObjectBase):
    model = Project
    model_admin = ProjectAdmin
    template_name = 'doing/submit_project.html'

    def after_save(self, request, obj, *args, **kwargs):
        member = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')

        if first_name:
            member.first_name = first_name
        if last_name:
            member.last_name = last_name
        if birthday:
            birthday = birthday.split('-')
            member.birthday = birthday[0] + birthday[1]
        if gender:
            member.gender = gender
        member.save()

        birth_town = request.POST.get('birth_town')
        residence = request.POST.get('residence')
        occupation = request.POST.get('occupation')
        school = request.POST.get('school')
        study_field = request.POST.get('study_field')

        try:
            competitor = Competitor.objects.get(member=member)
        except:
            competitor = Competitor.objects.create(member=member)
        if birth_town:
            competitor.birth_town = birth_town
        if residence:
            competitor.residence = residence
        if occupation:
            competitor.occupation = occupation
        if school:
            competitor.school = school
        if study_field:
            competitor.study_field = study_field

        competitor.save()
        obj.promoter = competitor
        team_mates = request.POST.get('team_mates_ids')
        if team_mates:
            obj.team_mate_list = [Member.objects.get(pk=mate) for mate in team_mates.split(',')]
        weblet = get_service_instance()
        obj.save()
        staff_emails = [member.email for member in Member.objects.using(UMBRELLA).filter(is_staff=True)]

        subject = _("Thank you for your application")
        cta_url = "https://tchopetyamo.com"
        leader = obj.promoter.member
        try:
            html_content = get_mail_content(subject, template_name='doing/mails/thanks.html',
                                            extra_context={'applicant_name': leader.full_name,
                                                           'category': obj.category,
                                                           'cta_url': cta_url})
            sender = 'Doing @ %s <no-reply@%s>' % ("tchopetyamo", "tchopetyamo.com")
            msg = EmailMessage(subject, html_content, sender, [leader.email])
            msg.bcc = staff_emails
            msg.content_subtype = "html"
            if getattr(settings, 'UNIT_TESTING', False):
                msg.send()
            else:
                Thread(target=lambda m: m.send(), args=(msg,)).start()
        except:
            logger.error("%s - Failed to send notice mails to %s." % (weblet, leader.first_name), exc_info=True)
        body = _('Congratulation!!! We received your application')
        if obj.category:
            body = _('Congratulation!!! We received your application in %(name)s' % {
                'name': obj.category.name})
        send_push(weblet, leader, subject, body, cta_url)
        return HttpResponseRedirect(reverse('doing:thanks'))


class Partnership(TemplateView):
    template_name = 'doing/partnership.html'


class ChallengeStepList(HybridListView):
    model = ChallengeStep
    model_admin = ChallengeStepAdmin


class ChangeChallengeStep(ChangeObjectBase):
    model = ChallengeStep
    model_admin = ChallengeStepAdmin


class TrainingModuleList(HybridListView):
    model = TrainingModule
    model_admin = TrainingModuleAdmin


class ChangeCompetitor(ChangeObjectBase):
    model = Competitor
    model_admin = CompetitorAdmin


class CompetitorList(HybridListView):
    model = Competitor
    model_admin = CompetitorAdmin


class ChangeCategory(ChangeObjectBase):
    model = Category
    model_admin = CategoryAdmin


class CategoryList(HybridListView):
    model = Category
    model_admin = CategoryAdmin


class ChangeReaction(ChangeObjectBase):
    model = Reaction
    model_admin = ReactionAdmin


class ReactionList(HybridListView):
    model = Reaction
    model_admin = ReactionAdmin


class Thanks(TemplateView):
    template_name = 'doing/thanks.html'
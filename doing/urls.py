from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from doing.views import Welcome, DownloadGuide, VoteList, ChangeProject, SubmitProject, \
    ProjectList, SubmitVote, ChangeCompetitor, CompetitorList, ChangeCategory, CategoryList, Partnership,\
    ChangeReaction, ReactionList, Thanks

urlpatterns = patterns(
    '',
    url(r'^$', Welcome.as_view(), name='welcome'),
    url(r'^downloadGuide/$', login_required(DownloadGuide.as_view()), name='download_guide'),

    url(r'^changeCompetitor/$', permission_required('doing.ik_manage_competitor')(ChangeCompetitor.as_view()), name='change_competitor'),
    url(r'^changeCompetitor/(?P<object_id>[-\w]+)$', permission_required('doing.ik_manage_competitor')(ChangeCompetitor.as_view()), name='change_competitor'),
    url(r'^CompetitorList/$', permission_required('doing.ik_manage_competitor')(CompetitorList.as_view()), name='competitor_list'),

    url(r'^changeReaction/$', permission_required('doing.ik_manage_reaction')(ChangeReaction.as_view()), name='change_reaction'),
    url(r'^changeReaction/(?P<object_id>[-\w]+)$', permission_required('doing.ik_manage_reaction')(ChangeReaction.as_view()), name='change_reaction'),
    url(r'^ReactionList/$', permission_required('doing.ik_manage_reaction')(ReactionList.as_view()), name='reaction_list'),

    url(r'^changeCategory/$', permission_required('doing.ik_manage_category')(ChangeCategory.as_view()), name='change_category'),
    url(r'^changeCategory/(?P<object_id>[-\w]+)$', permission_required('doing.ik_manage_category')(ChangeCategory.as_view()), name='change_category'),
    url(r'^CategoryList/$', permission_required('doing.ik_manage_category')(CategoryList.as_view()), name='category_list'),

    url(r'^changeProject/$', permission_required('doing.ik_manage_project')(login_required(ChangeProject.as_view())), name='change_project'),
    url(r'^submitProject/$', login_required(SubmitProject.as_view()), name='submit_project'),
    url(r'^changeProject/(?P<object_id>[-\w]+)$', permission_required('doing.ik_manage_project')(login_required(ChangeProject.as_view())), name='change_project'),
    url(r'^projectList/$', permission_required('doing.ik_manage_project')(login_required(ProjectList.as_view())), name='project_list'),

    url(r'^voteList/$', permission_required('doing.ik_manage_vote')(VoteList.as_view()), name='vote_list'),
    url(r'^submitVote/$', SubmitVote.as_view(), name='submit_vote'),

    url(r'^partnership/$', Partnership.as_view(), name='partnership'),
    url(r'^thanks/$', Thanks.as_view(), name='thanks'),
)




from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from datetime import datetime

import requests

from apps.gitlab.models import GitlabToken


@login_required
def new(request):
    author = request.GET['a']
    timestamp = request.GET['t']
    message = request.GET['m']
    sent_from = request.GET['u']

    try:
        gitlab_token = request.user.gitlab_token.token
    except GitlabToken.DoesNotExist:
        return redirect('/gitlab/trenger-token')

    post_data = [
        ('title', 'Forslag fra bruker'),
        ('labels', 'Suggestion'),
        ('description', '%s\n\n---\n\n_%s%s_\n\n> %s\n\n<sub>Sendt fra %s</sub>' % (
            message, ('%s, ' % author) if author else '', datetime.fromtimestamp(int(timestamp)),
            message.replace('\n', '\n> '), sent_from)),
    ]
    url = 'https://gitlab.hybrida.no/api/v3/projects/1/issues?private_token=%s' % gitlab_token
    r = requests.post(url, post_data)

    if r.status_code // 100 != 2:
        exit('\n----\n%s\n----\n' % str(r.status_code))

    result = r.json()
    if 'state' in result and result['state'] == 'opened':
        return redirect(result['web_url'] + '/edit#md-preview-holder')

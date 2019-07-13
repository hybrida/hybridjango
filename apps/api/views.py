from django.shortcuts import render

# Create your views here.

from django.http import HttpResponseBadRequest, HttpResponse
import json, requests, urllib

def feedback(request):
    if request.method == 'POST':

        # Get data from client
        anonymous = request.POST.get('ANONYMOUS', default='true') == 'true'
        data = request.POST.get('DATA', default='')
        referer = request.META['HTTP_REFERER']

        # Validate
        if data is not '':

            # Get user information
            authorName = 'Anonymous user'
            authorEmail = 'no-email'
            if not anonymous and request.user.is_authenticated:
                authorName = request.user.get_full_name()
                authorEmail = request.user.username + '@stud.ntnu.no'

            # Email
            subject = 'Tilbakemelding til Vevkom'
            bodyPreText = 'Dette er et svar på din tilbakemelding:\n'

            def slackSafe(string):
                return string.strip()\
                        .replace('&', '&amp;')\
                        .replace('<', '&lt;')\
                        .replace('>', '&gt;')

            def URI(string):
                return urllib.parse.quote_plus(string.encode('utf-8'))

            authorLink = "" if anonymous else\
                'mailto:' + URI(authorEmail) + '?subject=' +\
                URI(subject) + '&body=' + URI(bodyPreText + data)

            # Static information
            authorIcon = 'https://slack-files.com/T0CAJ0U4A-F2WLMK087-7d8bf05908'
            fallback = 'Feedback received'
            color = 'good'
            sentFromUrl = 'Sent from ' + referer

            jsonObj = {
                'attachments': [
                    {
                        'fallback': fallback,
                        'author_name': slackSafe(authorName),
                        'author_link': slackSafe(authorLink),
                        'author_icon': authorIcon,
                        'color': color,
                        'footer': slackSafe(sentFromUrl),
                        'text': slackSafe(data)
                    }
                ]
            }

            try:
                from hybridjango.utils.secrets import SLACK_WEBHOOK_URL
                slackResponse = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(jsonObj))
                if slackResponse.status_code == requests.codes.ok:
                    return HttpResponse("ok")
            except ImportError as e:
                print(e.msg)
                print('No slack webhook URL found, dumping feedback to stdout')
                print(jsonObj)
                return HttpResponseBadRequest("ERR_WEBHOOK_MISSING")

    return HttpResponseBadRequest("invalid request")


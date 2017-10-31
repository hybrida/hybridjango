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
            postURL = 'https://hooks.slack.com/services/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' # Test channel: 'https://hooks.slack.com/services/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'
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

            slackResponse = requests.post(postURL, data=json.dumps(jsonObj))
            if slackResponse.status_code == requests.codes.ok:
                return HttpResponse("ok")

    return HttpResponseBadRequest("invalid request")


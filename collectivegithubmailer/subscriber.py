import os
import logging
import requests
from pyramid.events import subscriber
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from githubevent.events import Push
from chameleon import PageTemplateLoader

logger = logging.getLogger('collectivegithubmailer')
templates = PageTemplateLoader(os.path.join(os.path.dirname(__file__), "templates"))


@subscriber(Push)
def handle_push(event):
    push = event.request.json_body
    logger.info(push)
    mailer = get_mailer(event.request)

    for commit in push['commits']:

        short_commit_msg = commit['message'].split('\n')[0][:60]
        reply_to = '%s <%s>' % (commit['author']['name'], commit['author']['email'])
        diff = requests.get(commit['url'] + '.diff').content
        
        files = ['A %s' % f for f in commit['added']]
        files.extend('M %s' % f for f in commit['modified'])
        files.extend('D %s' % f for f in commit['removed'])

        data = {
            'push': push,
            'commit': commit,
            'files': '\n'.join(files),
            'diff': diff,
        }

        msg = Message(
            subject = '%s/%s: %s' % (push['repository']['name'],
                                 push['ref'].split('/')[-1],
                                 short_commit_msg),
            sender = "%s <plone-cvs@lists.sourceforge.net>" % commit['author']['name'],
            recipients = ["dglick@gmail.com"],
            body = templates['commit_email.pt'](**data),
            extra_headers = {'Reply-To': reply_to}
            )
        
        mailer.send(msg)

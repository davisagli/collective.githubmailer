import os
import logging
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

    for commit in push['commits']:

        # TODO: add file summary and diff

        data = {
            'push': push,
            'commit': commit,
            'files': '',
            'diff': '',
        }

        # TODO: include repo, branch & snippet of commit message in subject
        # TODO: set reply-to to the commit author

        msg = Message(
            subject = '%s : %s' % (push['repository']['name'],
                                   push['ref']),
            sender = "plone-cvs@lists.sourceforge.net",
            recipients = ["plone-cvs@lists.sourceforge.net"],
            body = templates['commit_email.pt'](**data),
            )
        
        get_mailer(event.request).send(msg)

import logging
from pyramid.events import subscriber
from githubevent.events import Push

logger = logging.getLogger('collectivegithubmailer')


@subscriber(Push)
def handle_push(event):
    logger.info(event.request.json_body)

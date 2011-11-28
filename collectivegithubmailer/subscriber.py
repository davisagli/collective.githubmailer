from pyramid.events import subscriber
from githubevent.events import Push


@subscriber(Push)
def handle_push(event):
    print event.request.json_body

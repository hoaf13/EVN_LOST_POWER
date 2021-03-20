from .app import db 
from .app.models import Conversation

conversation = Conversation.query.all()

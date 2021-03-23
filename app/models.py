from app import db

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    intent = db.Column(db.String(32))
    action = db.Column(db.String(32))
    value = db.Column(db.String(100))
    client_message = db.Column(db.String(1000))
    bot_message = db.Column(db.String(1000))
    
    def __repr__(self):
        return '<Conversation %r>' % (self.action)
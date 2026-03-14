from datetime import datetime
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, UniqueConstraint

db = SQLAlchemy()


# =========================================================
# ADMINS
# =========================================================

class Admin(db.Model):
    __tablename__ = "admins"

    adm_id = db.Column(db.BigInteger, primary_key=True)
    adm_role = db.Column(
        Enum("super", "manager", name="admin_roles"),
        nullable=False,
        default="manager"
    )
    adm_full_name = db.Column(db.String(150), nullable=False)
    adm_email = db.Column(db.String(150), nullable=False, unique=True)
    adm_password_hash = db.Column(db.String(255), nullable=False)
    adm_created_at = db.Column(db.DateTime, default=datetime.utcnow)




# =========================================================
# USERS
# =========================================================

class User(db.Model):
    __tablename__ = "users"
    #duser = User.query.get(1)

    usr_id = db.Column(db.BigInteger, primary_key=True)
    usr_firstname = db.Column(db.String(150), nullable=False)
    usr_lastname = db.Column(db.String(100), nullable=False)
    usr_email = db.Column(db.String(150), nullable=False, unique=True)
    usr_password_hash = db.Column(db.String(255), nullable=False)
    usr_summary = db.Column(db.String(150))
    usr_image = db.Column(db.String(150))
    usr_track_id = db.Column(
        db.BigInteger,
        db.ForeignKey("tracks.trk_id", ondelete="SET NULL"),
        nullable=True
    )
    usr_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usr_updated_at = db.Column(
        db.DateTime,
        default=None,
        onupdate=datetime.utcnow
    )

    # Relationships
    track = db.relationship("Track", back_populates="users")
    conversations = db.relationship(
        "Conversation",
        back_populates="creator",
        passive_deletes=True
    )
    messages = db.relationship(
        "ConversationMessage",
        back_populates="user",
        passive_deletes=True
    )
    orders = db.relationship(
        "Order",
        back_populates="user",
        cascade="all, delete"
    )
    user_sessions = db.relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete"
    )

    @classmethod
    def is_email_used(self,email):
        '''An helper function to check if email has been used'''
        email_used = self.query.filter(self.usr_email==email).first()
        return email_used #None or <User>

# =========================================================
# TRACKS
# =========================================================

class Track(db.Model):
    __tablename__ = "tracks"

    trk_id = db.Column(db.BigInteger, primary_key=True)
    trk_level = db.Column(
        Enum("general", "intermediate", "advanced", "junior", name="track_levels"),
        nullable=False
    )
    trk_created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", back_populates="track")
    sessions = db.relationship("Session", back_populates="track")


# =========================================================
# SESSIONS
# =========================================================

class Session(db.Model):
    __tablename__ = "sessions"

    ses_id = db.Column(db.BigInteger, primary_key=True)
    ses_title = db.Column(db.String(200), nullable=False)
    ses_description = db.Column(db.Text)
    ses_track_id = db.Column(
        db.BigInteger,
        db.ForeignKey("tracks.trk_id", ondelete="SET NULL"),
        nullable=True
    )
    ses_start_time = db.Column(db.DateTime)
    ses_created_at = db.Column(db.DateTime, default=datetime.utcnow)

    track = db.relationship("Track", back_populates="sessions")
    attendees = db.relationship(
        "UserSession",
        back_populates="session",
        cascade="all, delete"
    )


# =========================================================
# USER SESSIONS (Many-to-Many Association)
# =========================================================

class UserSession(db.Model):
    # __tablename__ = "user_sessions"

    use_id = db.Column(db.Integer, primary_key=True)
    use_userid = db.Column(
        db.BigInteger,
        db.ForeignKey("users.usr_id", ondelete="CASCADE"),
        nullable=False
    )
    use_sessionid = db.Column(
        db.BigInteger,
        db.ForeignKey("sessions.ses_id", ondelete="CASCADE"),
        nullable=False
    )
    use_datereg = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="user_sessions")
    session = db.relationship("Session", back_populates="attendees")


# =========================================================
# CONVERSATIONS
# =========================================================

class Conversation(db.Model):
    __tablename__ = "conversations"

    con_id = db.Column(db.BigInteger, primary_key=True)
    con_title = db.Column(db.String(200))
    con_content = db.Column(db.Text, nullable=False)
    con_created_by = db.Column(
        db.BigInteger,
        db.ForeignKey("users.usr_id", ondelete="SET NULL"),
        nullable=True
    )
    con_created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship("User", back_populates="conversations")
    messages = db.relationship(
        "ConversationMessage",
        back_populates="conversation",
        cascade="all, delete"
    )

    def save(self):
        db.session.add(self)
        db.session.commit()
        




class ConversationMessage(db.Model):
    __tablename__ = "conversation_messages"

    msg_id = db.Column(db.BigInteger, primary_key=True)
    msg_conversation_id = db.Column(
        db.BigInteger,
        db.ForeignKey("conversations.con_id", ondelete="CASCADE"),
        nullable=False
    )
    msg_user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.usr_id", ondelete="SET NULL"),
        nullable=True
    )
    msg_message = db.Column(db.Text, nullable=False)
    msg_sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversation = db.relationship("Conversation", back_populates="messages")
    user = db.relationship("User", back_populates="messages")


# =========================================================
# TICKETS
# =========================================================

class Ticket(db.Model):
    __tablename__ = "tickets"

    tkt_id = db.Column(db.BigInteger, primary_key=True)
    tkt_name = db.Column(db.String(150), nullable=False)
    tkt_description = db.Column(db.Text)
    tkt_price = db.Column(db.Numeric(10, 2), nullable=False)
    tkt_created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship("Order", back_populates="ticket")


# =========================================================
# ORDERS
# =========================================================

class Order(db.Model):
    __tablename__ = "orders"

    ord_id = db.Column(db.BigInteger, primary_key=True)
    ord_user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.usr_id", ondelete="CASCADE"),
        nullable=False
    )
    ord_ticket_id = db.Column(
        db.BigInteger,
        db.ForeignKey("tickets.tkt_id", ondelete="SET NULL"),
        nullable=True
    )
    ord_order_ref = db.Column(db.String(50), unique=True)
    ord_total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    ord_status = db.Column(
        Enum("pending", "paid", "cancelled", "refunded", name="order_status"),
        default="pending"
    )
    ord_created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="orders")
    ticket = db.relationship("Ticket", back_populates="orders")
    payments = db.relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete"
    )




# =========================================================
# PAYMENTS
# =========================================================

class Payment(db.Model):
    __tablename__ = "payment"

    pay_id = db.Column(db.BigInteger, primary_key=True)
    pay_order_id = db.Column(
        db.BigInteger,
        db.ForeignKey("orders.ord_id", ondelete="CASCADE"),
        nullable=False
    )
    pay_payment_ref = db.Column(db.String(100))
    pay_amount = db.Column(db.Numeric(10, 2), nullable=False)
    pay_status = db.Column(
        Enum("pending", "successful", "failed", name="payment_status"),
        nullable=False
    )
    pay_paid_at = db.Column(db.DateTime)
    pay_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pay_data = db.Column(db.JSON)
    order = db.relationship("Order", back_populates="payments")


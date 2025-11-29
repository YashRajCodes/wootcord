from __future__ import annotations
import typing as t
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class EventPayload(BaseModel):
    """
    Represents the payload of a generic event.
    The 'event' field can be used to determine the specific type of event.
    """
    event: str


class Account(BaseModel):
    """
    Represents a user account in the system.
    """
    id: int
    name: str

class SocialProfiles(BaseModel):
    """
    Represents social media profiles associated with a user account.
    """
    github: t.Optional[str] = None
    twitter: t.Optional[str] = None
    facebook: t.Optional[str] = None
    linkedin: t.Optional[str] = None
    instagram: t.Optional[str] = None

class AdditionalAttributes(BaseModel):
    """
    Represents additional attributes associated with a contact.
    """
    created_at_ip: t.Optional[str] = Field(None, alias="created_at_ip")
    city: t.Optional[str] = None
    country: t.Optional[str] = None
    description: t.Optional[str] = None
    company_name: t.Optional[str] = None
    country_code: t.Optional[str] = None
    social_profiles: t.Optional[SocialProfiles] = None

class Contact(BaseModel):
    """
    Represents a contact in the system.
    """
    account: t.Optional[Account] = None
    additional_attributes: t.Optional[AdditionalAttributes] = None
    avatar: t.Optional[str] = None
    custom_attributes: t.Optional[t.Dict[str, t.Any]] = None
    email: t.Optional[str] = None
    id: int
    identifier: t.Optional[str] = None
    name: str
    phone_number: t.Optional[str] = None
    thumbnail: t.Optional[str] = None
    blocked: t.Optional[bool] = None

class ChangedAttribute(BaseModel):
    """
    Represents a changed attribute in an update event.
    """
    previous_value: t.Optional[t.Any] = None
    current_value: t.Optional[t.Any] = None

class ContactCreated(Contact):
    """
    Represents the payload for a 'contact_created' event.
    """
    event: t.Literal["contact_created"]

class ContactUpdated(Contact):
    """
    Represents the payload for a 'contact_updated' event.
    """
    event: t.Literal["contact_updated"]
    changed_attributes: t.List[t.Dict[str, ChangedAttribute]]

class Browser(BaseModel):
    """
    Represents browser information.
    """
    browser_name: t.Optional[str] = None
    browser_version: t.Optional[str] = None
    device_name: t.Optional[str] = None
    platform_name: t.Optional[str] = None
    platform_version: t.Optional[str] = None

class InitiatedAt(BaseModel):
    """
    Represents the timestamp when an action was initiated.
    """
    timestamp: str

class ConversationAdditionalAttributes(BaseModel):
    """
    Represents additional attributes for a conversation.
    """
    browser: t.Optional[Browser] = None
    browser_language: t.Optional[str] = None
    initiated_at: t.Optional[InitiatedAt] = None
    referer: t.Optional[str] = None

class ContactInbox(BaseModel):
    """
    Represents a contact's inbox.
    """
    contact_id: int
    created_at: datetime
    hmac_verified: bool
    id: int
    inbox_id: int
    pubsub_token: str
    source_id: str
    updated_at: datetime

class MessageStatus(str, Enum):
    """
    Represents the status of a message.
    """
    SENT = "sent"
    READ = "read"

class SenderType(str, Enum):
    """
    Represents the type of a message sender.
    """
    USER = "User"
    CONTACT = "Contact"

class Message(BaseModel):
    """
    Represents a message in a conversation.
    """
    account_id: int
    additional_attributes: t.Dict[str, t.Any]
    content: t.Optional[str] = None
    content_attributes: t.Dict[str, t.Any]
    content_type: str
    conversation_id: int
    created_at: int | datetime
    external_source_ids: t.Dict[str, t.Any]
    id: int
    inbox_id: int
    message_type: int
    private: bool
    processed_message_content: t.Optional[str] = None
    sender: t.Optional[t.Union[Contact, User]] = None
    sender_id: t.Optional[int] = None
    sender_type: t.Optional[SenderType] = None
    sentiment: t.Dict[str, t.Any]
    source_id: t.Optional[str] = None
    status: MessageStatus
    updated_at: datetime | str

class ConversationStatus(str, Enum):
    """
    Represents the status of a conversation.
    """
    PENDING = "pending"
    OPEN = "open"
    RESOLVED = "resolved"

class Conversation(BaseModel):
    """
    Represents a conversation.
    """
    additional_attributes: ConversationAdditionalAttributes
    agent_last_seen_at: int
    applied_sla: t.Optional[t.Any] = None
    can_reply: bool
    channel: str
    contact_inbox: ContactInbox
    contact_last_seen_at: int
    created_at: int
    custom_attributes: t.Dict[str, t.Any]
    first_reply_created_at: t.Optional[datetime] = None
    id: int
    inbox_id: int
    labels: t.List[str]
    last_activity_at: int
    messages: t.List[Message]
    meta: Meta
    priority: t.Optional[t.Any] = None
    sla_events: t.List[t.Any]
    sla_policy_id: t.Optional[int] = None
    snoozed_until: t.Optional[datetime] = None
    status: ConversationStatus
    timestamp: int
    unread_count: int
    updated_at: float
    waiting_since: int

class User(BaseModel):
    """
    Represents a user in the system.
    """
    account: t.Optional[Account] = None
    additional_attributes: t.Optional[AdditionalAttributes] = None
    avatar: t.Optional[str] = None
    custom_attributes: t.Optional[t.Dict[str, t.Any]] = None
    email: t.Optional[str] = None
    id: int
    identifier: t.Optional[str] = None
    name: str
    phone_number: t.Optional[str] = None
    thumbnail: t.Optional[str] = None
    blocked: t.Optional[bool] = None
    type: t.Optional[str] = None
    available_name: t.Optional[str] = None
    avatar_url: t.Optional[str] = None
    availability_status: t.Optional[str] = None

class Meta(BaseModel):
    """
    Represents metadata for a conversation.
    """
    assignee: t.Optional[User] = None
    hmac_verified: bool
    sender: Contact
    team: t.Optional[t.Any] = None

class ConversationCreated(Conversation):
    """
    Represents the payload for a 'conversation_created' event.
    """
    event: t.Literal["conversation_created"]

class ConversationUpdated(Conversation):
    """
    Represents the payload for a 'conversation_updated' event.
    """
    event: t.Literal["conversation_updated"]
    changed_attributes: t.Dict[str, ChangedAttribute]

class ConversationStatusChanged(Conversation):
    """
    Represents the payload for a 'conversation_status_changed' event.
    """
    event: t.Literal["conversation_status_changed"]

class TypingUser(BaseModel):
    """
    Represents a user in a typing event.
    """
    account: Account
    additional_attributes: AdditionalAttributes
    avatar: str
    custom_attributes: t.Dict[str, t.Any]
    email: t.Optional[str] = None
    id: int
    identifier: t.Optional[str] = None
    name: str
    phone_number: t.Optional[str] = None
    thumbnail: str
    blocked: bool

class ConversationTypingOn(BaseModel):
    """
    Represents the payload for a 'conversation_typing_on' event.
    """
    event: t.Literal["conversation_typing_on"]
    user: TypingUser
    conversation: Conversation
    is_private: bool

class ConversationTypingOff(BaseModel):
    """
    Represents the payload for a 'conversation_typing_off' event.
    """
    event: t.Literal["conversation_typing_off"]
    user: TypingUser
    conversation: Conversation
    is_private: bool

class Inbox(BaseModel):
    """
    Represents an inbox.
    """
    id: int
    name: str

class MessageType(str, Enum):
    """
    Represents the type of a message.
    """
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    TEMPLATE = "template"

class MessageCreated(BaseModel):
    """
    Represents the payload for a 'message_created' event.
    """
    account: Account
    additional_attributes: t.Dict[str, t.Any]
    content_attributes: t.Dict[str, t.Any]
    content_type: str
    content: t.Optional[str] = None
    conversation: Conversation
    created_at: datetime
    id: int
    inbox: Inbox
    message_type: MessageType
    private: bool
    sender: t.Optional[t.Union[Contact, User]] = None
    source_id: t.Optional[str] = None
    event: t.Literal["message_created"]
    attachments: t.Optional[t.List[Attachment]] = None

class MessageUpdated(MessageCreated):
    """
    Represents the payload for a 'message_updated' event.
    """
    event: t.Literal["message_updated"]

class Attachment(BaseModel):
    """
    Represents a message attachment.
    """
    id: int
    message_id: int
    file_type: str
    account_id: int
    extension: t.Optional[str] = None
    data_url: str
    thumb_url: str
    file_size: int
    width: t.Optional[int] = None
    height: t.Optional[int] = None

class EventInfo(BaseModel):
    """
    Represents information about an event.
    """
    initiated_at: InitiatedAt
    referer: str
    widget_language: str
    browser_language: str
    browser: Browser


class WebhookPayload(BaseModel):
    """
    Represents the payload of a webhook event.
    The 'event' field can be used to determine the specific type of event.
    """
    id: int
    contact: Contact
    inbox: Inbox
    account: Account
    current_conversation: t.Optional[Conversation] = None
    source_id: str
    event: t.Literal["webwidget_triggered"]
    event_info: EventInfo

class MessageCreatePayload(BaseModel):
    """
    Represents the payload required to create/send a message to Chatwoot.
    """
    content: str
    message_type: t.Literal["incoming", "outgoing"] = "outgoing"
    private: bool = False
    content_type: t.Literal["text", "input_select", "cards", "form"] = "text"
    content_attributes: t.Dict[str, t.Any] = {}

Message.model_rebuild()
Conversation.model_rebuild()
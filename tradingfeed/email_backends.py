from django.core.mail.backends.base import BaseEmailBackend
from postmarker.core import PostmarkClient
from django.conf import settings

class PostmarkEmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = PostmarkClient(server_token=settings.POSTMARK_API_KEY)

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        sent_count = 0
        for message in email_messages:
            response = self.client.emails.send(
                From=message.from_email,
                To=','.join(message.to),
                Subject=message.subject,
                TextBody=message.body,
                HtmlBody=message.alternatives[0][0] if message.alternatives else None
            )
            if response['MessageID']:
                sent_count += 1
        return sent_count

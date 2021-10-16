import base64
import mimetypes
from .client_base import Client_Base
from .decorators import token_required


class Mail(Client_Base):
    @token_required
    def message_folders(self, includeHiddenFolders=False, params=None):
        if includeHiddenFolders:
            data = {'includeHiddenFolders': True}
            return self._get(self._base_url + self.context + 'mailFolders', data=data, params=params)
        else:
            return self._get(self._base_url + self.context + 'mailFolders', params=params)

    @token_required
    def messages(self, folder_id=None, params=None):
        """Retrieve the list of messages in a mailbox folder.
        Args:
            folder_id: selected mail folder.
            params:
        Returns:
            A dict.
        """
        if folder_id:
            return self._get(self._base_url + self.context + 'mailFolders/{id}/messages'.format(id=folder_id), params=params)
        else:
            return self._get(self._base_url + self.context + 'messages', params=params)

    @token_required
    def messages_next(self, last_response_payload):
        if "@odata.nextLink" in last_response_payload.keys():
            return self._get(last_response_payload["@odata.nextLink"])
        else:
            return None

    @token_required
    def message(self, message_id, folder_id=None, params=None, mime_content=False):
        if folder_id:
            return self._get(self._base_url + self.context + 'mailFolders/{}/messages/{}'.format(folder_id, message_id), params=params)
        else:
            return self._get(self._base_url + self.context + 'messages/{}'.format(message_id), params=params)

    @token_required
    def message_attachments(self, message_id, folder_id=None, params=None):
        if folder_id:
            return self._get(self._base_url + self.context + 'mailFolders/{}/messages/{}/attachments'.format(folder_id, message_id), params=params)
        else:
            return self._get(self._base_url + self.context + 'messages/{}/attachments'.format(message_id), params=params)

    def message_attachment(self, attachment_id, message_id, folder_id=None, params=None):
        if folder_id:
            return self._get(self._base_url + self.context + 'mailFolders/{}/messages/{}/attachments/{}'.format(folder_id, message_id, attachment_id), params=params)
        else:
            return self._get(self._base_url + self.context + 'messages/{}/attachments/()'.format(message_id, attachment_id), params=params)

    @token_required
    def message_delete(self, message_id, folder_id=None, params=None):
        if folder_id:
            return self._delete(self._base_url + self.context + 'mailFolders/{}/messages/{}'.format(folder_id, message_id), params=params)
        else:
            return self._delete(self._base_url + self.context + 'messages/{}'.format(message_id), params=params)

    @token_required
    def message_move(self, message_id, destination, folder_id=None, params=None):
        data = {'destinationId': destination}
        if folder_id:
            return self._post(self._base_url + self.context + 'mailFolders/{}/messages/{}'.format(folder_id, message_id), json=data, params=params)
        else:
            return self._post(self._base_url + self.context + 'messages/{}'.format(message_id), json=data, params=params)

    @token_required
    def message_forward(self, message_id, recipients, comment='', folder_id=None, params=None):
        recipient_list = [{'emailAddress': {'address': address}}
                          for address in recipients]
        data = {'comment': comment,
                'toRecipients': recipient_list}
        if folder_id:
            return self._post(self._base_url + self.context + 'mailFolders/{}/messages/{}/forward'.format(folder_id, message_id), json=data, params=params)
        else:
            return self._post(self._base_url + self.context + 'messages/{}/forward'.format(message_id), json=data, params=params)

    @token_required
    def message_send(self, subject=None, recipients=None, body='', content_type='HTML', attachments=None):
        """Helper to send email from current user.

        Args:
            subject: email subject (required)
            recipients: list of recipient email addresses (required)
            body: body of the message
            content_type: content type (default is 'HTML')
            attachments: list of file attachments (local filenames)

        Returns:
            Returns the response from the POST to the sendmail API.
        """

        # Verify that required arguments have been passed.
        if not all([subject, recipients]):
            raise ValueError('sendmail(): required arguments missing')

        # Create recipient list in required format.
        recipient_list = [{'emailAddress': {'address': address}}
                          for address in recipients]

        # Create list of attachments in required format.
        attached_files = []
        if attachments:
            for filename in attachments:
                if isinstance(attachments, dict):
                    b64_content = base64.b64encode(attachments[filename])
                else:
                    b64_content = base64.b64encode(open(filename, 'rb').read())
                mime_type = mimetypes.guess_type(filename)[0]
                mime_type = mime_type if mime_type else ''
                attached_files.append(
                    {'@odata.type': '#microsoft.graph.fileAttachment',
                     'contentBytes': b64_content.decode('utf-8'),
                     'contentType': mime_type,
                     'name': filename})

        # Create email message in required format.
        email_msg = {'message': {'subject': subject,
                                 'body': {'contentType': content_type, 'content': body},
                                 'toRecipients': recipient_list,
                                 'attachments': attached_files},
                     'SaveToSentItems': 'true'}

        # Do a POST to Graph's sendMail API and return the response.
        return self._post(self._base_url + self.context + 'sendMail', json=email_msg)

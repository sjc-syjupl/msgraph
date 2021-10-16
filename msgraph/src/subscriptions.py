from .client_base import Client_Base
from .decorators import token_required


class Subscriptions(Client_Base):
    @token_required
    def subscription(self, subscription_id=None):
        if subscription_id:
            return self._get(self.base_url + 'subscriptions/{}'.format(subscription_id))
        else:
            return self._get(self.base_url + 'subscriptions')

    @token_required
    def subscription_create(self, change_type, notification_url, resource, expiration_datetime, client_state=None):
        data = {
            'changeType': change_type,
            'notificationUrl': notification_url,
            'resource': resource,
            'expirationDateTime': expiration_datetime,
            'clientState': client_state
        }
        return self._post(self.base_url + 'subscriptions', json=data)

    @token_required
    def subscription_renew(self, subscription_id, expiration_datetime):
        data = {
            'expirationDateTime': expiration_datetime
        }
        return self._patch(self.base_url + 'subscriptions/{}'.format(subscription_id), json=data)

    @token_required
    def subscription_delete(self, subscription_id):
        return self._delete(self.base_url + 'subscriptions/{}'.format(subscription_id))

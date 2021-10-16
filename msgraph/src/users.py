from .client_base import Client_Base
from .decorators import token_required


class Users(Client_Base):
    @token_required
    def me(self):
        return self._get(self.base_url + 'me')

    @token_required
    def user(self, user_id):
        return self._get(self.base_url + 'users/{}'.format(user_id))

    @token_required
    def users(self, params=None):
        return self._get(self.base_url + 'users', params=params)

    @token_required
    def user_create(self, displayName, mailNickname, userPrincipalName, password, accountEnabled=True, forceChangePasswordNextSignIn=True):
        data = {
            "accountEnabled": accountEnabled,
            "displayName": displayName,
            "mailNickname": mailNickname,
            "userPrincipalName": userPrincipalName,
            "passwordProfile": {
                "forceChangePasswordNextSignIn": forceChangePasswordNextSignIn,
                "password": password
            }
        }
        return self._post(self.base_url + 'users', json=data)

    @token_required
    def me_update(self, data):
        return self._patch(self.base_url + 'me', json=data)

    @token_required
    def user_update(self, user_id, data):
        return self._patch(self.base_url + 'users/{}'.format(user_id), json=data)

    @token_required
    def user_delete(self, user_id, data):
        return self._delete(self.base_url + 'users/{}'.format(user_id), json=data)

    @token_required
    def me_change_password(self, current_password, new_password):
        data = {
            "currentPassword": current_password,
            "newPassword": new_password
        }
        return self._post(self.base_url + 'me/changePassword', json=data)

    @token_required
    def user_change_password(self, user_id, current_password, new_password):
        data = {
            "currentPassword": current_password,
            "newPassword": new_password
        }
        return self._post(self.base_url + 'users/{}/changePassword'.format(user_id), json=data)

    @token_required
    def user_delta(self, params=None):
        return self._get(self.base_url + 'users/delta', params=params)

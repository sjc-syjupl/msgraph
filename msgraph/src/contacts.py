from .client_base import Client_Base
from .decorators import token_required


class Contacts(Client_Base):
    @token_required
    def contacts(self, params=None):
        return self._get(self.base_url + self.context + 'contacts', params=params)

    @token_required
    def contact(self, contact_id=None):
        return self._get(self.base_url + self.context + 'contacts/{}'.format(contact_id))

    @token_required
    def contact_create(self, givenName, surname, email_addresses, **kwargs):
        addresses_list = [{
            "emailAddress": {
                "address": a['email'],
                "name": a['name']
            }
        } for a in email_addresses]
        data = {
            "givenName": givenName,
            "surname": surname,
            "emailAddresses": addresses_list,
        }
        return self._post(self.base_url + self.context + 'contacts', json={**kwargs, **data})

    @token_required
    def contact_update(self, contact_id, **kwargs):
        return self._patch(self.base_url + self.context + 'contacts/{}'.format(contact_id), json=kwargs)

    @token_required
    def contact_delete(self, contact_id, **kwargs):
        return self._delete(self.base_url + self.context + 'contacts/{}'.format(contact_id))

    @token_required
    def contact_folders(self, params=None):
        return self._get(self.base_url + self.context + 'contactFolders')

    @token_required
    def contact_folder_create(self, name, parent_folder_id=''):
        data = {"parentFolderId": parent_folder_id, "displayName": name}
        return self._post(self.base_url + self.context + 'contactFolders', json=data)

    @token_required
    def contact_folder_update(self, folder_id, name, parent_folder_id=None):
        data = {"displayName": name}
        if parent_folder_id:
            data["parentFolderId"] = parent_folder_id
        return self._patch(self.base_url + self.context + 'contactFolders/{}'.format(folder_id), json=data)

    @token_required
    def contact_folder_delete(self, folder_id):
        return self._delete(self.base_url + self.context + 'contactFolders/{}'.format(folder_id))

    @token_required
    def contact_childFolders(self, folder_id):
        return self._get(self.base_url + self.context + 'contactFolders/{}/childFolders'.format(folder_id))

    @token_required
    def contact_childFolder_create(self, parent_folder_id, name):
        data = {"displayName": name}
        return self._post(self.base_url + self.context + 'contactFolders/{}/childFolders'.format(parent_folder_id), json=data)

    @token_required
    def contacts_in_folder(self, folder_id):
        return self._get(self.base_url + self.context + 'contactFolders/{id}/contacts'.format(folder_id))

    @token_required
    def contact_create_in_folder(self, folder_id, givenName, surname, email_addresses, **kwargs):
        addresses_list = [{
            "emailAddress": {
                "address": a['email'],
                "name": a['name']
            }
        } for a in email_addresses]
        data = {
            "givenName": givenName,
            "surname": surname,
            "emailAddresses": addresses_list,
        }
        return self._post(self.base_url + self.context + 'contactFolders/{id}/contacts'.format(folder_id), json={**kwargs, **data})

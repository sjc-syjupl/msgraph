import requests
from urllib.parse import quote
from .client_base import Client_Base
from .decorators import token_required


class Files(Client_Base):
    def _files_context(self, site=None, group=None, drive_id=None, item_id=None, path=None, action=None):
        global quote
        context = self.context
        if site:
            context = 'sites/{}'.format(site)
        elif group:
            context = 'groups/{}/'.format(group)
        elif drive_id:
            context = 'drives/{}/'.format(drive_id)

        if item_id:
            if drive_id:
                context += 'items/{}/'.format(item_id)
            else:
                context += 'drive/items/{}/'.format(item_id)
            if action:
                context += '/{}'.format(action)
        elif path:
            if drive_id:
                context += 'root:/{}'.format(quote(path))
            else:
                context += 'drive/root:/{}'.format(quote(path))
            if action:
                context += ':/{}'.format(action)
        return context

    @token_required
    def file_default_drive(self, site=None, group=None):
        return self._get(self.base_url + self._files_context(site=site, group=group) + 'drive')

    @token_required
    def file_drives(self, site=None, group=None, params=None):
        return self._get(self.base_url + self._files_context(site=site, group=group) + 'drives', params=params)

    @token_required
    def files(self, path=None, item_id=None, site=None, group=None, drive_id=None, params=None):
        if item_id or path:
            return self._get(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path, action='children'), params=params)
        else:  # get files from root folder
            if drive_id:
                return self._get(self.base_url + self._files_context(drive_id=drive_id) + 'root/children', params=params)
            else:
                return self._get(self.base_url + self._files_context(site=site, group=group) + 'drive/root/children', params=params)

    @token_required
    def file_info(self, path=None, item_id=None, site=None, group=None, drive_id=None):
        if item_id or path:
            return self._get(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path))
        else:  # get files from root folder
            raise ValueError('file_info(): path or item_id are required')

    @token_required
    def file_create_folder(self, name, path=None, item_id=None, site=None, group=None, drive_id=None, rename=False):
        data = {"name": name, "folder": {}}
        if rename:
            data["@microsoft.graph.conflictBehavior"] = "rename"
        if item_id or path:
            return self._post(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path, action='children'), json=data)
        else:  # create folder in root
            if drive_id:
                return self._post(self.base_url + self._files_context(drive_id=drive_id) + 'root/children', json=data)
            else:
                return self._post(self.base_url + self._files_context(site=site, group=group) + 'drive/root/children', json=data)

    @token_required
    def file_rename(self, new_name, path=None, item_id=None, site=None, group=None, drive_id=None):
        data = {"name": new_name}
        if item_id or path:
            return self._patch(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path), json=data)
        else:  # get files from root folder
            raise ValueError('file_rename(): path or item_id are required')

    @token_required
    def file_delete(self, path=None, item_id=None, site=None, group=None, drive_id=None):
        if item_id or path:
            return self._delete(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path))
        else:  # get files from root folder
            raise ValueError('file_delete(): path or item_id are required')

    @token_required
    def file_move(self, new_name, new_folder_id, path=None, item_id=None, site=None, group=None, drive_id=None):
        data = {"name": new_name, "parentReference": {"id": new_folder_id}, }
        if item_id or path:
            return self._patch(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path), json=data)
        else:  # get files from root folder
            raise ValueError('file_move(): path or item_id are required')

    @token_required
    def file_copy(self, new_name, new_folder_id, path=None, item_id=None, site=None, group=None, drive_id=None):
        data = {"name": new_name, "parentReference": {"id": new_folder_id}, }
        if item_id or path:
            return self._post(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path, action='copy'), json=data)
        else:  # get files from root folder
            raise ValueError('file_copy(): path or item_id are required')

    @token_required
    def file_download(self, path=None, item_id=None, site=None, group=None, drive_id=None, format=None):
        data = {}
        if format:
            data = {'format': format}
        if item_id or path:
            return self._get(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path, action='content'), data=data)
        else:  # get files from root folder
            raise ValueError('file_download(): path or item_id are required')

    @token_required
    def file_download_url(self, path=None, item_id=None, site=None, group=None, drive_id=None, format=None):
        data = {}
        if format:
            data = {'format': format}
        if item_id or path:
            return self._get(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path, action='content'), data=data, allow_redirects=False)
        else:  # get files from root folder
            raise ValueError('file_download(): path or item_id are required')

    @token_required
    def file_upload_existing(self, data, path=None, item_id=None, site=None, group=None, drive_id=None):
        if item_id or path:
            if len(data) > 3*1024*1024:
                response = self.file_upload_existing(
                    data='', path=path, item_id=item_id, site=site, group=group, drive_id=drive_id)
                return self.file_upload_large(data=data, item_id=response['id'], site=site, group=group, drive_id=drive_id)
            else:
                headers = {'Content-Type': 'text/plain'}
                if not isinstance(data, str):
                    headers = {'Content-Type': 'application/octet-stream'}
                return self._put(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=item_id, path=path, action='content'), data=data, headers=headers)
        else:  # get files from root folder
            raise ValueError(
                'file_upload_existing(): path or item_id are required')

    @token_required
    def file_upload_new(self, filename, data, parent_path=None, parent_item_id=None, site=None, group=None, drive_id=None):
        if parent_item_id or parent_path:
            if len(data) > 3*1024*1024:
                response = self.file_upload_new(
                    data='', path=parent_path, item_id=parent_item_id, site=site, group=group, drive_id=drive_id)
                return self.file_upload_large(data=data, item_id=response['id'], site=site, group=group, drive_id=drive_id)
            else:
                headers = {
                    'Content-Type': 'text/plain' if isinstance(data, str) else 'application/octet-stream'}
                return self._put(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id, item_id=(parent_item_id+':' if parent_item_id else None),
                                                                     path=parent_path, action='{}:/content'.format(filename)), data=data, headers=headers)
        else:  # get files from root folder
            raise ValueError(
                'file_upload_new(): parent_path or parent_item_id are required')

    @token_required
    def file_upload_large(self, data, path=None, item_id=None, site=None, group=None, drive_id=None):
        if item_id or path:
            create_session = {
                "@microsoft.graph.conflictBehavior": "replace", "fileSize": len(data)}
            upload_session = self._post(self.base_url + self._files_context(site=site, group=group, drive_id=drive_id,
                                        item_id=item_id, path=path, action='createUploadSession'), data=create_session)
            headers = {
                'Content-Type': 'text/plain' if isinstance(data, str) else 'application/octet-stream'}
            return requests.put(upload_session['uploadUrl'], data=data, headers=headers)
        else:  # get files from root folder
            raise ValueError(
                'file_upload_large(): parent_path or parent_item_id are required')

from .client_base import Client_Base
from .decorators import token_required


class OneNote(Client_Base):
    def _onenote_context(self, group=None, site=None):
        if group:
            return 'groups/{}/'.format(group)
        elif site:
            return 'sites/{}/'.format(site)
        else:
            return self.context

    @token_required
    def onenote_notebooks(self, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/notebooks')

    @token_required
    def onenote_notebook(self, notebook_id, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/notebooks/{}'.format(notebook_id))

    @token_required
    def onenote_sections(self, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/sections')

    @token_required
    def onenote_section(self, section_id, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/sections/{}'.format(section_id))

    @token_required
    def onenote_sectionGroups(self, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/sectionGroups')

    @token_required
    def onenote_sectionGroup(self, section_groups_id, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/sectionGroups/{}'.format(section_groups_id))

    @token_required
    def onenote_pages(self, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/pages')

    @token_required
    def onenote_page(self, page_id, group=None, site=None):
        return self._get(self.base_url + self._onenote_context(group, site) + 'onenote/pages/{}'.format(page_id))

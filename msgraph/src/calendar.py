from .client_base import Client_Base
from .decorators import token_required


class Calendar(Client_Base):
    def _calendar_context(self, calendar_group=None, group=None, calendar=None):
        if calendar_group:
            return self.context + 'calendarGroups/{}/'.format(calendar_group)
        if group:
            return 'groups/{}/'.format(group)
        if calendar:
            return self.context + 'calendars/{}/'.format(calendar)
        return self.context

    @token_required
    def calendars(self, calendar_group=None):
        return self._get(self.base_url + self._calendar_context(calendar_group) + 'calendars')

    @token_required
    def calendar(self, calendar_id=None, calendar_group=None):
        if calendar_id:
            return self._get(self.base_url + self._calendar_context(calendar_group) + 'calendars/{}'.format(calendar_id))
        else:
            return self._get(self.base_url + self.context + 'calendar')

    @token_required
    def calendar_create(self, name):
        body = {'name': name}
        return self._post(self.base_url + self.context + 'calendars', json=body)

    @token_required
    def calendar_update(self, calendar_id, name, calendar_group=None):
        body = {'name': name}
        return self._patch(self.base_url + self._calendar_context(calendar_group) + 'calendars/{}'.format(calendar_id), json=body)

    @token_required
    def calendar_delete(self, calendar_id, calendar_group=None):
        return self._delete(self.base_url + self._calendar_context(calendar_group) + 'calendars/{}'.format(calendar_id))

    @token_required
    def calendar_events(self, calendar_id=None, calendar_group=None, params=None):
        if calendar_id:
            return self._get(self.base_url + self._calendar_context(calendar_group) + 'events', params=params)
        else:
            return self._get(self.base_url + self.context + 'events', params=params)

    @token_required
    def calendar_events_view(self, start_date_time, end_date_time, calendar_id=None, calendar_group=None):
        data = {'startDateTime': start_date_time, 'endDateTime': end_date_time}
        if calendar_id:
            return self._get(self.base_url + self._calendar_context(calendar_group) + 'events', data=data)
        else:
            return self._get(self.base_url + self.context + 'events', data=data)

    @token_required
    def calendar_track_changes(self, start_date_time, end_date_time, params=None):
        data = {'startDateTime': start_date_time, 'endDateTime': end_date_time}
        return self._get(self.base_url + self.context + 'calendarView/delta', data=data, params=params)

    @token_required
    def calendar_event(self, event_id, group=None, params=None):
        return self._get(self.base_url + self._calendar_context(group=group) + 'events/{}'.format(event_id), params=params)

    @token_required
    def calendar_create_event(self, subject, content, start_datetime, start_timezone, end_datetime, end_timezone,
                              attendees, location="", calendar=None):
        """
        Create a new calendar event.

        Args:
            subject: subject of event, string
            content: content of event, string
            start_datetime: in the format of 2017-09-04T11:00:00, dateTimeTimeZone string
            start_timezone: in the format of Pacific Standard Time, string
            end_datetime: in the format of 2017-09-04T11:00:00, dateTimeTimeZone string
            end_timezone: in the format of Pacific Standard Time, string
            location:   string
            attendees: list of dicts of the form:
                        [{'email': 'email@example.com', 'name': 'John Doe', 'type': 'required'},...]
            calendar: The calendar the event is scheduled on
        Returns:
            A dict.
        """
        event = self.calendar_build_event_request(subject, content, start_datetime, start_timezone, end_datetime,
                                                  end_timezone, attendees, location)
        return self._post(self.base_url + self._calendar_context(calendar=calendar) + 'events', json=event)

    @token_required
    def calendar_update_event(self, event_id, subject, content, start_datetime, start_timezone, end_datetime,
                              end_timezone, attendees, location="", calendar=None):
        """
        Update an existing calendar event.

        Args:
            event_id: id of the calendar event
            subject: subject of event, string
            content: content of event, string
            start_datetime: in the format of 2017-09-04T11:00:00, dateTimeTimeZone string
            start_timezone: in the format of Pacific Standard Time, string
            end_datetime: in the format of 2017-09-04T11:00:00, dateTimeTimeZone string
            end_timezone: in the format of Pacific Standard Time, string
            location:   string
            attendees: list of dicts of the form:
                        [{'email': 'email@example.com', 'name': 'John Doe', 'type': 'required'},...]
            calendar: The calendar the event is scheduled on
        Returns:
            A dict.
        """
        event = self.calendar_build_event_request(subject, content, start_datetime, start_timezone, end_datetime,
                                                  end_timezone, attendees, location)
        return self._patch(self.base_url + self._calendar_context(calendar=calendar) + 'events/{}'.format(event_id), json=event)

    @token_required
    def calendar_delete_event(self, event_id, calendar=None):
        return self._delete(self.base_url + self._calendar_context(calendar=calendar) + 'events/{}'.format(event_id))

    def calendar_build_event_request(subject, content, start_datetime, start_timezone, end_datetime, end_timezone,
                                     attendees, location):
        attendees_list = [{
            "emailAddress": {
                "address": a['email'],
                "name": a['name']
            },
            "type": a['type']
        } for a in attendees]
        return {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": content
            },
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": start_timezone
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": end_timezone
            },
            "location": {
                "displayName": location
            },
            "attendees": attendees_list
        }

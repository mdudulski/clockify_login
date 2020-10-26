import pandas as pd
import requests
from config import api_key_from_config, workspace_name, user_name


class ClockifyApiHandler:
    BASE_URL = 'https://api.clockify.me/api/v1/'
    HEADER_CONTENT = 'application/json'
    HEADER_X_API = api_key_from_config
    # TODO return error if key is wrong
    WORKSPACE_NAME = workspace_name
    USER_NAME = user_name
    HEADERS = {
        'content-type': HEADER_CONTENT,
        'X-Api-Key': HEADER_X_API
    }

    def _get_workspaces_id(self):
        workspaces = requests.get(
            self.BASE_URL + '/workspaces',
            headers=self.HEADERS)
        df_workspace = pd.DataFrame.from_dict(workspaces.json())
        workspace_id = df_workspace[df_workspace['name']
                                    == workspace_name]['id'].to_string(index=False)
        return workspace_id.lstrip()

    def _get_user_id(self, email):
        request = requests.get(
            self.BASE_URL + '/workspaces/' + self._get_workspaces_id() + '/users',
            headers=self.HEADERS,
            params={'email': email})
        df_user = pd.DataFrame.from_dict(request.json())
        return df_user['id'].item()

    def clockify_get_time_entries_by_days(self, email, start_date, end_date):
        request = requests.get(
            self.BASE_URL + '/workspaces/' + self._get_workspaces_id() +
            '/user/' + self._get_user_id(email) + '/time-entries',
            headers=self.HEADERS,
            params={'start': start_date + 'T00:00:00.001Z', 'end': end_date + 'T23:59:59.999Z',
                    'page-size': 1000, 'in-progress': False})
        request_json = request.json()
        return request_json

    def clockify_add_new_time_entry(self, start_datetime, end_datetime, description, project_id, task_id):
        request = requests.post(
            self.BASE_URL + '/workspaces/' + self._get_workspaces_id() +
            '/time-entries',
            headers=self.HEADERS,
            json={
                'start': start_datetime
                , 'end': end_datetime
                , "billable": "true"
                , "description": description
                , "projectId": project_id
                , "taskId": task_id
            })
        return request.text

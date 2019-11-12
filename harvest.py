from datetime import datetime

import requests
import calendar

import settings


class Harvest:
    user_id = None
    headers = {
        "User-Agent": "Harvest API Example",
        "Authorization": "Bearer " + settings.HARVEST_ACCESS_TOKEN,
        "Harvest-Account-ID": settings.HARVEST_ACCOUNT_ID,
        "Content-Type": "application/json",
    }
    projects = None
    tasks = None
    selected_project = None
    selected_task = None
    notes = None

    def make_request(self, url, data=None, method='GET'):
        if method == "GET":
            r = requests.get(url=url, headers=self.headers)
        elif method == "POST":
            r = requests.post(url=url, headers=self.headers, json=data, allow_redirects=False)
        return r.json()

    def get_workingdays(self):
        cal = calendar.Calendar()
        now = datetime.now()
        return [x for x in cal.itermonthdays2(now.year, now.month) if x[0] != 0 and x[1] < 5]

    def generate_time(self, project_id, task_id, spent_date):
        data = {"user_id": self.user_id, "project_id": project_id, "task_id": task_id, "spent_date": spent_date,
                "hours": 8.0}
        if self.notes:
            data["notes"] = self.notes
        self.make_request(settings.TIME_URL, data=data, method="POST")

    def get_projects(self):
        user = self.make_request(settings.USER_URL)
        self.user_id = user.get("id")
        projects = self.make_request(settings.PROJECT_URL.format(user_id=self.user_id))

        projects_assignments = projects['project_assignments']

        self.projects = list(map(lambda x: {'client': x['client']['name'], 'project': x['project']['name'],
                                            'project_id': x['project']['id'],
                                            'task_assignments': x['task_assignments']}, projects_assignments))
        return self.projects

    def set_project(self, project_pos):
        self.selected_project = self.projects[project_pos-1]

    def set_task(self, task_pos):
        self.selected_task = self.selected_project["task_assignments"][task_pos-1]['task']

    def set_notes(self, notes):
        self.notes = notes

    def make_sheet(self):
        dates = self.get_workingdays()
        actual_month = datetime.now().month
        actual_year = datetime.now().year
        for date in dates:
            self.generate_time(self.selected_project['project_id'], self.selected_task['id'],
                               datetime(year=actual_year, month=actual_month, day=date[0]).strftime('%Y-%m-%d'))

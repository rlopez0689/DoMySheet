from harvest import Harvest


harvest = Harvest()

print("Let me do you sheet :)")
projects = harvest.get_projects()
for index, project in enumerate(projects):
    print(index+1, project['client'], project['project'])

harvest.set_project(int(input("select project \n")))

for index, task in enumerate(harvest.selected_project["task_assignments"]):
    print(index+1, task['task']['name'])

harvest.set_task(int(input("select Task \n")))

notes = input("Any notes for the task?")
if notes:
    harvest.set_notes(notes)

harvest.make_sheet()

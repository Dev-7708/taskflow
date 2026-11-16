# TaskFlow

A team task management application — create projects, invite members, assign tasks,
and move them across a drag-and-drop Kanban board.

Built as a REST API first, so the same backend serves both a web client and a
Flutter mobile client.

## Status

🚧 In development. Built step by step; see commit history.

- [ ] Django project + PostgreSQL schema
- [ ] Token authentication
- [ ] Projects, memberships, role-based permissions
- [ ] Tasks CRUD + filtering, pagination, search
- [ ] Kanban board UI
- [ ] Docker + deployment
- [ ] Flutter mobile client

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL |
| Web UI | HTML, CSS, JavaScript |
| Mobile | Flutter (Dart) |
| Infra | Docker, Render |

## Roles

| Role | Permissions |
|---|---|
| Owner | Full control of the project, including deletion and member management |
| Member | Create, edit and move tasks |
| Viewer | Read-only access |

## Author

Dev Pratap Singh

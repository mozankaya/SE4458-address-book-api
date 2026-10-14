# Address Book API

SE4458 Assignment 2 – Group 1 (Address Book)
Student: Mehmet Ozan Kaya

A simple REST API to create, edit, update, delete, search, sort and favorite contacts.
Built with **FastAPI** and deployed on **Vercel**. Data is stored in memory.

- **Source code:** https://github.com/YOUR_USERNAME/address-book-api
- **Live API (Swagger):** https://YOUR_PROJECT.vercel.app/docs

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/contacts` | List contacts (search, tag/favorite filter, sort, pagination) |
| GET | `/contacts/{id}` | Get one contact |
| POST | `/contacts` | Create a contact |
| PUT | `/contacts/{id}` | Update all fields of a contact |
| PATCH | `/contacts/{id}` | Edit only the sent fields |
| DELETE | `/contacts/{id}` | Delete a contact |
| PATCH | `/contacts/{id}/favorite` | Toggle favorite |

`GET /contacts` query parameters: `search`, `tag`, `favorite`, `sort_by` (`first_name`, `last_name`, `email`), `order` (`asc`, `desc`), `page`, `page_size`.

Example: `GET /contacts?search=alan&sort_by=last_name&order=desc`

## Design

- `app/main.py` – FastAPI app and endpoints
- `app/models.py` – Pydantic models for validation and Swagger docs
- `app/store.py` – in-memory database (a Python dict) with search/filter/sort logic and sample data
- `api/index.py` + `vercel.json` – Vercel entry point; all requests are routed to the FastAPI app

Swagger UI is generated automatically by FastAPI at `/docs`. The base URL redirects there.

## Assumptions

- First name and last name are required; email, phone and tags are optional (as in the "Add New Contact" form).
- Email must have a basic `name@domain.com` format.
- Search is case-insensitive and looks at name, email and tags.
- Tags are free text, there is no fixed tag list.
- 8 sample contacts are loaded on startup so the API is not empty. Their emails use the reserved `example.com` domain.
- No authentication, since the API should be publicly available.

## Issues encountered

- **In-memory data on Vercel:** Vercel runs the app as a serverless function. When it is idle it shuts down, and the next request starts with fresh memory, so added contacts can disappear and the sample data comes back. This is expected with an in-memory database on serverless hosting.

<!-- TODO: add the problems you actually hit while building/deploying -->

## Run locally

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs. Run tests with `pytest`.

## Deploy

Push to GitHub, import the repo in Vercel (framework preset: **Other**) and deploy.
If `/docs` asks for a Vercel login, turn off *Deployment Protection* in the project settings.

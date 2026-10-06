# Openbook

Booking and client management for salons, clinics and wellness studios. (Working name.)

## Run locally

    cp .env.example .env
    docker compose up --build

- API: http://localhost:8000 (docs at /docs)
- Landing page: http://localhost:8080

## Tests

    cd backend && pip install -r requirements.txt && pytest -q

## Branches

- `main`: production, deploys on merge (added in Stage 4)
- `dev`: integration branch; open PRs into `dev`

## Stages

1. Foundation: repo, Docker, CI, landing page and waitlist (done)
2a. Tenants, signup/login, migrations (done)
2b. Billing with Razorpay
3. Clients, services, staff, appointments, reminders
4. Production infrastructure

## Database migrations

    cd backend
    alembic revision --autogenerate -m "describe the change"
    alembic upgrade head

## Rule for every business table

Add `tenant_id`, depend on `current_tenant_id` in the route, and filter every query by it.

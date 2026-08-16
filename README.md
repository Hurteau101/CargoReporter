# Cargo Reporter

A Django web app built for a client to track air cargo shipments, SLA (service level agreements), duplicate AWBs, freighter status, and shipment scanning, from a single dashboard. Frontend design was provided by the client.

https://cargo-reporter.ca/


## Features

- **SLA Report Upload** - Upload an Excel/CSV export and the system parses, validates, and groups it by destination automatically
- **SLA Tracking** - Tracks and displays the SLA of the uploaded AWBs.
- **Under-30-Hours Tracking** - Flags AWBs approaching their deadline before they pass
- **Duplicate AWB Detection** - Automatically detects and lists AWB numbers that appear more than once in an upload
- **Freighter Tracking** - Tracks aircraft type, tail/flight number, route, status (active, delayed, in maintenance, etc.), and station notification state
- **AWB Status & Photos** - Attach status updates and images (via Cloudinary) to individual AWBs. This allows to track the location of the AWB in the warehouse
- **AWB Scanner** - A barcode/number scanning view for logging AWBs by destination, with scan counts and full-order tracking
- **Client Directory** - Stores client contacts and their associated destination
- **Selective & Mass Data Clearing** - Clear individual data tabs or wipe all tracked data (including cleaning up stored images) in one action
- **Restricted Google Login** - Google OAuth login limited to an admin-managed allow-list of email addresses

## Tech Stack

- **Backend:** Django 6.0
- **Auth:** django-allauth (Google OAuth with custom allow-list adapter)
- **Data Processing:** pandas, openpyxl (Excel/CSV parsing)
- **Image Storage:** Cloudinary
- **Frontend:** Django templates, Tailwind CSS (design provided by client)
- **Database:** PostgreSQL (via psycopg2)


## Getting Started

### Prerequisites

- Python
- PostgreSQL
- A Cloudinary account (for image storage)
- Google OAuth credentials (for login)

### Installation

```bash
# Clone the repository
git clone https://github.com/Hurteau101/CargoReporter.git
cd CargoReporter

# Create a virtual environment
python -m venv venv

# Activate it
Windows - venv\Scripts\activate | Linux - venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with your database credentials, Cloudinary keys (`CLOUD_NAME`, `API_KEY`, `API_SECRET`), and Google OAuth credentials.

### Running the App

```bash
# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

## How It Works

1. A user uploads the daily SLA report (Excel/CSV) from the homepage.
2. The file is validated for the expected column headers, then parsed and grouped by destination with pandas.
3. Rows are automatically split into SLA breaches, under-30-hour warnings, and duplicate AWBs, and saved to the database
4. Staff can browse each category, log AWBs via the scanner, track freighter status, and attach photos/status notes to individual shipments
5. Any tab (or all data at once) can be cleared from the dashboard, including associated Cloudinary images

## Screenshots
<img width="1797" height="677" alt="awb scanned" src="https://github.com/user-attachments/assets/914adf4f-f7a9-41cc-8944-1e5c7a00976f" />
<img width="1820" height="476" alt="SLA" src="https://github.com/user-attachments/assets/0e34e58d-d783-42c5-a41b-40ca00cdd4a9" />
<img width="1901" height="872" alt="Homepage" src="https://github.com/user-attachments/assets/a34def16-e256-44b3-8866-10c667ab10bb" />

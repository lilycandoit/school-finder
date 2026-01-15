# NSW School Finder

A location-first web application that helps migrant parents in New South Wales (NSW), Australia find and compare nearby schools using official open government data.

## Features

- **Location-based search**: Find schools by suburb or postcode
- **Distance calculation**: Schools shown with distance from your location
- **School details**: View comprehensive information about each school
- **Comparison tool**: Compare up to 3 schools side-by-side
- **Mobile-first design**: Optimized for mobile devices
- **Accessible**: Designed for users with limited English

## Tech Stack

- **Backend**: FastAPI
- **Database**: SQLite with SQLModel
- **Templates**: Jinja2
- **Styling**: TailwindCSS
- **Deployment**: Fly.io

## Setup

### Prerequisites

- Python 3.12+
- pip

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd school-finder
```

2. **Create a virtual environment (recommended):**

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. **Install dependencies:**

```bash
# If using virtual environment (activated above):
pip install -r requirements.txt

# OR if not using virtual environment, use pip3:
pip3 install -r requirements.txt
```

4. **Load data into database:**

```bash
# Make sure virtual environment is activated if you're using one
python3 scripts/load_data.py
```

This will:

- Create the SQLite database
- Load schools from `master_dataset.csv`
- Load postcodes from `data/postcodes_nsw.csv` (if available)

### Running Locally

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## Data Sources

- **Schools Data**: NSW Department of Education Master Dataset

  - Source: https://data.nsw.gov.au/data/dataset/nsw-education-nsw-public-schools-master-dataset
  - File: `master_dataset.csv`

- **Postcode Centroids**: NSW postcode centroid data
  - File: `data/postcodes_nsw.csv`
  - Note: If postcode data is not available, the app will use fallback geocoding (median of schools in suburb)

## Deployment

### Fly.io

1. Install Fly CLI:

```bash
curl -L https://fly.io/install.sh | sh
```

2. Login to Fly:

```bash
fly auth login
```

3. Create volume for database:

```bash
fly volumes create school_finder_data --size 1 --region syd
```

4. Deploy:

```bash
fly deploy
```

## Project Structure

```
school-finder/
├── app/
│   ├── models/          # Database models
│   ├── controllers/     # Business logic
│   ├── routes/          # FastAPI routes
│   ├── templates/       # Jinja2 templates
│   ├── utils/           # Utilities
│   └── static/          # Static files
├── data/                # Data files
├── scripts/             # Utility scripts
├── main.py              # FastAPI app
└── requirements.txt     # Dependencies
```

## Important Notes

### ICSEA Values

ICSEA (Index of Community Socio-Educational Advantage) values are displayed with the following explanation:

> "ICSEA shows the general socio-educational background of students at a school. It does not measure school quality or teaching performance."

ICSEA values are:

- Only shown on the school detail page
- Never labeled as "good" or "bad"
- Never used for ranking or recommendations

### Data Privacy

- All data is from public government sources
- No user data is collected or stored
- No authentication required

## License

This project uses data from the NSW Department of Education under Creative Commons Attribution license.

## Credits

A Vibecamp Creation

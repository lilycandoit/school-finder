# NSW School Finder

A location-based web application that helps **migrant parents and newly arrived families in New South Wales** find, understand, and compare nearby schools using **official NSW open government data**.

This project is built with a strong focus on **accessibility**, **ethical data use**, and **reducing cognitive load** for parents who may be unfamiliar with the NSW education system or are not native English speakers.

---

## Why this project exists

Finding a school in NSW can be overwhelming — especially for migrant families. Government websites are information-rich but often:

* Use complex education terminology
* Assume local system knowledge
* Scatter important details across multiple pages

**NSW School Finder** brings everything together in one clear, parent-friendly interface.

> **Fun fact:** I originally built this app for myself and my future kids.
> Because of that, I pay close attention to the small details that actually matter when parents are making real decisions.

---

## Key Features

### Search & Discovery

* Search schools by **suburb** or **postcode**
* Adjustable **radius** to control distance
* Supports **primary, secondary, and special-purpose schools**

### Practical Filters

* Preschool on site
* English language support
* Opportunity classes (OC)
* Selective / non-selective schools
* Distance education availability

### Clear School Cards

* School name, level, and location
* Distance from searched area
* Enrolment size (small / medium / large)
* Quick access to detailed view

### Compare Schools

* Select and compare **up to 3 schools side-by-side**
* Designed to support real decision-making, not just browsing

### Detailed School Pages

Each school page includes:

* Contact details and website
* Student numbers
* Multilingual background percentage
* Learning support options
* Programs offered
* ICSEA value with a **plain-English explanation**

### Plain-English Explanations

Complex NSW education terms are translated into **simple, friendly language**, including:

* Selective schools
* Opportunity classes (OC)
* Intensive English support
* Schools for specific purposes

This is especially helpful for families with **non-native English backgrounds**.

---

## Tech Stack

* **Backend:** FastAPI
* **ORM:** SQLAlchemy
* **Database:** SQLite
* **Templating:** Jinja2
* **Styling:** Tailwind CSS
* **Deployment:** Vercel

---

## Data Source

* **NSW Open Education Dataset**
* Data is used **read-only** and displayed transparently
* No modification or ranking of schools beyond official data

This project follows principles of **ethical data use** and avoids misleading comparisons.

---

## Design Principles

* **Accessibility first** – readable layouts, clear labels, minimal clutter
* **Low cognitive load** – only show what parents need at each step
* **Trustworthy data** – official government sources only
* **Human-centred design** – built around real parent questions, not technical metrics

---

## Performance & Accessibility

This app is optimised for speed and inclusivity:

**Performance**
* Bounding box pre-filtering reduces distance calculations from ~3000 to ~100 schools
* Database indexes on all filter fields for fast queries
* Gzip compression for smaller response sizes
* Haversine formula for accurate distance calculations

**Accessibility**
* Skip-to-content link for keyboard navigation
* ARIA labels on interactive elements
* Semantic HTML with proper heading hierarchy
* Form fieldsets with legends for screen readers
* WCAG-compliant text contrast ratios
* Mobile-responsive comparison table with scroll hints

---

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

2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Load data into database:

```bash
python3 scripts/load_data.py
```

This will:

- Create the SQLite database
- Load schools from `master_dataset.csv`
- Load postcodes from `data/postcodes_nsw.csv`

### Running Locally

```bash
python3 main.py
```

Or alternatively:

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

---

## Future Improvements

Planned ideas include:

* Saving favourite schools
* Additional explanations for NSW-specific concepts
* Map view for school locations

This app will continue to evolve as new ideas — and real parenting needs — come up.

---

## Who this is for

* Migrant parents new to NSW
* Families with non-native English backgrounds
* Anyone who wants a **clear, calm, and honest** way to explore NSW schools

---

## Feedback

If you have suggestions, questions, or ideas — especially from a parent's perspective — I'd love to hear them.

This project is personal, practical, and built with care.

---

## License

This project uses data from the NSW Department of Education under Creative Commons Attribution license.

## Credits

A Vibecamp Creation

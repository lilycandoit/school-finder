---
name: NSW School Finder MVP
overview: Build a location-first web app for migrant parents to find and compare nearby NSW schools using official government data. Server-rendered FastAPI app with SQLite, following MVC architecture and Vibecamp design system.
todos: []
---

# NSW School Finder - Implementation Plan

## Plan Overview

Build a simple, accessible web application that helps migrant parents in NSW find schools near their location. The app prioritizes clarity, simplicity, and ethical data presentation.

## Architecture Overview

```
User Input (suburb/postcode)
  → Geocoding (postcode CSV or suburb median)
  → Haversine distance calculation
  → Filter schools by radius
  → Display results with comparison capability
```

## Key Design Decisions

### Geocoding Strategy

1. **Postcode Input**: Lookup in bundled NSW postcode centroid CSV
2. **Suburb Input**:

   - First: Try bundled suburb centroid table (if available)
   - Fallback: Compute median lat/lon from schools in that suburb (and postcode if provided)

3. **Distance**: Haversine formula for radius filtering

### Data Handling

- Load `master_dataset.csv` into SQLite on first run
- Index on `Latitude`, `Longitude`, `Town_suburb`, `Postcode` for performance
- Handle missing data gracefully (display "Not available")

### ICSEA Ethical Display

- Only show ICSEA on detail page
- Include explanation: "ICSEA shows the general socio-educational background of students at a school. It does not measure school quality or teaching performance."
- Never label as good/bad or high/low

## Project Structure

```
school-finder/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── school.py              # SQLModel School model
│   ├── controllers/
│   │   ├── geocoding.py           # Postcode/suburb → lat/lon conversion
│   │   ├── distance.py            # Haversine formula implementation
│   │   └── school_controller.py   # School search and filtering logic
│   ├── routes/
│   │   └── school_routes.py       # FastAPI route handlers
│   ├── templates/
│   │   ├── base.html              # Base template with Vibecamp design
│   │   ├── index.html             # Home page (location input)
│   │   ├── results.html           # Results page (schools list)
│   │   ├── detail.html            # School detail page
│   │   └── compare.html           # Compare page (up to 3 schools)
│   ├── utils/
│   │   ├── database.py            # Database setup and connection
│   │   └── data_loader.py         # CSV → SQLite import script
│   └── static/
│       ├── img/
│       │   └── vc-logo.svg        # Vibecamp logo
│       └── css/                    # Custom CSS if needed
├── data/
│   ├── master_dataset.csv         # NSW schools dataset
│   └── postcodes_nsw.csv          # NSW postcode centroids (to be sourced)
├── scripts/
│   └── load_data.py               # Script to import CSV into SQLite
├── main.py                         # FastAPI app entry point
├── requirements.txt               # Python dependencies
├── fly.toml                        # Fly.io deployment config
└── README.md                       # Project documentation
```

## Implementation Steps

### Phase 1: Project Setup & Data Infrastructure

1. **Initialize FastAPI Application**

   - Set up `main.py` with lifespan context manager
   - Configure Jinja2 templates and static files
   - Apply Vibecamp design system (black/white, Kalam/Inter fonts)

2. **Database Setup**

   - Create SQLModel School model matching CSV columns
   - Set up async SQLite connection with volume support (`/data` on Fly.io)
   - Create database initialization function

3. **Data Loading**

   - Create `scripts/load_data.py` to import `master_dataset.csv` into SQLite
   - Handle data type conversions (strings to floats for lat/lon, etc.)
   - Create indexes on `Latitude`, `Longitude`, `Town_suburb`, `Postcode`
   - Handle missing/null values appropriately

4. **Postcode Dataset**

   - Source and bundle NSW postcode centroid CSV
   - Create Postcode model for lookup table
   - Load postcode data into SQLite

### Phase 2: Core Functionality

5. **Geocoding Module**

   - Implement postcode → lat/lon lookup
   - Implement suburb → lat/lon (with fallback to median of schools)
   - Handle edge cases (invalid postcode/suburb, multiple matches)

6. **Distance Calculation**

   - Implement Haversine formula in `app/controllers/distance.py`
   - Test with known coordinates

7. **School Search Controller**

   - Query schools within radius using Haversine
   - Filter by school level and sector
   - Sort by distance (closest first)
   - Handle empty results gracefully

### Phase 3: Routes & Pages

8. **Home Page Route** (`/`)

   - Simple form: suburb/postcode input, radius selector (3km/5km/10km)
   - Submit to `/results` via POST
   - Mobile-first design with large touch targets

9. **Results Page Route** (`/results`)

   - Display school cards with key info (name, level, sector, distance, enrolment)
   - Filters for level and sector
   - Checkboxes for comparison (max 3)
   - "View details" buttons linking to detail page
   - "Compare selected" button

10. **School Detail Route** (`/school/{school_id}`)

    - Display all available school information
    - Show ICSEA with explanation text
    - Handle missing fields ("Not available")
    - "Add to comparison" button

11. **Compare Route** (`/compare`)

    - Accept up to 3 school IDs via query params
    - Display comparison table
    - Include ICSEA explanation
    - No recommendations or highlighting

### Phase 4: UI/UX Polish

12. **Templates Implementation**

    - Base template with Vibecamp branding
    - Mobile-responsive design (TailwindCSS)
    - Accessible forms and navigation
    - Clear error messages

13. **Error Handling**

    - Invalid suburb/postcode → friendly error message
    - No schools found → helpful message
    - Database errors → graceful fallback

### Phase 5: Deployment

14. **Fly.io Configuration**

    - Create `fly.toml` with volume mount for `/data`
    - Configure environment variables
    - Set up volume for SQLite persistence

15. **Testing & Documentation**

    - Test geocoding with various inputs
    - Test distance calculations
    - Test comparison functionality
    - Update README with setup instructions

## Improvements & Recommendations

### 1. **Accessibility Enhancements**

- Add ARIA labels to all form inputs
- Ensure keyboard navigation works
- High contrast ratios (already covered by black/white design)
- Screen reader friendly labels

### 2. **Error Handling**

- Validate suburb/postcode format before geocoding
- Show helpful suggestions if input doesn't match
- Clear messaging when no schools found in radius

### 3. **Performance Optimizations**

- Database indexes on frequently queried columns
- Consider caching geocoding results (optional for MVP)
- Limit results to top 50 schools (closest) to avoid overwhelming UI

### 4. **Data Quality**

- Handle "np" values in Indigenous/LBOTE percentages
- Validate lat/lon ranges for NSW (rough bounds check)
- Handle schools with missing coordinates

### 5. **User Experience**

- Show loading state during search
- Display result count ("Found 12 schools within 5km")
- Breadcrumb navigation on detail/compare pages
- "Back to results" links

## Free Deployment Platform: Fly.io

**Recommended: Fly.io** (already in your rules)

**Why Fly.io:**

- Free tier: 3 shared-cpu-1x VMs (sufficient for MVP)
- Persistent volumes for SQLite database
- Excellent FastAPI support
- Easy deployment from GitHub
- Automatic HTTPS
- No credit card required for free tier

**Alternative Options:**

- **Render**: Free tier but spins down after inactivity (not ideal for SQLite)
- **Railway**: $5/month credit, then pay-as-you-go
- **PythonAnywhere**: Free tier available but more limited

**Fly.io Setup:**

1. Create account (no credit card needed)
2. Install `flyctl` CLI
3. Run `fly launch` to generate `fly.toml`
4. Create volume: `fly volumes create school_finder_data --size 1 --region syd`
5. Configure volume mount in `fly.toml`
6. Deploy: `fly deploy`

## Data Sources

1. **Schools Data**: `master_dataset.csv` (already provided)
2. **Postcode Centroids**: Need to source NSW postcode centroid CSV

   - Options: Australian Bureau of Statistics, Geoscience Australia, or community datasets
   - Format needed: postcode, latitude, longitude

## Technical Considerations

### Database Schema

- School model: All CSV columns as nullable fields
- Postcode model: postcode (PK), latitude, longitude
- Indexes: `(Latitude, Longitude)`, `Town_suburb`, `Postcode`

### Haversine Formula

```python
def haversine(lat1, lon1, lat2, lon2):
    # Returns distance in kilometers
    # R = 6371 km (Earth's radius)
```

### Geocoding Fallback Logic

```python
def geocode_location(suburb=None, postcode=None):
    if postcode:
        # Try postcode lookup first
        result = lookup_postcode(postcode)
        if result:
            return result

    if suburb:
        # Try suburb centroid table
        result = lookup_suburb(suburb, postcode)
        if result:
            return result

        # Fallback: median of schools in suburb
        return compute_suburb_median(suburb, postcode)
```

## Success Criteria

- [ ] User can enter suburb/postcode and find nearby schools
- [ ] Distance filtering works accurately (Haversine)
- [ ] School details display correctly with "Not available" for missing data
- [ ] ICSEA shown only on detail page with explanation
- [ ] Comparison works for up to 3 schools
- [ ] Mobile-responsive design
- [ ] Accessible to users with limited English
- [ ] Deployed and accessible on Fly.io

## Non-Goals (Reinforced)

- No user accounts/authentication
- No school rankings or recommendations
- No maps or directions
- No external APIs (except bundled datasets)
- No reviews/comments
- No catchment boundaries
- No NAPLAN scores

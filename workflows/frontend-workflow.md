# Frontend Workflow & User Experience Architecture

## 1. Frontend Technology Stack

The BloodConnect frontend is engineered for responsive, high-contrast, accessible design with glassmorphic aesthetics.

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Templating Engine** | Django Template Language (DTL) | Server-Side Rendering (SSR) of dynamic views, conditional layouts, and CSRF token injection |
| **CSS Framework** | Bootstrap 5.3.0 + Custom CSS | Responsive layout grid, modern utilities, and custom glassmorphism design (`static/css/style.css`) |
| **Iconography** | Bootstrap Icons 1.10.5 | Visual indicators for statuses, metrics, navigation, and badges |
| **Notification Engine** | Toastify.js | Client-side reactive toast alerts populated from Django's backend message framework |
| **Mapping Engine** | Leaflet.js 1.9.4 | Interactive OpenStreetMap integration plotting hospital coordinates and regional centers |
| **Data Visualization** | Chart.js | Dynamic bar and doughnut charts visualizing real-time blood deficit distributions |

---

## 2. Template Architecture & Inheritance Hierarchy

The frontend uses a unified master layout (`base.html`) providing the persistent navigation bar, brand assets, footer, and automated notification handling script.

```mermaid
flowchart TD
    Base["base.html<br/>• Glassmorphism Navbar<br/>• Dynamic Role Links<br/>• Toastify Message Engine<br/>• Footer"]

    Base --> Index["index/index.html<br/>• Hero Section<br/>• Mission Statement<br/>• Registration CTAs"]
    Base --> AuthGroup["accounts/ Templates"]
    Base --> DonorGroup["Donor Views (index/)"]
    Base --> HospGroup["Hospital Views (index/)"]
    Base --> AdminGroup["Admin Views (index/)"]

    AuthGroup --> Login["accounts/login.html"]
    AuthGroup --> RegDonor["accounts/register_donneur.html"]
    AuthGroup --> RegHosp["accounts/register_hopital.html"]

    DonorGroup --> DashDonor["index/dashboard_donneur.html<br/>• Donor Tier Badge & Points<br/>• Next Eligible Date Indicator<br/>• Active Urgent Requests<br/>• Booked Campaigns List"]
    DonorGroup --> ProfileDonor["index/profil_donneur.html<br/>• Personal Info & Blood Group"]
    DonorGroup --> RecordDon["index/enregistrer_don.html<br/>• Self-reported Donation Entry"]
    DonorGroup --> ListCamp["index/list_campagnes.html<br/>• Blood Drive Schedule & Time-slot Selector"]

    HospGroup --> DashHosp["index/dashboard_hopital.html<br/>• Active Blood Requests<br/>• Donor Responses Feed<br/>• Campaign Schedules"]
    HospGroup --> CreateDemande["index/create_demande.html<br/>• Blood Group, Quantity, Deadline"]
    HospGroup --> EditDemande["index/edit_demande.html"]
    HospGroup --> CreateCamp["index/create_campagne.html<br/>• Date, Place, Target Groups, Quota"]

    AdminGroup --> DashAdmin["index/dashboard_admin.html<br/>• Accreditation Verification Panel<br/>• Leaflet Hospital Map<br/>• Chart.js Blood Group Stats<br/>• CSV Export Trigger"]
```

---

## 3. Global Notification & Toast Notification Workflow

Django sends flash messages (`messages.success`, `messages.error`, `messages.warning`, `messages.info`) during view redirects. The frontend captures these in an invisible DOM container and dynamically converts them to animated Toastify notifications on DOM load.

```mermaid
sequenceDiagram
    autonumber
    actor User as User Browser
    participant Django as Django Template (base.html)
    participant DOM as Hidden DOM Container
    participant Toast as Toastify.js Engine

    User->>Django: Submit form (e.g. Register, Respond, Book)
    Django->>Django: Process View & Attach messages.success("...")
    Django-->>User: Render HTML with embedded message tags
    User->>DOM: Parse <span class="django-message" data-message="..." data-tags="...">
    DOM->>Toast: Trigger Toastify constructor with color mapping:
    Note over Toast: success -> #10b981 (Green)<br/>error -> #ef4444 (Red)<br/>warning -> #eab308 (Amber)<br/>info -> #3b82f6 (Blue)
    Toast-->>User: Display animated Toast alert in upper right corner (4000ms)
```

---

## 4. Persona User Journeys & Screen Transitions

### A. Volunteer Donor User Journey

```mermaid
stateDiagram-v2
    [*] --> LandingPage: Visits BloodConnect
    LandingPage --> DonorRegistration: Clicks "Je suis donneur"
    DonorRegistration --> DonorDashboard: Successful Sign-up (Auto-login)
    
    state DonorDashboard {
        [*] --> ViewStatus: Check Level, Points & Next Eligible Date
        ViewStatus --> ActiveRequests: Browse Urgent Blood Needs
        ViewStatus --> BookCampaigns: Browse Blood Drive Campaigns
        ViewStatus --> LogDonation: Enter Past Blood Donation
        ViewStatus --> ToggleAvailability: Flip Active/Inactive Switch
    }

    ActiveRequests --> SubmitResponse: Click "Répondre"
    SubmitResponse --> DonorDashboard: +25 Points Awarded & Request Marked

    BookCampaigns --> SelectSlot: Choose Available Time Slot
    SelectSlot --> DonorDashboard: +50 Points Awarded & Slot Reserved

    LogDonation --> RecordSuccess: Enter Date & Hospital
    RecordSuccess --> DonorDashboard: +100 Points Awarded & Delay Recalculated
```

### B. Hospital Staff User Journey

```mermaid
stateDiagram-v2
    [*] --> HospitalRegistration: Clicks "Espace hôpital"
    HospitalRegistration --> PendingApproval: Awaiting Admin Accreditation
    PendingApproval --> HospitalDashboard: Admin Validates Hospital

    state HospitalDashboard {
        [*] --> Overview: Active Needs & Scheduled Campaigns
        Overview --> CreateUrgentRequest: Clicks "Nouvelle demande"
        Overview --> ManageRequests: Edit Details or Mark "Clôturée"
        Overview --> CreateCampaign: Clicks "Créer une campagne"
        Overview --> ViewResponses: See Volunteer Donors Responding
    }

    CreateUrgentRequest --> HospitalDashboard: Broadcast to All Matching Donors
    CreateCampaign --> HospitalDashboard: Public Blood Drive Published
```

### C. Platform Administrator User Journey

```mermaid
stateDiagram-v2
    [*] --> AdminDashboard: Login as Staff / Superuser
    
    state AdminDashboard {
        [*] --> HospitalApprovalSection: Review Pending Facilities
        [*] --> MapSection: Inspect Geocoded Hospital Facilities
        [*] --> StatisticsSection: Review Blood Group Supply/Deficit (Chart.js)
        [*] --> DonorRegistry: Filter & Review Registered Donors
    }

    HospitalApprovalSection --> ValidateHospital: Click "Valider" (POST)
    ValidateHospital --> AdminDashboard: Hospital Instantly Unlocked

    DonorRegistry --> ExportCSV: Click "Exporter CSV"
    ExportCSV --> AdminDashboard: Download UTF-8 BOM CSV File
```

---

## 5. Client-Side Interactive Components

### Leaflet.js Hospital Geospatial Map
On `dashboard_admin.html`, Leaflet initializes a dark/light tile layer and evaluates embedded hospital records:
```javascript
// Initializes center on national coordinates
const map = L.map('map').setView([36.8065, 10.1815], 7);
// Iterates through hospital queryset and drops custom markers
// displays popup with hospital name, accreditation number, and validation badge
```

### Chart.js Blood Group Deficit Visualization
On `dashboard_admin.html`, Chart.js reads aggregated active emergency requests:
```javascript
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'],
        datasets: [{ label: 'Demandes Actives', data: [...] }]
    }
});
```

# VITALSTREAM
### UNESCO Global Blood Initiative & Emergency Hemodynamic Intelligence Grid

VitalStream is a mission-critical web intelligence console connecting hospital transfusion banks with compatible volunteer blood donors in real time while enforcing biological cooldowns and clinical safety protocols.

---

## 🏛️ UNESCO Global Health Initiative Overview

VitalStream shifts blood donation from a localized manual process to an **internationally coordinated algorithmic grid**:
* **Biological Interval Enforcement**: Enforces biological cooldown intervals (56 days for men, 84 days for women) calculating dynamic eligibility from each donor's last validated donation.
* **Triage & Emergency Dispatch**: Certified medical centers publish urgent requisitions specifying blood group, quantity, and deadline. Compatible regional donors receive instant alerts.
* **Citizen Donor Gamification**: Donors earn XP across platform interactions (+100 XP for donation, +50 XP for blood drive booking, +25 XP for emergency response) progressing through 4 honorary citizen tiers:
  * 🥇 **Sauveur d'Or** (1,000+ XP)
  * 🥈 **Héros d'Argent** (500–999 XP)
  * 🥉 **Goutte de Bronze** (100–499 XP)
  * 🌱 **Nouveau Donneur** (0–99 XP)
* **Hospital Accreditation Gateway**: Unverified facilities register and remain locked until formal accreditation by a platform administrator.
* **Interactive Tactical Maps & Telemetry**: Integrated CartoDB dark matter maps (Leaflet.js) and hemodynamic deficit telemetry (Chart.js).

---

## 🎨 Design System & Color Tokens

VitalStream features a tactical, high-contrast clinical HUD interface exceeding WCAG 2.2 AAA readability standards:

* **Abyssal Space Indigos (`#03060F`, `#0B132B`, `#151F3D`)**: Reduces cognitive fatigue in clinical settings.
* **Vital Arterial Crimson (`#EF233C`, `#D90429`, `#FF4D6D`)**: Applied to urgent requisitions, blood group badges, and critical deficit indicators.
* **Bioluminescent Cyan & Emerald (`#00F5D4`, `#10B981`)**: Signals clinical safety, eligible biological donor states, accredited hospitals, and successful matches.
* **Typography**: `Space Grotesk` (headings), `Plus Jakarta Sans` (body), and `JetBrains Mono` (tabular numbers and blood pills).

---

## 📁 Repository Structure

```
VITALSTREAM/
├── BloodConnect/                      # Django Full-Stack Application
│   ├── accounts/                      # Authentication & Registration Controllers
│   ├── bloodconnect/                  # Core Project Configuration & Routing
│   ├── index/                         # Models, Views, Forms, and Modern Templates
│   │   ├── templates/                 # Rebuilt UNESCO VitalStream Templates
│   │   │   ├── accounts/              # Login & Enrolment Interfaces
│   │   │   └── index/                 # Dashboards & Requisition Terminals
│   │   ├── models.py                  # Relational Schemas (Donneur, Hopital, Demande, etc.)
│   │   └── views.py                   # Role-based View Controllers & Dispatch Logic
│   ├── static/                        # Production Assets & Tactical CSS Styles
│   │   └── css/style.css              # VitalStream Design Tokens & Animations
│   ├── db.sqlite3                     # SQLite3 Database (Pre-seeded Demo Accounts)
│   └── manage.py                      # Django CLI Manager
├── workflows/                         # Complete System Architecture Documentation
│   ├── README.md                      # Architecture Overview & Role Maps
│   ├── frontend-workflow.md           # Template Tree & Client UX Architecture
│   ├── backend-workflow.md            # MVT Request Lifecycle & Business Engines
│   ├── database-workflow.md           # Entity-Relationship (ER) Models & State Machines
│   └── full-stack-integration-workflow.md # End-to-End Sequence Diagrams
├── .gitignore                         # Git Ignore Specifications
└── README.md                          # Main Project Documentation
```

---

## 🚀 Quickstart Guide

### Prerequisites
* Python 3.10+ (Tested on Python 3.14)
* pip / virtualenv

### 1. Clone the Repository
```bash
git clone https://github.com/SunBreaThing441/VITALSTREAM.git
cd VITALSTREAM
```

### 2. Install Dependencies
```bash
python -m pip install django
```

### 3. Launch the Application Server
```bash
cd BloodConnect
python manage.py runserver 127.0.0.1:8001
```

### 4. Access the Live Consoles
* **Command Center Landing**: [http://127.0.0.1:8001/](http://127.0.0.1:8001/)
* **Passerelle Login**: [http://127.0.0.1:8001/accounts/login/](http://127.0.0.1:8001/accounts/login/)
* **Donor Command Deck**: [http://127.0.0.1:8001/dashboard/donneur/](http://127.0.0.1:8001/dashboard/donneur/)
* **Hospital Requisition Terminal**: [http://127.0.0.1:8001/dashboard/hopital/](http://127.0.0.1:8001/dashboard/hopital/)
* **UNESCO Admin Intelligence Console**: [http://127.0.0.1:8001/dashboard/admin/](http://127.0.0.1:8001/dashboard/admin/)

---

## 🔐 Pre-Seeded Accounts for Testing

| Username | Role | Dashboard URL | Capabilities |
| :--- | :--- | :--- | :--- |
| **salmen** | SuperAdmin | `/dashboard/admin/` | Hospital accreditation, deficit analytics, CSV donor export |
| **omar** | Volunteer Donor | `/dashboard/donneur/` | Urgent response pledge, cooldown monitoring, donation logging |
| **charlesnicolle**| Accredited Hospital | `/dashboard/hopital/` | Issue urgent blood requisitions, schedule blood drive campaigns |

---

## 📜 License
This initiative is developed under the [MIT License](BloodConnect/LICENSE).

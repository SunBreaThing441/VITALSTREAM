# BloodConnect Platform — System Architecture & Workflows

Welcome to the comprehensive workflow documentation for the **BloodConnect Platform**. This repository section details the architectural designs, process lifecycles, and data interactions across the **Frontend**, **Backend**, and **Database** tiers.

---

## 📑 Workflow Documentation Index

| Document | Focus Area | Description |
| :--- | :--- | :--- |
| **[1. Frontend Workflow](./frontend-workflow.md)** | Client-side Presentation & UX | Page inheritance, UI navigation journeys for Donors, Hospitals, and Admins, dynamic components (Leaflet, Chart.js, Toastify). |
| **[2. Backend Workflow](./backend-workflow.md)** | Server Logic & Business Rules | Django MVT request-response lifecycle, authentication & RBAC, eligibility calculations (56/84 days), points engine, validation gates. |
| **[3. Database Workflow](./database-workflow.md)** | Data Models & Relational Schemas | Complete Entity-Relationship (ER) diagram, table schemas, foreign key relationships, model lifecycle state machines. |
| **[4. Full-Stack Integration Workflow](./full-stack-integration-workflow.md)** | End-to-End System Interactions | Unified sequence diagrams tracking requests from UI triggers through backend processing down to database commits. |

---

## 🏛️ High-Level System Architecture

BloodConnect is built as an integrated, high-performance Django web application following the **Model-View-Template (MVT)** pattern.

```mermaid
flowchart TB
    subgraph ClientTier["Client / Frontend Tier"]
        UI_Visitor["Public Visitor<br/>Landing Page & Auth"]
        UI_Donor["Volunteer Donor<br/>Dashboard & Actions"]
        UI_Hospital["Hospital Staff<br/>Urgent Requests & Drives"]
        UI_Admin["Superuser / Admin<br/>Validation & Analytics"]
    end

    subgraph PresentationTech["Frontend Presentation Technologies"]
        TPL["Django Templates (Jinja-style)"]
        CSS["Bootstrap 5.3 + Glassmorphism CSS"]
        JS_MAP["Leaflet.js (Map Geolocation)"]
        JS_CHART["Chart.js (Blood Group Distribution)"]
        JS_TOAST["Toastify.js (Feedback Alerts)"]
    end

    subgraph BackendTier["Server / Backend Tier (Django)"]
        ROUTER["URL Dispatcher<br/>(bloodconnect / index / accounts)"]
        AUTH["Authentication & RBAC<br/>(OneToOne User Links)"]
        RULES["Business Rules Engine<br/>- Delay Rules (56/84 days)<br/>- Gamification (Points & Tiers)<br/>- Accreditation Verification"]
        VIEWS["Controller Views<br/>(QuerySet Operations, Forms, CSV Export)"]
    end

    subgraph DataTier["Data / Persistence Tier (SQLite)"]
        DB[(db.sqlite3)]
        TABLES["Relational Tables:<br/>User, Donneur, Hopital, DemandeUrgente,<br/>Don, Campagne, Inscription, ReponseAppel"]
    end

    ClientTier --> PresentationTech
    PresentationTech --> ROUTER
    ROUTER --> AUTH
    AUTH --> VIEWS
    VIEWS <--> RULES
    VIEWS <--> DB
```

---

## 👥 Core Personas & System Roles

```mermaid
flowchart LR
    User([Platform User]) --> CheckAuth{Authenticated?}

    CheckAuth -- No --> Guest[Public Visitor]
    Guest --> G1[View Homepage]
    Guest --> G2[Register as Donor]
    Guest --> G3[Register as Hospital]
    Guest --> G4[Login]

    CheckAuth -- Yes --> RoleSwitch{Account Role}

    RoleSwitch -- is_superuser / is_staff --> Admin[Administrator]
    Admin --> A1[Validate Pending Hospitals]
    Admin --> A2[Monitor National Blood Deficits]
    Admin --> A3[Export Donor CSV Records]

    RoleSwitch -- hasattr 'donneur' --> Donor[Volunteer Donor]
    Donor --> D1[Review Urgent Blood Requests]
    Donor --> D2[Respond to Urgent Appeals]
    Donor --> D3[Register Donation & Gain Points]
    Donor --> D4[Book Campaign Time Slots]
    Donor --> D5[Toggle Availability Status]

    RoleSwitch -- hasattr 'hopital' --> Hospital[Hospital Medical Center]
    Hospital --> H1[Submit Urgent Blood Needs]
    Hospital --> H2[Edit / Close Urgent Requests]
    Hospital --> H3[Schedule Donation Campaigns]
    Hospital --> H4[Track Volunteer Responses]
```

---

## 🚀 Quick Reference Guide

- **Server Root**: `http://127.0.0.1:8001/`
- **Admin Gateway**: `http://127.0.0.1:8001/admin/`
- **Donor Hub**: `http://127.0.0.1:8001/dashboard/donneur/`
- **Hospital Hub**: `http://127.0.0.1:8001/dashboard/hopital/`
- **National Overview**: `http://127.0.0.1:8001/dashboard/admin/`

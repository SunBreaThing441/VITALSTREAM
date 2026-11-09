# Full-Stack Integration Workflows

This document illustrates the end-to-end operational workflows connecting user actions in the **Frontend**, processing in the **Backend**, and persistence in the **Database**.

---

## 1. Scenario 1: Hospital Registration & Admin Approval Workflow

A new hospital joins the platform and must be vetted by an administrator before posting urgent requests.

```mermaid
sequenceDiagram
    autonumber
    actor HospUser as Hospital Representative
    participant UI as Browser (Registration Form)
    participant Backend as Django (register_hopital)
    participant DB as SQLite3 (auth_user, index_hopital)
    actor AdminUser as Platform Admin
    participant AdminUI as Admin Dashboard

    HospUser->>UI: Submits registration form (nom, agrement, credentials)
    UI->>Backend: POST /accounts/register/hopital/
    Backend->>Backend: Validate HopitalRegisterForm & Agrement uniqueness
    Backend->>DB: INSERT into auth_user (username, password_hash)
    Backend->>DB: INSERT into index_hopital (user_id, agrement, valide=False)
    Backend-->>UI: 302 Redirect to /dashboard/hopital/
    UI-->>HospUser: Render Dashboard with "En attente de validation admin" warning

    Note over HospUser, AdminUser: Hospital is blocked from creating requests until approved

    AdminUser->>AdminUI: Opens /dashboard/admin/
    AdminUI->>Backend: GET /dashboard/admin/
    Backend->>DB: SELECT * FROM index_hopital WHERE valide=False
    DB-->>Backend: Return unvalidated hospital records
    Backend-->>AdminUI: Render Admin Dashboard with pending facilities
    AdminUser->>AdminUI: Clicks "Valider" button
    AdminUI->>Backend: POST /dashboard/admin/ (hopital_id, action="valider")
    Backend->>DB: UPDATE index_hopital SET valide=True WHERE id=hopital_id
    Backend-->>AdminUI: 302 Redirect with messages.success("Hôpital validé")
    AdminUI-->>AdminUser: Toast notification: "L'hôpital a été validé avec succès"
```

---

## 2. Scenario 2: Urgent Blood Request & Donor Response Workflow

A verified hospital posts a critical shortage of blood bags, and an eligible donor volunteers.

```mermaid
sequenceDiagram
    autonumber
    actor Hosp as Hospital Staff
    participant HospUI as Hospital Dashboard
    participant Backend as Django Server
    participant DB as SQLite3
    actor Donor as Volunteer Donor
    participant DonorUI as Donor Dashboard

    Hosp->>HospUI: Fill urgent request form (e.g. 5 bags of O-, deadline 24h)
    HospUI->>Backend: POST /demande/nouvelle/
    Backend->>Backend: Verify hopital.valide == True
    Backend->>DB: INSERT into index_demandeurgente (hopital_id, groupe_sanguin='O-', quantite=5, statut='Active')
    Backend-->>HospUI: 302 Redirect to /dashboard/hopital/

    Note over Backend, Donor: Emergency is now visible to all active donors

    Donor->>DonorUI: Visits /dashboard/donneur/
    DonorUI->>Backend: GET /dashboard/donneur/
    Backend->>DB: SELECT * FROM index_demandeurgente WHERE statut='Active'
    Backend->>Backend: Check donor.est_eligible() & calculate points/tier
    Backend-->>DonorUI: Render active requests with "Répondre" button
    Donor->>DonorUI: Clicks "Répondre" on urgent request
    DonorUI->>Backend: GET /demande/<id>/repondre/
    Backend->>Backend: Check donor.est_eligible() (Biological cooldown)
    Backend->>DB: Check if ReponseAppel already exists
    alt Already responded
        Backend-->>DonorUI: Warning: "Vous avez déjà répondu à cette demande"
    else First response
        Backend->>DB: INSERT into index_reponseappel (demande_id, donneur_id, statut='En attente')
        Backend->>DB: UPDATE index_donneur SET points = points + 25
        Backend-->>DonorUI: 302 Redirect with messages.success("+25 points 🎉")
        DonorUI-->>Donor: Toast displays: "Intention de don transmise ! +25 points 🎉"
    end
```

---

## 3. Scenario 3: Blood Donation Logging & Tier Promotion Workflow

A donor records a validated blood donation, triggering cooldown recalculations and badge promotions.

```mermaid
sequenceDiagram
    autonumber
    actor Donor as Volunteer Donor
    participant UI as Browser (enregistrer_don.html)
    participant Backend as Django (enregistrer_don)
    participant DB as SQLite3 (index_don, index_donneur)

    Donor->>UI: Submits past donation date & selected hospital
    UI->>Backend: POST /donneur/enregistrer-don/
    Backend->>Backend: Parse date_don (ISO format)
    Backend->>DB: INSERT into index_don (donneur_id, hopital_id, date_don, valide=True)
    Backend->>DB: UPDATE index_donneur SET points = points + 100
    Note over Backend: donneur.prochaine_date_don() now advances by +56d (M) or +84d (F)
    Note over Backend: If points >= 500, tier promotes to "Héros d'Argent"
    Backend-->>UI: 302 Redirect to /dashboard/donneur/
    UI-->>Donor: Display toast "+100 points 🎉" and updated Next Eligible Date
```

---

## 4. Scenario 4: Blood Drive Campaign Booking Workflow

A hospital schedules a collection drive, and an eligible donor reserves a time slot.

```mermaid
sequenceDiagram
    autonumber
    actor Hosp as Hospital Staff
    actor Donor as Volunteer Donor
    participant Backend as Django (Campagne Views)
    participant DB as SQLite3

    Hosp->>Backend: POST /campagne/nouvelle/ (Date, Venue, Groups, Capacity=50)
    Backend->>DB: INSERT into index_campagne
    
    Donor->>Backend: GET /campagnes/
    Backend->>DB: SELECT * FROM index_campagne ORDER BY date
    Backend-->>Donor: Render list of drives with time slot picker
    
    Donor->>Backend: POST /campagne/<id>/inscrire/ (creneau="10:30")
    Backend->>Backend: Validate donor.est_eligible() == True
    Backend->>DB: SELECT COUNT(*) FROM index_inscription WHERE campagne_id=id
    alt Capacity full
        Backend-->>Donor: Error: "Cette campagne est complète"
    else Capacity available
        Backend->>DB: INSERT into index_inscription (campagne_id, donneur_id, creneau_horaire="10:30")
        Backend->>DB: UPDATE index_donneur SET points = points + 50
        Backend-->>Donor: Success: "Inscription confirmée à 10:30. +50 points 🎉"
    end
```

---

## 5. Cross-Tier Interaction Matrix

| User Action | Client-Side Trigger | Server View Function | Database Mutations | Client Response / Viewport Update |
| :--- | :--- | :--- | :--- | :--- |
| **Donor Registration** | Form Submit on `register_donneur.html` | `accounts.views.register_donneur` | `INSERT auth_user`, `INSERT index_donneur` | Auto-login & redirect to Donor Dashboard |
| **Hospital Registration** | Form Submit on `register_hopital.html` | `accounts.views.register_hopital` | `INSERT auth_user`, `INSERT index_hopital` (`valide=False`) | Redirect to Hospital Dashboard with pending alert |
| **Approve Hospital** | "Valider" click on `dashboard_admin.html` | `index.views.dashboard_admin` | `UPDATE index_hopital SET valide=True` | Toast alert, hospital status badge changes to Green |
| **Publish Urgent Need** | Form Submit on `create_demande.html` | `index.views.create_demande` | `INSERT index_demandeurgente` | Request appears on Hospital & Donor Dashboards |
| **Volunteer for Need** | "Répondre" button click | `index.views.repondre_demande` | `INSERT index_reponseappel`, `UPDATE index_donneur (+25 pts)` | Toast notification, button changes to "Répondu" |
| **Close Urgent Need** | "Clôturer" button click | `index.views.close_demande` | `UPDATE index_demandeurgente SET statut='Clôturée'` | Request moves to closed requests section |
| **Log Donation** | Form Submit on `enregistrer_don.html` | `index.views.enregistrer_don` | `INSERT index_don`, `UPDATE index_donneur (+100 pts)` | Cooldown reset (+56/84 days), +100 pts toast |
| **Book Campaign Slot**| Time slot selection & Submit | `index.views.inscrire_campagne`| `INSERT index_inscription`, `UPDATE index_donneur (+50 pts)`| Slot booked confirmation toast, +50 pts badge |
| **Toggle Availability**| Availability switch click | `index.views.toggle_actif` | `UPDATE index_donneur SET actif = NOT actif` | Status badge toggles between Active and Inactive |
| **Export Donor CSV** | "Exporter CSV" button click | `index.views.export_donneurs_csv`| None (Read-only `SELECT`) | Browser initiates file download `donneurs_bloodconnect.csv` |

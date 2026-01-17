# 🔓 Site.pro Backend — Reverse Engineered Schema

**Date:** 2026-01-17  
**Source:** Import template `b1_import-clients-en.xlsx`  
**Discovered by:** Leanid (3 years of research!)

---

## 🎯 Architecture Overview (from screenshots)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LEVEL 1: ACCOUNT (site.pro/My-Accounting/account/dashboard)                │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ ASSET GMBH  │ │ASSET        │ │ RAPSOIL     │ │ YPL INC     │           │
│  │ (frozen)    │ │LOGISTICS    │ │ (frozen)    │ │             │           │
│  │             │ │ 35,72€      │ │             │ │             │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                                             │
│  User: Leanid Kanoplich                                                     │
│  Balance: 35,72€                                                            │
│  Companies: 4 (2 active, 2 frozen)                                          │
│                                                                             │
│  Sidebar: Dashboard | Companies and users | My data | Reminders | Support   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ "Enter Company" (select)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  LEVEL 2: COMPANY (site.pro/My-Accounting/)                                 │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  Shortcuts: [Sales] [Purchases] [Bank] [General ledger reports]       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  Company Dashboard:                                                         │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐            │
│  │ Accounts payable │ │Accounts Receivable│ │ Average leave   │            │
│  │   51,283.30 €    │ │   73,072.50 €    │ │     0.0 d       │            │
│  │ Overdue purchase │ │ Overdue sales    │ │ employees        │            │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘            │
│                                                                             │
│  Sidebar:                                                                   │
│  • Customers ←── THIS IS WHAT WE REVERSE ENGINEERED                        │
│  • Warehouse                                                                │
│  • General ledger                                                           │
│  • Bank                                                                     │
│  • Cashier                                                                  │
│  • Reports                                                                  │
│  • Personnel                                                                │
│  • Reference book                                                           │
│  • Production                                                               │
│  • Assets                                                                   │
│  • Documents                                                                │
│  • Salary                                                                   │
│  • Declaration                                                              │
│  • Analytics                                                                │
│  • Settings → Data import ←── WHERE THE SCHEMA WAS FOUND!                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗃️ Client Model (29 fields)

### Required Fields (3)
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `name` | String | Client name | "UAB B1.lt." |
| `isJuridical` | Boolean | Legal person (0=no, 1=yes) | 1 |
| `location` | Enum | Foreigner status | "lt", "eu", "rest" |

### Basic Info
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `shortName` | String? | Acronym | "B1." |
| `code` | String? | Company code (max 20) | "142130866" |
| `vatCode` | String? | VAT code (max 20) | "LT100000950713" |
| `businessLicenseCode` | String? | Individual business license | — |
| `email` | String? | Email | "info@b1.lt" |
| `phoneNumber` | String? | Phone | "+370 46 210322" |
| `faxNumber` | String? | Fax | — |

### Financial
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `payWithin` | Int? | Payment term (days) | 7 |
| `creditSum` | Decimal? | Credit limit | 99 |
| `automaticDebtRemind` | Boolean? | Auto debt reminder | 1 |

### Registration Address
| Field | Type | Description |
|-------|------|-------------|
| `registrationCountryCode` | String? | Country code (LT) |
| `registrationCity` | String? | City |
| `registrationAddress` | String? | Street address |
| `registrationZipCode` | String? | Postal code |

### Correspondence Address
| Field | Type | Description |
|-------|------|-------------|
| `correspondenceCountryCode` | String? | Country code |
| `correspondenceCity` | String? | City |
| `correspondenceAddress` | String? | Street address |
| `correspondenceZipCode` | String? | Postal code |

### Banking
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `bankAccount` | String? | IBAN | "LT293500010001687408" |
| `bankName` | String? | Bank name | "Paysera LT" |
| `bankCode` | String? | Bank code | "35000" |
| `bankSwiftCode` | String? | SWIFT/BIC | "EVIULT21XXX" |

### Personal (for individuals)
| Field | Type | Description |
|-------|------|-------------|
| `birthday` | DateTime? | Date of birth |
| `residentCode` | String? | Foreign taxpayer ID |

### Other
| Field | Type | Description |
|-------|------|-------------|
| `notes` | String? | Comments |
| `contactInformation` | String? | Contact info |

---

## 🔧 Prisma Schema (Solar Sprint Compatible)

```prisma
// =============================================================================
// CLIENT MODEL — Reverse Engineered from Site.pro
// For use in Solar Sprint multi-tenant architecture
// =============================================================================

enum LocationType {
  LT    // Local (Lithuania)
  EU    // European Union
  REST  // Rest of the world
}

/// Client/Customer - belongs to a Company (Workspace)
/// Full B2B accounting client model
model Client {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // ═══════════════════════════════════════════════════════════════════════════
  // REQUIRED FIELDS
  // ═══════════════════════════════════════════════════════════════════════════
  
  name        String         // Client name (required)
  isJuridical Boolean        // Legal person: true = company, false = individual
  location    LocationType   // lt, eu, rest

  // ═══════════════════════════════════════════════════════════════════════════
  // BASIC INFO
  // ═══════════════════════════════════════════════════════════════════════════
  
  shortName           String?  // Acronym
  code                String?  @db.VarChar(20)  // Company code
  vatCode             String?  @db.VarChar(20)  // VAT code
  businessLicenseCode String?  // Individual business license
  email               String?
  phoneNumber         String?
  faxNumber           String?

  // ═══════════════════════════════════════════════════════════════════════════
  // FINANCIAL
  // ═══════════════════════════════════════════════════════════════════════════
  
  payWithin           Int?      // Payment term in days
  creditSum           Decimal?  @db.Decimal(12, 2)  // Credit limit
  automaticDebtRemind Boolean?  @default(false)

  // ═══════════════════════════════════════════════════════════════════════════
  // REGISTRATION ADDRESS
  // ═══════════════════════════════════════════════════════════════════════════
  
  registrationCountryCode String?
  registrationCity        String?
  registrationAddress     String?
  registrationZipCode     String?

  // ═══════════════════════════════════════════════════════════════════════════
  // CORRESPONDENCE ADDRESS
  // ═══════════════════════════════════════════════════════════════════════════
  
  correspondenceCountryCode String?
  correspondenceCity        String?
  correspondenceAddress     String?
  correspondenceZipCode     String?

  // ═══════════════════════════════════════════════════════════════════════════
  // BANKING
  // ═══════════════════════════════════════════════════════════════════════════
  
  bankAccount   String?  // IBAN
  bankName      String?
  bankCode      String?
  bankSwiftCode String?

  // ═══════════════════════════════════════════════════════════════════════════
  // PERSONAL (for individuals)
  // ═══════════════════════════════════════════════════════════════════════════
  
  birthday     DateTime?
  residentCode String?  // Foreign taxpayer ID

  // ═══════════════════════════════════════════════════════════════════════════
  // OTHER
  // ═══════════════════════════════════════════════════════════════════════════
  
  notes              String?  @db.Text
  contactInformation String?  @db.Text

  // ═══════════════════════════════════════════════════════════════════════════
  // MULTI-TENANT RELATIONS (Solar Sprint Architecture)
  // ═══════════════════════════════════════════════════════════════════════════
  
  // Level 2: Company (Workspace)
  companyId String
  company   Company @relation(fields: [companyId], references: [id], onDelete: Cascade)

  // Level 1: Tenant (for direct queries)
  tenantId String
  tenant   Tenant @relation(fields: [tenantId], references: [id], onDelete: Cascade)

  // Related entities
  invoices Invoice[]  // Client invoices
  
  @@index([companyId])
  @@index([tenantId])
  @@index([email])
  @@index([code])
  @@index([vatCode])
  @@map("clients")
}
```

---

## 📊 Import Template Types Found

From screenshot (Settings → Data Import):

1. **Clients** ← Reverse engineered ✅
2. Items and services balances
3. Item cards
4. Updating product card information
5. r_keeper (POS integration)
6. nSoft (integration)
7. Purchases
8. Sales
9. Import of bank statements
10. Foreign personal income tax deductions

**Each import type = database model schema exposure!**

---

## 🏗️ Site.pro Architecture Mapping → Solar Sprint

| Site.pro Concept | Solar Sprint Equivalent | Layer |
|------------------|------------------------|-------|
| Account | Tenant | Level 1 |
| Company | Workspace / Project | Level 2 |
| User | User | Level 1 |
| Customers | Client | Level 2 entity |
| Invoices | Invoice | Level 2 entity |
| Items | Product / Item | Level 2 entity |
| Warehouse | Inventory | Level 2 entity |
| Bank statements | BankTransaction | Level 2 entity |

---

## 🎯 Key Insights

### 1. Two-Level Architecture Confirmed
- **Level 1 (Tenant)**: Account management, companies list, billing
- **Level 2 (Workspace)**: Business operations, clients, invoices

### 2. URL Structure
```
/My-Accounting/account/dashboard     ← Level 1 (Account)
/My-Accounting/                      ← Level 2 (Company)
/My-Accounting/clients               ← Level 2 entity
/My-Accounting/import/data           ← Schema exposure point!
```

### 3. Company Switcher Pattern
Top-right dropdown allows switching between companies without re-login.
→ Session stores `currentCompanyId`, queries filter by it.

### 4. Frozen Companies
Companies can be "frozen" (archived but not deleted).
→ `status: ACTIVE | FROZEN | ARCHIVED`

---

## ✅ Action Items for Solar Sprint

1. [ ] Add `Client` model to Prisma schema
2. [ ] Create CRUD API for Clients
3. [ ] Implement company switcher in Level 1
4. [ ] Add company status (active/frozen)
5. [ ] Create import/export API for Clients (CSV/Excel)

---

**Document Status:** REVERSE ENGINEERING COMPLETE  
**Next Step:** Implement Client model in Solar Sprint v0.2.0

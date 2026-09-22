# Nexora

Nexora is a modular download manager built with Python and PyQt6.

Version: **1.0.0**

---

## Project Architecture

Nexora follows a layered architecture:

```text
UI
 ↓
Connector
 ↓
Core
 ↓
Database / Engine / Storage
```

### UI

Responsible only for displaying the application interface and collecting user actions.

```text
ui/
├── windows/
├── pages/
├── components/
├── widgets/
├── dialogs/
└── menus/
```

### Connector

Responsible for connecting the UI with the Core layer.

```text
connector/
├── controller_manager/
├── url_controller/
├── download_controller/
├── queue_controller/
├── schedule_controller/
├── history_controller/
├── settings_controller/
└── account_controller/
```

### Core

Contains the application's actual business logic.

```text
core/
├── database/
├── downloads/
├── file/
├── storage/
├── accounts/
├── queue/
├── speed/
├── history/
├── settings/
├── aria2_engine/
└── schedule/
```

---

# v1.0.0 Development Roadmap

Development will be completed step by step.

## Step 01 — Project Structure

Status: **Completed**

* [x] Create project root
* [x] Create config
* [x] Create resources
* [x] Create aria2
* [x] Create ui
* [x] Create conne
* [x] Create core
* [x] Create utils
* [x] Create tests
* [x] Create data

---

## Step 02 — Configuration

Directory:

```text
config/
├── app_paths.py
├── app_constants.py
├── app_config.py
└── app_config_manager.py
```

Tasks:

* [ ] Application paths
* [ ] Application constants
* [ ] Application configuration
* [ ] Configuration manager
* [ ] Runtime directories
* [ ] Resource paths
* [ ] aria2 path
* [ ] Database path

---

## Step 03 — Database

Directory:

```text
core/database/
├── connection.py
├── db_manager.py
├── schema.py
└── repositories/
```

Tasks:

* [ ] Database connection
* [ ] Database initialization
* [ ] Schema
* [ ] Repository base
* [ ] Account repository
* [ ] Drive repository
* [ ] Download repository
* [ ] Queue repository
* [ ] History repository
* [ ] Settings repository

---

## Step 04 — File System

Directory:

```text
core/file/
├── file_info_manager.py
└── file_resolver.py
```

Tasks:

* [ ] File information
* [ ] File name resolution
* [ ] File size
* [ ] File type
* [ ] URL/file resolution

---

## Step 05 — Storage

Directory:

```text
core/storage/
└── storage_manager.py
```

Tasks:

* [ ] Download location
* [ ] Temporary location
* [ ] File path handling
* [ ] Disk space checking

---

## Step 06 — Aria2 Engine

Directory:

```text
aria2/
└── aria2c.exe

core/aria2_engine/
└── aria2_engine.py
```

Tasks:

* [ ] Start aria2
* [ ] Connect to RPC
* [ ] Add download
* [ ] Pause
* [ ] Resume
* [ ] Stop
* [ ] Remove
* [ ] Progress
* [ ] Speed
* [ ] Download status
* [ ] Error handling

---

## Step 07 — Download System

Directory:

```text
core/downloads/
├── download_manager.py
└── download_worker.py
```

Tasks:

* [ ] Create download
* [ ] Start download
* [ ] Pause download
* [ ] Resume download
* [ ] Stop download
* [ ] Delete download
* [ ] Download progress
* [ ] Download completion
* [ ] Download failure

---

## Step 08 — Queue System

Directory:

```text
core/queue/
├── queue_manager.py
└── queue_worker.py
```

Tasks:

* [ ] Create queue
* [ ] Add item
* [ ] Remove item
* [ ] Queue ordering
* [ ] Start next item
* [ ] Pause queue
* [ ] Resume queue
* [ ] Stop queue

---

## Step 09 — Speed System

Directory:

```text
core/speed/
└── speed_manager.py
```

Tasks:

* [ ] Current speed
* [ ] Average speed
* [ ] Total speed
* [ ] Speed limit support

---

## Step 10 — Account System

Directory:

```text
core/accounts/
├── account_manager.py
└── auth_manager.py
```

Tasks
* [ ] Account management
* [ ] Login
* [ ] Logout
* [ ] Token management
* [ ] Account information

Cloud providers can be added later without changing the UI architecture.

---

## Step 11 — History

Directory:

```text
core/history/
└── history_manager.py
```

Tasks:

* [ ] Save download history
* [ ] Read history
* [ ] Delete history
* [ ] Clear history
* [ ] History status

---

## Step 12 — Settings

Directory:

```text
core/settings/
└── settings_manager.py
```

Tasks:

* [ ] Read settings
* [ ] Save settings
* [ ] Download settings
* [ ] Connection settings
* [ ] UI settings

---

## Step 13 — Schedule

Directory:

```text
core/schedule/
└── schedule_manager.py
```

Tasks:

* [ ] Create schedule
* [ ] Edit schedule
* [ ] Delete schedule
* [ ] Enable/disable schedule
* [ ] Start scheduled download

---

## Step 14 — UI

Directory:

```text
ui/
├── windows/
├── pages/
├── components/
├── widgets/
├── dialogs/
└── menus/
```

Tasks:

* [ ] Main Window
* [ ] Menu Bar
* [ ] Toolbar
* [ ] Dashboard
* [ ] Download Page
* [ ] Schedule Page
* [ ] History Page
* [ ] Settings Page
* [ ] Download Item Widget
* [ ] Add URL Dialog
* [ ] Direct Download Dialog
* [ ] Login Dialog
* [ ] About Dialog
* [ ] Status Bar

---

## Step 15 — Controllers

Directory:

```text
connector/
├── controller_manager/
├── url_controller/
├── download_controller/
├── queue_controller/
├── schedule_controller/
├── history_controller/
├── settings_controller/
└── account_controller/
```

Tasks:

* [ ] Controller Manager
* [ ] URL Controller
* [ ] Download Controller
* [ ] Queue Controller
* [ ] Schedule Controller
* [ ] History Controller
* [ ] Settings Controller
* [ ] Account Controller

---

## Step 16 — Integration

Connect all layers:

```text
MainWindow
    ↓
ControllerManager
    ↓
Controllers
    ↓
Core Managers
    ↓
Repositories / Engine / Workers
```

Tasks:

* [ ] UI → Controller
* [ ] Controller → Core
* [ ] Core → Database
* [ ] Core → Aria2
* [ ] Core → Storage
* [ ] Core → UI signals

---

## Step 17 — Testing

Directory:

```text
tests/
```

Tasks:

* [ ] Configuration tests
* [ ] Database tests
* [ ] File tests
* [ ] Storage tests
* [ ] Aria2 tests
* [ ] Download tests
* [ ] Queue tests
* [ ] Account tests
* [ ] Controller tests
* [ ] UI integration tests

---

## Step 18 — Error Handling & Logging

Directory:

```text
data/
└── logs/
```

Tasks:

* [ ] Application errors
* [ ] Download errors
* [ ] Database errors
* [ ] Aria2 errors
* [ ] Logging
* [ ] User-friendly error messages

---

## Step 19 — Final Integration Test

Test the complete flow:

```text
Add URL
   ↓
Analyze URL
   ↓
Get File Information
   ↓
Check Storage
   ↓
Create Database Record
   ↓
Add Queue
   ↓
Start Aria2
   ↓
Download
   ↓
Update Progress
   ↓
Complete
   ↓
Save History
```

---

## Step 20 — Build

Final tasks:

* [ ] PyInstaller configuration
* [ ] Include resources
* [ ] Include aria2
* [ ] Include required files
* [ ] Test EXE
* [ ] Test clean installation
* [ ] Version 1.0.0 release

---

# Development Rules

1. Do not mix UI logic with Core logic.
2. UI must not directly access the database.
3. UI must not directly control aria2.
4. Controllers connect UI and Core.
5. Core contains business logic.
6. Database repositories handle database operations.
7. Managers handle application logic.
8. Workers handle long-running/background operations.
9. Do not create unnecessary files before they are needed.
10. Complete and test one step before moving to the next step.
11. Existing prototype code is not considered final until it passes the new architecture.
12. Avoid changing the finalized root architecture without a specific reason.

---

# Version

```text
Nexora v1.0.0
```

Development approach:

```text
Structure
   ↓
Configuration
   ↓
Database
   ↓
Core
   ↓
Engine
   ↓
UI
   ↓
Controllers
   ↓
Integration
   ↓
Testing
   ↓
Build
   ↓
Nexora v1.0.0
```
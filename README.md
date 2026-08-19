# Splash Finance Tracker

Splash is a desktop-based Personal Finance Tracker application built with Python, utilizing `CustomTkinter` for the GUI, `Pandas`/`Matplotlib` for data analysis, and `SQLite` for persistent storage.

## Display 
<div align="center">

![Splash-GUI demo](data/Display.jpeg)

</div>

## Architecture Overview
The application follows a modular structure separating UI concerns from data processing and database operations.

```mermaid
graph TD
    User[User Interaction] --> UI[CustomTkinter GUI]
    UI --> Logic[Finance Tracker Logic]
    Logic --> DataProcessing[Pandas / Matplotlib]
    Logic --> DB[(SQLite Database)]
    DataProcessing --> UI
```

---
Based on the project structure of `finance-tracker-gui`, here is a suggested `README.md` structure. Since this is a desktop application using `CustomTkinter` and `SQLite`, the architecture focuses on the separation between the UI layer, the logic/data layer, and the persistent storage.

```mermaid
classDiagram
    class App {
        +MainApplication root
        +setup_ui()
        +run()
    }
    class DatabaseManager {
        +sqlite3 connection
        +execute_query()
        +fetch_transactions()
        +save_transaction()
    }
    class FinanceTracker {
        +add_income()
        +add_expense()
        +get_report()
    }
    class DataVisualizer {
        +Matplotlib figure
        +render_charts()
    }
    class UI_Components {
        +CustomTkinter widgets
        +update_dashboard()
    }

    App *-- FinanceTracker : manages
    FinanceTracker o-- DatabaseManager : persists
    FinanceTracker o-- DataVisualizer : visualizes
    App o-- UI_Components : renders
```

## Features
- **Transaction Management:** Add, view, and manage income and expense logs.
- **Visual Analytics:** Interactive charts and graphs powered by Matplotlib.
- **Persistent Storage:** Local SQLite database ensures data remains saved between sessions.
- **Easy Reset:** Manual transaction database reset capability.

## Technical Stack
- **Language:** Python
- **GUI Framework:** CustomTkinter
- **Data Handling:** Pandas
- **Visualization:** Matplotlib
- **Database:** SQLite

---
*Note: This project is currently on a indefinite hiatus phase. Features such as login authorization are planned for future updates.*
```

## NISER tracker local database

## Description
This project is a database management system designed for CMS Outer Tracker Module Assembly for processing and visualization of data. It uses Flask for the front-end, PostgreSQL/SQLite3 for the relational database management, and includes a variety of tools for managing workflows, forms, and visual inspections.


## Project Structure
```
.
├── DATABASE
│   ├── README.md
│   └── nisers.db
├── Static
│   ├── assets
│   ├── uploads
│   └── WORKFLOW_FILES
├── Templates
│   ├── add_station_form.html
│   ├── all_stations.html
│   ├── base.html
│   ├── dynamic_form.html
│   ├── home.html
│   ├── index.html
│   ├── login.html
│   ├── material_reciever.html
│   ├── material_type.html
│   ├── module_report.html
│   ├── modules.html
│   ├── visual_inspection.html
│   ├── wire_bonding.html
│   └── workflow.html
├── Utilities
│   └── add_user.py

├── database_table.py
├── forms.py
├── main.py
├── noise_test_plot_maker.
├── noise_test.py
├── process_data.py
├── save_form_database.py
├── requirements.txt
├── README.md
```

---

## Installation
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd module_production_db
   ```

3. **Set Up the Virtual Environment:**
   ```bash
   ''add script for setting virtual env''  
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```bash
   python main.py
   ```

---

## Usage
- Access the application via the local server (http://127.0.0.1:9999).
- Use the login page to authenticate.
- Navigate through different modules to manage workflows, inspect materials, or view reports.

---

## Dependencies
- **Python**: 3.10+
- **Flask**: For the web framework
- **SQLAlchemy**: For database interaction
- **WTForms**: For form handling
- **Matplotlib**: For visualization

For more, refer to `requirements.txt`.

---

## Key Modules and Scripts
- **`main.py`**: The entry point of the application.
- **`database_table.py`**: Handles database interactions.
- **`forms.py`**: Defines forms for the Flask application.
- **`noise_test.py`**: Noise testing and analysis script.
- **`save_form_database.py`**: Save form data into the database.
- **`process_data.py`**: Data processing utility.

---

## Contribution
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## Contact



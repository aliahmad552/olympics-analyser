# 🏅 Olympics Analysis Web App

This project is a Streamlit-based interactive web application that allows users to explore **128 years of Olympic history** (1896–2024) using data analysis and visualizations.

---

## 📌 Features

- 📊 **Medal Tally** – View total medals by country and year.
- 🌍 **Overall Analysis** – Explore trends in:
  - Participating Nations
  - Number of Events
  - Athlete Participation
  - Gender Split over the years
- 🏳️ **Country-wise Analysis** *(to be implemented)* – Explore performance of individual countries.
- 🧍 **Athlete-wise Analysis** *(to be implemented)* – Discover top athletes and their stats.

---

## 🗂 Dataset

The app uses a cleaned and merged dataset:
- `athlete_events.csv` – Olympic athlete records
- `noc_regions.csv` – Mapping of National Olympic Committees to countries

---

## 🚀 How to Run

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/olympics-analysis-app.git
   cd olympics-analysis-app
2. **Install dependencies**:

```bash
Copy
Edit
pip install -r requirements.txt

3. **Run the Streamlit app**:

```bash
Copy
Edit
streamlit run app.py

## 🛠️ File Structure
graphql
Copy
Edit
-├── app.py                # Main Streamlit app
-├── helper.py             # Helper functions for data processing
-├── preprocessor.py       # Data cleaning and merging
-├── athlete_events.csv    # Olympic athlete data
-├── noc_regions.csv       # NOC to region mapping
-└── README.md             # Project documentation

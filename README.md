# 📊 IIHR Research Performance Dashboard

An interactive dashboard to analyze and evaluate the research performance of scientists at the **Indian Institute of Hydrology Research (IIHR)** using **Google Scholar metrics**.

The system combines automated Scholar data extraction, human-in-the-loop updates, and normalized performance scoring to support institutional research assessment.

---

## 🔍 Features

- Automatic extraction of **h-index** and **total citations** from Google Scholar
- User input option for missing or incorrect Scholar profile links
- Composite **Research Performance Score** using normalized metrics
- Identification of top-performing scientists
- Data quality and coverage reporting
- Exportable results (CSV)

---

## 🧮 Performance Score Formula
Performance Score =
0.6 × normalized citations +
0.4 × normalized h-index

---

## 🛠️ Tech Stack

- Python 3.11
- Streamlit
- Pandas, NumPy
- Altair
- Scholarly (Google Scholar scraping)

---

## 🚀 Deployment

The dashboard is deployed on **Streamlit Cloud** and accessible via a web browser.

---

## ⚠️ Note

Due to the absence of an official Google Scholar API, the system uses a **semi-automated and ethical data update approach**.

---


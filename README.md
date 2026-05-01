# Gluten-Free Restaurant Finder

**Live App:** https://tu-app.streamlit.app

Find safe gluten-free restaurants in Melbourne using real customer reviews and machine learning.

---

## Overview

This application helps users identify gluten-free friendly restaurants in Melbourne by:

- Analyzing customer reviews
- Estimating a safety score for each restaurant
- Displaying results on an interactive map
- Showing distance from the user’s location
- Highlighting gluten-related mentions in reviews
- Displaying restaurant images

---

## Application Preview

### Map view

![Map](assets/image1.JPG)

### Restaurant details

![Details](assets/image2.jpg)

---

## How to run

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

---

## Technology Stack

- Python
- Streamlit
- Pandas
- Folium
- Scikit-learn (text analysis)

---

## Project Structure

```text
.
├── app/
│   └── streamlit_app.py
├── assets/
│   ├── image1.JPG
│   ├── image2.jpg
│   └── skyline.png
├── data/
│   ├── raw/
│   │   ├── raw_data.csv
│   │   └── imagenes.csv
│   └── processed/
│       ├── clean_data.csv
│       └── restaurant_ranking.csv
├── notebooks/
│   └── celiac_restaurant_analysis.ipynb
├── src/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Data

The dataset includes restaurant information, customer reviews, and image references.
Data is split into:

- **raw/**: original datasets
- **processed/**: cleaned and enriched data used in the app

---

## Features

- Interactive map with restaurant locations
- Gluten safety scoring based on reviews
- Keyword highlighting in reviews
- Restaurant filtering (category, price)
- Image display for each location

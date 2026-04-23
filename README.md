# Gluten-Free Restaurant Finder

Machine learning project to identify gluten-free safe restaurants from customer reviews and visualize them on an interactive map.

---

## Overview

This application helps users find gluten-free friendly restaurants in Melbourne by:

* Analyzing customer reviews
* Estimating a safety score for each restaurant
* Displaying results on an interactive map
* Showing distance from the user’s location
* Highlighting gluten-related mentions in reviews
* Displaying restaurant images

---

## Application Preview

### Map view

![Map](assets/map.png)

### Restaurant details

![Details](assets/details.png)

### Filters and search

![Filters](assets/filters.png)

---

## Demo

(Add your Streamlit Cloud link here)

---

## Technology Stack

* Python
* Streamlit
* Pandas
* Folium
* Machine Learning

---

## Project Structure

```
.
├── App/
│   └── app.py
├── data/
│   ├── restaurant_ranking.csv
│   ├── clean_data.csv
│   ├── raw_data.csv
│   └── imagenes.csv
├── assets/
│   ├── skyline.png
│   ├── map.png
│   ├── details.png
│   └── filters.png
├── Notebooks/
│   └── Celiac_Restaurant_Analysis.ipynb
├── requirements.txt
└── README.md
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run App/app.py
```

---

## Methodology

* Reviews are processed to identify gluten-related content
* A model assigns a safety score to each restaurant
* Data is combined with geographic coordinates
* Results are visualized through an interactive map

---

## Features

* Search by restaurant name
* Filter by category
* Filter by price
* Geolocation support
* Route calculation
* Review analysis
* Image visualization

---

## Notes

* This project is intended for educational purposes
* Data accuracy is not guaranteed
* No API keys are required to run the application

---

## Author

Lucía Terres

---

## License

This project is for academic and demonstration purposes.

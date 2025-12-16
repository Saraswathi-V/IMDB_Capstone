# IMDb Big Data Dashboard

A **Big Data analytics dashboard** for IMDb datasets using **MongoDB**, **Streamlit**, and optional visualizations via **Power BI** or **Tableau**. This project demonstrates data ingestion, transformation, and interactive visualization for large-scale movie datasets.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Features](#features)  
- [Data Sources](#data-sources)  
- [Architecture](#architecture)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Power BI / Tableau Integration](#power-bi--tableau-integration)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Project Overview

This project ingests large IMDb datasets into **MongoDB**, processes the data using **Python**, and creates interactive dashboards with **Streamlit**. Users can explore movie trends, ratings, genres, and more through aggregated visualizations.

---

## Features

- Load IMDb datasets into MongoDB  
- Clean and aggregate large-scale data  
- Interactive dashboards with Streamlit  
- Filter by genres, year, ratings, and more  
- Optional integration with Power BI or Tableau for advanced visualizations  

---

## Data Sources

- [IMDb Title Basics](https://datasets.imdbws.com/title.basics.tsv.gz)  
- [IMDb Title Ratings](https://datasets.imdbws.com/title.ratings.tsv.gz)  
- [Additional IMDb datasets](https://datasets.imdbws.com/)  

> Note: Ensure the datasets are downloaded and placed in the `data/` folder.

---

## Architecture

[IMDb TSV/GZ Files] --> [MongoDB] --> [Python ETL Scripts] --> [Streamlit Dashboard]

--> [Power BI/Tableau Visualizations]


---

## Installation

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/imdb-bigdata-dashboard.git
cd imdb-bigdata-dashboard
---
### Create a virtual environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


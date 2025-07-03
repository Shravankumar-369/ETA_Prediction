# ETA_Prediction

A machine learning-powered web application that predicts Estimated Time of Arrival (ETA) for rides across Bengaluru city. The model is trained on real-world travel data including distance, time of day, day of week, and traffic conditions. Built with **XGBoost**, **Streamlit**, and **OpenRouteService API**.

![App Banner](https://i.postimg.cc/YSCMXh5r/bengaluru-banner.png)

---

##  Features

- Predicts ETA based on:
  - Pickup & Drop locations
  - Day of the week
  - Hour of the day (24-hour format)
-  Uses an XGBoost regression model with optimized hyperparameters
-  Uses OpenRouteService + Geopy for geolocation & distance calculation
-  Includes traffic level awareness (low/medium/high)
-  Clean UI powered by Streamlit

---

##  Technologies Used

| Tool / Library | Purpose |
|----------------|---------|
| `Streamlit` | Frontend UI |
| `XGBoost` | Machine Learning model |
| `pandas`, `numpy` | Data processing |
| `sklearn` | ML pipeline and metrics |
| `geopy` | Geocoding addresses |
| `openrouteservice` | Calculating driving distance in km |

---

How It Works
1. User inputs pickup and drop-off locations

2. System uses OpenRouteService API to compute the driving distance

3. Extracts hour of day and day of week, categorizes traffic level

4. ML model (XGBoost) predicts ETA in minutes

5. Results are displayed with distance and ETA

---
## Author

Shravan Kumar Gogi

# O-MyGot AI IoT for BSF Farming Assistant

## Overview

**O-MyGot** is a comprehensive tool designed to optimize Maggot or Black Soldier Fly (BSF) production through AI and IoT. Our application provides features for automated larvae counting using computer vision, harvest predictions, and environmental monitoring.

## Team
| Name | Role | Github-Profile |
| :---: | :---: | :---: |
| Ali Astra Mikail | AI/ML & IoT Engineer | [@aliastrm](https://github.com/aliastrm) |
| Indri Windriasari | AI/ML Engineer & Project Manager | [@driins](https://github.com/driins) |
| Ginanjar Aditya P | Backend Engineer | [@kudith](https://github.com/kudith) |
| Prayoga Setiawan | Hardware & Mechanical Engineer |  |

## Features

### 1. *Environmental Monitoring*
- Monitor historical temperature and humidity data from maggot environment.
- Visualize average temperature and humidity with charts.

### 2. *Maggot Counting*
- Upload images of larvae and get an automatic count using our computer vision model.
- Supports ESP32 Cam capture image using button capture on streamlit

### 2. *Harvest Prediction*
- Predict the number of days until BSF larvae are ready for harvest based on environmental and feeding conditions.
- Input parameters include temperature, humidity, feed quantity, and larvae growth rate.

### 4. *Help and Support*
- Access FAQs and contact support for personalized assistance.
- Submit feedback directly through the app.

## Installation

### Prerequisites

- Python 3.9
- MongoDB
- YOLOv9 (for computer vision)
- Required Python libraries: numpy, pandas, pickle, pymongo, streamlit, tensorflow, Pillow

### Setup Instructions

1. *Clone the Repository*

   git clone https://github.com/O-MyGot/O-MyGot-apps.git
   
2. *Install Dependencies*

   Create a virtual environment (optional but recommended):

   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   
   Install the required libraries:

   pip install -r requirements.txt
   
3. *Prepare the Environment*
   - Ensure ESP32, ESP32 Cam, and MongoDB is installed and running.

4. *Run the Application*

   streamlit run app.py
   

## Usage

1. *Accessing the App*

   Open a web browser and navigate to http://localhost:8501 to interact with the O-MyGot BSF Farming Assistant.

2. *Navigating the App*

   - *Home*: Overview and project details.
   - *Prediction*: Input data to predict harvest timing.
   - *Maggot Counting*: Capture image from ESP32 Cam to count maggot larvae.
   - *Monitoring*: View and analyze historical environmental data.
   - *Help & Feedback*: Get support and FAQs and submit your suggestions and comments.


## Contact

For questions or support, please contact:

- *GitHub Repository*: [O-MyGot](https://github.com/O-MyGot/O-MyGot-apps)

## Acknowledgements

- *Providers*: Thanks to the contributors of this project.
- *Libraries*: Streamlit, TensorFlow, Pillow, and other Python libraries used.

---

### Additional Notes

1. *Requirements File*: Ensure you create a requirements.txt file listing all Python dependencies, e.g., numpy, pandas, pymongo, streamlit, tensorflow, Pillow.

2. *App Description*: Modify the project description and instructions to match any changes or additional features in your app.

3. *Licenses*: Include any additional license information if you use or modify third-party libraries.

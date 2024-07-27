import streamlit as st
import numpy as np
import pickle
from PIL import Image
import urllib.request
import cv2
import pymongo
import pandas as pd
import time

# Load the models and scalers
with open('harvest_prediction_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Function to fetch data from MongoDB
def fetch_data():
    client = pymongo.MongoClient("mongodb://ohmaigot:22omgpro@ac-x32m9gw-shard-00-00.kfniqpk.mongodb.net:27017,ac-x32m9gw-shard-00-01.kfniqpk.mongodb.net:27017,ac-x32m9gw-shard-00-02.kfniqpk.mongodb.net:27017/?ssl=true&replicaSet=atlas-13lmid-shard-0&authSource=admin&retryWrites=true&w=majority&appName=ohmaigot-cluster")
    db = client['IoTDatabase']
    collection = db['Sensor']
    data = list(collection.find())
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Function to set query parameters
def set_query_params(**kwargs):
    st.experimental_set_query_params(**kwargs)

# Get query parameters
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Home"])[0]

# Sidebar for navigation
st.sidebar.title("O-MyGot!")
page = st.sidebar.radio(
    "Here's what you can do:",
    ["Home", "Prediction", "Maggot Counting", "Monitoring", "Help & Support"],
    index=["Home", "Prediction", "Maggot Counting", "Monitoring", "Help & Support"].index(page)
)

# Update query parameters based on sidebar selection
set_query_params(page=page)

# Home Page
if page == "Home":
    st.title('O-MyGot! - **Your Maggot (BSF Larvae) Farming Assistant!**')
    st.write("""
    ## About This Project

    Welcome to your go-to assistant for Maggot (Black Soldier Fly Larvae)  farming! Our application is designed to make your life easier by providing valuable insights and tools to optimize your BSF production. Here's what you can do:

    ### 1. **Harvest Prediction**
    Want to know when your BSF larvae will be ready for harvest? Simply enter the current conditions:
    - **Temperature (°C)**
    - **Humidity (%)**
    - **Feed Quantity (kg)**
    - **Larvae Growth Rate (g/day)**

    We’ll predict how many days it will take until your larvae are ready for harvest!

    ### 2. **Maggot Counting**
    Struggling to count maggots? Make it a breeze with our maggot counting feature and let our model handle the counting.

    ### 3. **Environmental Monitoring**
    Stay on top of your environmental conditions. We fetch data from your MongoDB database and show you the latest trends in temperature and humidity.

    Our app uses the latest technology to support your farming needs and help you get the best results from your BSF larvae.
    """)

# Prediction Page
elif page == "Prediction":
    st.title('Predict Your BSF Harvest Date')

    st.write("""
    Fill in the details below to get an estimate of how many days it will take until your BSF larvae are ready for harvest:
    """)

    # Create input fields for user
    temperature = st.number_input('Temperature (°C)', min_value=0, max_value=50, value=28)
    humidity = st.number_input('Humidity (%)', min_value=0, max_value=100, value=65)
    feed_quantity = st.number_input('Feed Quantity (kg)', min_value=0, max_value=100, value=50)
    larvae_growth_rate = st.number_input('Larvae Growth Rate (g/day)', min_value=0.0, max_value=1.0, value=0.4)

    # Prepare the input data for the model
    input_data = np.array([[temperature, humidity, feed_quantity, larvae_growth_rate]])
    input_data_scaled = scaler.transform(input_data)  # Scale the input data
    
    st.write("""Hit the **Predict** button below and get an accurate estimate of the days until harvest. It's that simple!""")

    # Make predictions
    if st.button('Predict'):
        prediction = model.predict(input_data_scaled)
        st.write(f'Predicted Days to Harvest: {prediction[0]:.2f} days')

# Maggot Counting Page
elif page == "Maggot Counting":
    st.title('Count Your Maggot with Ease')

    st.write("""
    Struggling to count maggots? 
    
    Make it a breeze with these simple steps! 

    1. Click on **Capture and Count** button.
    2. Our model will process the image and give you the count of Maggot.

    It's quick and easy, let the magic happen!
    """)

    url = 'http://192.168.18.54/cam-hi.jpg'
    st.write("Live stream from ESP32-CAM at: [Stream](http://192.168.18.54/cam-hi.jpg)")

    def get_frame():
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
        return img

    if st.button('Capture and Count'):
        frame = get_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(cv2.GaussianBlur(gray, (11, 11), 0), 30, 150, 3)
        dilated = cv2.dilate(canny, (1, 1), iterations=2)
        (cnt, _) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(frame, cnt, -1, (0, 255, 0), 2)
        st.image(frame, caption=f'Captured Image with {len(cnt)} Maggot', use_column_width=True)
        st.write(f'Number of Maggot: {len(cnt)}')

    else:
        frame = get_frame()
        st.image(frame, caption='Live Transmission', use_column_width=True)

# Monitoring Page
elif page == "Monitoring":
    st.title('Track Your Environmental Conditions')

    st.write("""
    Here's what you can see:
    """)

    # Fetch data from MongoDB
    data = fetch_data()

    # Display average temperature and humidity
    avg_temp = data['temperature'].mean()
    avg_humidity = data['humidity'].mean()

    # Layout for average values
    st.markdown("""
    <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 20px;">
        <div style="text-align: center;">
            <img src="https://img.icons8.com/ios/50/temperature.png" alt="Temperature Icon"/>
            <h3>Average Temperature</h3>
            <p style="font-size: 24px; color: #ff6347;">{:.2f} °C</p>
        </div>
        <div style="text-align: center;">
            <img src="https://img.icons8.com/ios/50/humidity.png" alt="Humidity Icon"/>
            <h3>Average Humidity</h3>
            <p style="font-size: 24px; color: #4682b4;">{:.2f} %</p>
        </div>
    </div>
    """.format(avg_temp, avg_humidity), unsafe_allow_html=True)

    st.write("""
    ### **Historical Data**
    View the historical trends of temperature and humidity over time with our easy-to-read line chart. It helps you spot patterns and make informed decisions.
    """)

    # Display historical data
    st.line_chart(data.set_index('timestamp')[['temperature', 'humidity']])

    st.write("""
    Stay informed about your farming conditions to ensure the best environment for your BSF larvae. It's all here in one place!
    """)

elif page == "Help & Support":
    st.title('Help & Support')
    st.write("""
    ## Need Assistance?

    If you have any questions or need help with using the app, you're in the right place. Here’s how you can get support:

    ### **Frequently Asked Questions**
    - **How do I use the prediction feature?**
    - **How can I to use maggot counting?**
    - **Where does the environmental data come from?**

    ### **Contact Support**
    If you need personalized help, please contact us:
    - **Email**: support@bsffarmapp.com
    - **Phone**: +1-234-567-8901

    We're here to help you get the most out of our app and support your BSF farming needs.
    """)

    st.title('We Value Your Feedback')
    st.write("""
    ## Share Your Thoughts

    Your feedback helps us improve the app and better serve your needs. Please let us know what you think:

    - **What features do you like?**
    - **What improvements would you suggest?**
    - **Any issues you encountered?**

    ### **Leave Your Feedback Below**
    """)

    feedback = st.text_area("Your feedback:")
    if st.button('Submit Feedback'):
        st.write("Thank you for your feedback!")

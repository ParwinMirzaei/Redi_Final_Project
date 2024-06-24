import sys
import random
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # API key for accessing the weather service
        self.api_key = 'ec0fdd298254fb963e76fbbb35bc51a4'
        
        # Read fun facts from a text file
        self.facts = self.read_fun_facts('funfacts.txt')
        
        # Set up the GUI
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle('Weather App')
        self.setGeometry(300, 250, 700, 600)
        self.setStyleSheet("background-color: #809ea1;")  # Sky blue background

        # Layout
        self.layout = QVBoxLayout()

        # Location input
        self.location_label = QLabel('Enter Location:')
        self.location_label.setStyleSheet("font-family: 'Times New Roman'; font-size: 30px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.location_label)

        self.location_input = QLineEdit(self)
        self.location_input.setStyleSheet("font-family: 'Times New Roman';font-size: 26px; padding: 18px; background-color: #F0FFF0;")  # Light green background
        self.layout.addWidget(self.location_input)
        self.location_input.returnPressed.connect(self.fetch_weather)  # Connect Enter key to fetch_weather

        # Fetch weather button
        self.fetch_button = QPushButton('Get Weather', self)
        self.fetch_button.setStyleSheet("font-family: 'Times New Roman'; background-color: #2b8b7f; color: white; font-size: 22px; font-weight: bold; padding: 10px;")  # Cerulean button
        self.fetch_button.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.fetch_button)

        # Weather icon display
        self.icon_label = QLabel(self)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.icon_label)

        # Weather result display
        self.result_display = QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("font-family: 'Times New Roman';font-size: 24px; padding: 16px; background-color: #F0FFF0;")  # Light green background
        self.layout.addWidget(self.result_display)

        # Fun fact display
        self.fun_fact_label = QLabel(self)
        self.fun_fact_label.setAlignment(Qt.AlignCenter)
        self.fun_fact_label.setWordWrap(True)
        self.fun_fact_label.setStyleSheet("font-family: 'Times New Roman';font-size: 20px; padding: 16px; background-color: #F0FFF0; color: #333;")  # Light green background
        self.layout.addWidget(self.fun_fact_label)
        
        # Set layout
        self.setLayout(self.layout)

    def read_fun_facts(self, filename):
        """Reads fun facts from a text file and returns a list of facts."""
        # Get the absolute path of the file
        file_path = os.path.join(os.path.dirname(__file__), filename)
        
        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"Error: Could not find the file {file_path}")
            return ["Could not find the fun facts file!"]

        # Read lines from the file and strip newline characters
        try:
            with open(file_path, 'r') as file:
                facts = [line.strip() for line in file.readlines()]
            return facts
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ["Error reading the fun facts file!"]

    def fetch_weather(self):
        # Get the location from the input field
        location = self.location_input.text()
        # Fetch weather data from the API
        result = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={self.api_key}')
        
        # Check for valid response
        if result.status_code != 200 or result.json().get('cod') == '404':
            self.result_display.setText("Invalid location. Please check the location spelling!")
            self.icon_label.clear()
            self.fun_fact_label.clear()
            return
        
        # Parse weather data
        data = result.json()
        description = data['weather'][0]['description']
        temperature = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        high = round(data['main']['temp_max'])
        low = round(data['main']['temp_min'])

        # Construct the weather information string
        weather_info = (
            f"The weather in {location.title()} now is <b><span style='color:red;'>{temperature}° C</span></b> with {description}.<br><br>"
            f"It feels like {feels_like}° C.<br><br>"
            f"Today's high is {high}° C and today's low is {low}° C.<br><br>"
        )

        advice = ""
        
        # Set the icon and advice based on the weather description
        icon_directory = "C:/Users/nkogh/ReDI_Project/Redi_Final_Project/"
        if 'rain' in description:
            advice += "Take an umbrella with you.<br><br>"
            icon_path = icon_directory + 'rain.png'
        elif 'clear' in description:
            advice += "Put on sunglasses.<br><br>"
            icon_path = icon_directory + 'sun.png'
        elif 'cloud' in description:
            advice += "It might be a bit gloomy.<br><br>"
            icon_path = icon_directory + 'cloud.png'
        elif 'snow' in description:
            advice += "Wear warm clothes.<br><br>"
            icon_path = icon_directory + 'snow.png'
        elif 'thunderstorm' in description:
            advice += "Stay indoors if possible.<br><br>"
            icon_path = icon_directory + 'thunderstorm.png'
        else:
            advice = "Check the weather carefully."
            icon_path = ""

        # Set the weather icon
        if icon_path:
            pixmap = QPixmap(icon_path).scaled(50, 50, Qt.KeepAspectRatio)
            self.icon_label.setPixmap(pixmap)
        else:
            self.icon_label.clear()

        # Display the weather information and advice
        self.result_display.setHtml(weather_info + advice)
        # Display a random fun fact
        self.display_random_fact()

    def display_random_fact(self):
        # Select a random fun fact
        random_fact = random.choice(self.facts)
        # Display the fun fact
        self.fun_fact_label.setText(f"<h3 style='font-size: 24px; color: #2b8b7f;'>Fun Fact:</h3> <p style='font-size: 20px;'>{random_fact}</p>")

# Main function to run the app
def main():
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

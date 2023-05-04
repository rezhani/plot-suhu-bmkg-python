import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

# Mendapatkan data XML dari URL
url = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KalimantanTimur.xml"
response = requests.get(url)
xml_text = response.text

# Parsing data XML
root = ET.fromstring(xml_text)

# Mencari data suhu di kota Samarinda (id="501354")
samarinda_data = None
for area in root.findall('.//area[@id="501354"]'):
    if area.attrib['type'] == 'land':
        samarinda_data = area
        break

if samarinda_data is None:
    print("Data suhu untuk kota Samarinda tidak ditemukan.")
else:
    # Mengambil data suhu pada setiap interval waktu (h=0 hingga h=66)
    suhu_data = samarinda_data.findall('./parameter[@id="t"]/timerange')

    # Mengambil nilai suhu pada setiap interval waktu
    waktu = []
    suhu_values = []
    for suhu in suhu_data:
        jam = int(suhu.attrib['h'])
        if jam <= 66:  # Hanya mengambil data hingga h=66
            waktu.append(jam)
            suhu_values.append(float(suhu.find('value').text))

    # Membuat plot suhu
    plt.plot(waktu, suhu_values)
    plt.xlabel('Waktu (jam)')

    # Mengatur label sumbu x menjadi per interval waktu 6 jam dengan ulangan nilai 0, 6, 12, 18
    x_ticks = np.tile([6, 12, 18, 24], len(waktu)//4 + 1)[:len(waktu)]
    plt.xticks(waktu, x_ticks)

    plt.ylabel('Suhu (°C)')
    plt.title('Plot Suhu di Samarinda')
    plt.grid(True)
    plt.show()

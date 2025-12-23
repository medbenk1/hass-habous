import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fetch the HTML content from API
url = "https://www.habous.gov.ma/prieres/horaire-api.php?ville=7"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
}
response = requests.get(url, headers=headers, verify=False)
html_content = response.text

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with class "horaire"
table = soup.find('table', {'class': 'horaire'})
if table is None:
    raise ValueError("Impossible de trouver le tableau des horaires dans le HTML")

# Extract all time cells (td with color #055D96)
time_cells = table.find_all('td', {'style': lambda x: x and '#055D96' in str(x)})

if len(time_cells) < 5:
    raise ValueError(f"Nombre insuffisant d'horaires trouvés: {len(time_cells)}")

# Extract times (they are in order: Alfajr, Chourouq, Dhuhr, Asr, Maghrib, Ishae)
times = [cell.get_text().strip() for cell in time_cells]

current_date = datetime.now().date()

data = {
    'Alfajr': datetime.strptime(f"{current_date} {times[0]}", "%Y-%m-%d %H:%M").isoformat(),
    'Chourouq': datetime.strptime(f"{current_date} {times[1]}", "%Y-%m-%d %H:%M").isoformat(),
    'Dhuhr': datetime.strptime(f"{current_date} {times[2]}", "%Y-%m-%d %H:%M").isoformat(),
    'Asr': datetime.strptime(f"{current_date} {times[3]}", "%Y-%m-%d %H:%M").isoformat(),
    'Maghrib': datetime.strptime(f"{current_date} {times[4]}", "%Y-%m-%d %H:%M").isoformat(),
    'Ishae': datetime.strptime(f"{current_date} {times[5]}", "%Y-%m-%d %H:%M").isoformat(),
}

json_data = json.dumps(data, indent=4)

print(json_data)

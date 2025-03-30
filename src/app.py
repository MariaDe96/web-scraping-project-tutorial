import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://companies-market-cap-copy.vercel.app/index.html"
try:
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    print("Página descargada exitosamente")
except requests.exceptions.RequestException as e:
    print("Ocurrió un error:", e)
    exit()

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find('table')
if table:
    print("Tabla con la evolución anual encontrada.")
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cells = row.find_all('td')
        year = cells[0].text.strip()
        revenue = cells[1].text.strip()
        change = cells[2].text.strip()
        data.append({"Year": year, "Revenue": revenue, "Change (%)": change})

    df = pd.DataFrame(data)
    print("Datos almacenados en un DataFrame:")
    print(df)

    df.to_csv('earnings_data.csv', index=False, encoding='utf-8')
    print("Datos guardados en 'earnings_data.csv'.")
else:
    print("No se encontró la tabla con la evolución anual.")

#Vamos a limpiar los datos $ y B del data
df = pd.DataFrame(data)
print("Datos sin limpiar")
print(df)

df['Revenue']= df['Revenue'].str.replace('$', '', regex=False).str.replace('B', '', regex=False)
df['Change (%)']= df['Change (%)'].str.replace('%', '', regex=False)
df.fillna(0, inplace=True)
df = df[df['Revenue'] != '']
df = df[df['Change (%)'] != '']
df['Revenue']= pd.to_numeric(df['Revenue'], errors='coerce')
df['Change (%)']= pd.to_numeric(df['Change (%)'], errors='coerce')
df.fillna(0, inplace=True)
df.to_csv('earnings_data_cleaned.csv', index=False, encoding='utf-8')
print("Datos limpios:")
print(df)

import sqlite3
import pandas as pd

csv_file = 'earnings_data_cleaned.csv'
try: 
    df = pd.read_csv(csv_file)
    print("Datos desde el CVS")
    print(df)
except Exception as e:
    print("Error al cargar los datos", e)
    exit()

base_file = 'earnings_data.base'
connection = sqlite3.connect(base_file)
cursor = connection.cursor()
print(f"Base de datos {base_file} creada.")

create_table_query = '''
CREATE TABLE IF NOT EXISTS Earnings (
     Year INTEGER NOT NULL,
     Revenue REAL NOT NULL,
     Change REAL NOT NULL
);
'''
cursor.execute(create_table_query)
print("Tabla 'Earnings' creada.")

insert_query= '''
INSERT INTO Earnings (Year, Revenue, Change)
VALUES (?, ?, ?);
'''
for index, row in df.iterrows():
    cursor.execute(insert_query, (row['Year'], row['Revenue'], row['Change (%)']))
print("Datos insertados en la tabla 'Earnings'.")

connection.commit()
print("Cambios almacenados.")

connection.close()
print(f"Conexion {base_file} cerrada.")

import matplotlib.pyplot as plt

print("Estructura de datos del DataFrame")
print(df.head())
print(df.dtypes)
# EJEMPLO 1 

plt.figure(figsize=(10, 6))
plt.plot(df['Year'], df['Revenue'], marker='o', linestyle='-', color='b', label='Ingresos')
plt.title('Crecimiento de los Ingresos', fontsize=14)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Ingresos ($B)', fontsize=12)
plt.grid(True)
plt.legend()
plt.show()
plt.savefig('ingresos.png')

# EJEMPLO 2 

plt.figure(figsize=(10, 6))
plt.plot(df['Year'], df['Change (%)'], color='orange', label='Cambio (%)')
plt.title('Porcentaje del cambio anual', fontsize=14)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Change (%)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.show()
plt.savefig('porcentaje.png')

# EJEMPLO 3 

plt.figure(figsize=(10, 6))
plt.scatter(df['Revenue'], df['Change (%)'], color='green', alpha=0.7, label='Relación')
plt.title('Relación de Ingresos y Cambio (%)', fontsize=14)
plt.xlabel('Ingresos ($B)', fontsize=12)
plt.ylabel('Cambio (%)', fontsize=12)
plt.grid(True)
plt.legend()
plt.show()
plt.savefig('cambioporcentual.png')


## ejercicio adiconal
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://companies-market-cap-copy.vercel.app/earnings.html'
try: 
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text
    print("Página descargada exitosamente")
except requests.exceptions.RequestException as e:
    print("Ocurrió un error:", e)
    exit()

soup = BeautifulSoup(html_content, 'html.parser')

table = soup.find('table')
if table:
    print("Tabla con la evolución anual encontrada.")
    rows = table.find_all('tr')
    tesla_data = []

    for row in rows[1:]:
        cells = row.find_all('td')
        company = cells[0].text.strip()
        year = cells[1].text.strip()
        earnings = cells[2].text.strip()

        if company.lower() == "tesla":
            try:
                tesla_data.append({"Year": int(year), "Earnings": earnings})
            except ValueError:
                print(f"Error: {year}")
    df = pd.DataFrame(tesla_data)

    if not df.empty:
        latest_tesla_data = df.loc[df['Year'].idxmax()]
        print(f"Ganancias del ultimo año:\nAño: {latest_tesla_data['Year']}, Ganancias: {latest_tesla_data['Earnings']}")
    else:
        print("No se encontraron datos para tesla.")
else:
    print("No se encontró la tabla con la evolución anual.")

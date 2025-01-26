from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Configurar el navegador y el controlador
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Para que no se abra la ventana del navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de la página
url = "https://www.decampoacampo.com/__dcac/outside/canuelas/precios"

# Cargar la página
driver.get(url)

# Esperar unos segundos para asegurarse de que JavaScript cargue el contenido
time.sleep(5)  # Ajusta este tiempo si es necesario

# Obtener el HTML después de que se haya cargado el contenido dinámicamente
html = driver.page_source

# Analizar el HTML con BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Buscar la fecha del último cierre de mercado
fecha_element = soup.find('span', class_='aclaracion_semana')
if fecha_element:
    fecha = fecha_element.text.strip().replace("(", "").replace(")", "")
    print(f"Fecha del último cierre de mercado: {fecha}")
else:
    print("No se encontró la fecha del último cierre de mercado.")

# Buscar el precio correspondiente a "Novillitos hasta 390 Kg."
tabla_precios = soup.find('div', id='tabla-precios')
if tabla_precios:
    filas = tabla_precios.find_all('tr', class_='tr_precios')
    for fila in filas:
        categoria = fila.find('td', class_='td_precios')
        if categoria and "Novillitos hasta 390 Kg." in categoria.text:
            precio = fila.find_all('td')[1].find('span', class_='h4').text.strip()
            print(f"Precio para Novillitos hasta 390 Kg.: {precio}")
            break
else:
    print("No se encontró la tabla de precios.")

# Cerrar el navegador
driver.quit()

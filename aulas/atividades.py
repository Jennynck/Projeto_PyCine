import locale
import random
from zoneinfo import ZoneInfo
from fastapi import FastAPI
from datetime import datetime

import requests

app = FastAPI()

# ----------------------------------------------------
# Atividade 1
# ----------------------------------------------------

locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

@app.get("/diasemana")
def dia_semana():
    return{"diasemana": datetime.now().strftime("%A")}

# ----------------------------------------------------
# Atividade 2
# ----------------------------------------------------

@app.get("/number/{num}")
def numero(num: int):
    if num % 2 == 0:
        return {
            "numero": num,
            "tipo": "PAR"
        }
    else:
        return {
            "numero": num,
            "tipo": "ÍMPAR"
        }

# ----------------------------------------------------  
# Atividade 3
# ----------------------------------------------------
    
tzs = {
    "brasilia": "America/Sao_Paulo",
    "tokyo": "Asia/Tokyo",
    "londres": "Europe/London"
}

@app.get("/hora/{pais}")
def hora_pais(pais: str):
    tz_nome = tzs.get(pais.lower())
    if tz_nome:
        hora = datetime.now(ZoneInfo(tz_nome)).strftime("%H:%M:%S")
        return {"hora": hora}

# ----------------------------------------------------    
# Atividade 4
# ----------------------------------------------------

"""
{
  "q":"Quality means doing it right when no one is looking.",
  "a":"Henry Ford",
  "h":"<blockquote>“Quality means doing it right when no one is looking.” — <footer>Henry Ford</footer></blockquote>"
}

"""

@app.get("/frase")
def get_frase():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url)
    data = response.json()

    frase = data[0]["q"]
    autor = data[0]["a"]

    return {"frase": frase, "autor": autor}

# ----------------------------------------------------
# Atividade 5
# ----------------------------------------------------

names = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Australia", "Bahamas", "Bolivia", "Brasil"]

isos = ["AF", "AL", "DZ", "AS", "AU", "BS", "BO", "BR"] 

areas = [647.500, 28.748, 2.381740, 199, 7.686850, 13.940, 1.098580, 8.511965]

@app.get("/country/name/{name}")
def get_country_name(name: str):
    for i in range(len(names)):
        if names[i].lower() == name.lower():
            return {"name": names[i], 
                    "iso": isos[i], 
                    "area": areas[i]}
    return {"detail": "País não encontrado"}

@app.get("/country/iso/{iso}")    
def get_country_iso(iso: str):
    for i in range(len(isos)):
        if isos[i].upper() == iso.upper():
            return {"name": names[i], 
                    "iso": isos[i], 
                    "area": areas[i]}
    return {"detail": "Código ISO não encontrado ou inexistente"}

@app.get("/country/area/{area}") 
def get_country_area(area: float):
    for i in range(len(areas)):
        if areas[i] == area:
            return {"name": names[i], 
                    "iso": isos[i], 
                    "area": areas[i]}
    return {"detail": "Área não encontrada"}


# ----------------------------------------------------
# Atividade 6
# ----------------------------------------------------

# /sortear/6/60
# sortear seis numeros de 1 até 60
@app.get("/sortear/{quant}/{max_num}")
def sortear(quant: int, max_num: int):
    if quant > max_num:
        return {"erro": "A quantidade é maior que o valor máximo"}
    
    num = random.sample(range(1, max_num + 1), quant)
    return {"sorteio": num}

# uvicorn atividades:app --reload
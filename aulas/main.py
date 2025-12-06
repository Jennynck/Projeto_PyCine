from fastapi import FastAPI

app = FastAPI()

data = {
    55: "Brasil",
    20: "Egito",
    54: "Argentina"
}

# /country/55
@app.get("/country/{area}")
def country_area(area: int):
    if area in data:
        return{
            "area": area,
            "name": data[area]
        }
    
@app.get("/users")
def list_users():
    import json
    with open("users.json") as f:
        return json.load(f)
    
# /sortear/6/60
# sortear seis numeros de 1 até 60
@app.get("/sortear/{quant}/{max}")
def sortear():
    pass

# Definir o ENDPOINT
# http://localhost:8000/

@app.get("/")
def hello():
    return {"mensagem": "Hello World"}
    

@app.get("/now")
def datetime_now():
    from datetime import datetime
    return {
        "datahora": datetime.now(),
        "pais": "BR"
    }

# uvicorn atv1:app --reload
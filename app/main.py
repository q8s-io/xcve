from fastapi import FastAPI, HTTPException
from py2neo import Graph
from py2neo.data import Node, Relationship
import json

app = FastAPI()
graph = Graph(host="xcve-neo4j", password='streams')


@app.get("/")
def read_root():
    ret = graph.run('match (n) return n limit 5').data()
    return {"Hello": json.dumps(ret)}

@app.get("/random")
def random():
    return {"random": '{}'}
 
@app.get("/search/{keyword}")
def search(keyword: str=None):
    return {"yourkey": keyword}

@app.get("/cve/{cve_id}")
def scann_cve(cve_id: str):
    if not cve_id:
        raise HTTPException(status_code=404, detail="No cve_id specified!")
    ret = graph.run('match (n:CVE) where n.name="{}" return  n'.format(cve_id)).data()
    return {cve_id: json.dumps(ret)}

@app.get("/vendor/{vendor_name}")
def search_vendor(vendor_name: str):
    return {"vendor_name": vendor_name}

@app.get("/product/{product_name}")
def search_product(product_name: str):
    return {"product_name": product_name}

@app.get("/proversion/{proversion_name}")
def proversion(proversion_name: str):
    return {"proversion_name": proversion_name}

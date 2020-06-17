#!/usr/bin/python
# -* - coding: UTF-8 -* -

from fastapi import FastAPI, HTTPException
from py2neo import Graph
from py2neo.data import Node, Relationship
import json

app = FastAPI()
graph = Graph(host="xcve-neo4j", password='streams')


@app.get("/")
@app.get("/random")
def random():
    # generate something random that maybe useful on main page.
    ret = graph.run('match (cve:CVE) with cve, rand() as number return cve order by number limit 10').data()
    return ret
 
@app.get("/search/{keyword}")
def search(keyword: str=None):
    return {"yourkey": keyword}

@app.get("/cve/{cve_id}")
def scann_cve(cve_id: str):
    # abs match cve-number
    if not cve_id:
        raise HTTPException(status_code=404, detail="No cve_id specified!")
    cve = graph.run('match (cve:CVE) where cve.name="{}" return cve'.format(cve_id)).data()[0]
    relations = graph.run('match (cve:CVE)-[r]->(x) where cve.name="{}" return r,x'.format(cve_id)).data()
    
    for i in relations:
        rlname = i.get('r').__class__.__name__
        if not rlname in cve:
            cve[rlname] = []
        x = dict(i.get('x'))
        x['label'] = str(i.get('x').labels)
        cve[rlname].append(x)

    return {cve_id: cve}

@app.get("/vendor/{vendor_name}")
def search_vendor(vendor_name: str):
    # abs search by vendor
    return {"vendor_name": vendor_name}

@app.get("/product/{product_name}")
def search_product(product_name: str):
    # abs search by product
    return {"product_name": product_name}

@app.get("/proversion/{proversion_name}")
def proversion(proversion_name: str):
    # match procut-version
    return {"proversion_name": proversion_name}

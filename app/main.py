#!/usr/bin/python
# -* - coding: UTF-8 -* -

from fastapi import FastAPI, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from py2neo import Graph
from py2neo.data import Node, Relationship, walk
from enum import Enum
from pydantic import BaseModel
from typing import Set
from itertools import groupby
import json

app = FastAPI()
# CROS
# read more: https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], # allow any origin.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#graph = Graph(host="xcve-neo4j", password='streams')
graph = Graph(host="127.0.0.1", password='streams')


def cve_relate_nodes(cve_id, deep):
    '''
    i.get('x').identity  # node's ID
    i.get('x').labels  # node's labels as list
    i.get('x')['name']  # value of name in node
    i.get('r').__class__.__name__  # relation's name
    '''
    ret = {}
    relations = graph.run('match (cve:CVE)-[r]->(x) where cve.name="{}" return r,x'.format(cve_id)).data()
    for i in relations:
        rlname = i.get('r').__class__.__name__
        if not rlname in ret:
            ret[rlname] = []
        x = dict(i.get('x'))
        x['label'] = str(i.get('x').labels)
        ret[rlname].append(x)
    return ret

def cve_relate_nodes_v3(cve_id, deep):
    nodes = {}
    edges = []
    relations = graph.run('match (cve:CVE)-[r1]->(x)<-[r2:FORK|PRODUCE]-(y) where cve.name="{}" return cve, r1, x, r2, y'.format(cve_id)).data()
    # cve--r1--> x <--r2--y
    for i in relations:
        # make nodes
        def append_nodes(n):
            if n.identity not in nodes:
                nodes[n.identity] = {
                            "id": n.identity,
                            "label": n.get('name', 'N/A'),
                            "class": list(n._labels)[0],
                        }
        append_nodes(i.get('cve')) # cve_id => cve ID
        append_nodes(i.get('x'))
        append_nodes(i.get('y'))
        # make edges
        def append_edges(s, label, t):
            edges.append({
                    "source": s,
                    "target": t,
                    "label": label,
                    # weight: 2
                })
        append_edges(i.get('cve').identity, i.get('r1').__class__.__name__, i.get('x').identity)
        append_edges(i.get('y').identity, i.get('r2').__class__.__name__, i.get('x').identity)
    nodes = list(nodes.values())
    ret = {
        "nodes": nodes,
        "edges": edges,
    }
    return ret


def related_nodes(rootid, deep=1):
    nodes = {}
    edges = []
    paths = graph.run('match p=(root)-[*{}]-() where ID(root)={} return p'.format(deep, rootid)).data()

    # paths is a set of path like : a-[r]->(b)
    for path in paths:
        for x in walk(path.get('p')):
            # x1 is node a
            # x2 is relation r
            # x3 is node b
            if issubclass(type(x), Node):
                n = x # x is node

            if issubclass(type(x), Relationship):
                def append_nodes(n):
                    if n.identity not in nodes:
                        nodes[n.identity] = {
                                    "id": n.identity,
                                    "label": n.get('name', 'N/A'),
                                    "class": list(n._labels)[0],
                                }
                append_nodes(x.start_node)
                append_nodes(x.end_node)
                def append_edges(s, label, t):
                    edges.append({
                            "source": s,
                            "target": t,
                            "label": label,
                        })
                append_edges(x.start_node.identity, x.__class__.__name__, x.end_node.identity)
    nodes = list(nodes.values())
    ret = {
        "nodes": nodes,
        "edges": edges,
    }
    return ret


def count_nodes(nodes):
    ret = []
    sortednodes = sorted(nodes, key=lambda x: x.get('class', ''))
    for k, g in groupby(sortednodes, lambda x: x.get('class', '')):
        glen = len(list(g))
        ret.append({k: glen})
    return ret


def cve_relate_nodes_v2(cve_id, deep):
    nodes = {}
    edges = {}
    relations = graph.run('match (cve:CVE)-[r]->(x)<-[s:EFFECT]-(y) where cve.name="{}" return r,x, s, y'.format(cve_id)).data()
    for i in relations:
        # make nodes
        def append_nodes(n):
            if n.identity not in nodes:
                nodes[n.identity] = {
                            "id": n.identity,
                            "label": n.get('name', 'N/A'),
                            "class": n.labels,
                        }
        append_nodes(i.get('x'))
        append_nodes(i.get('y'))
        # make edges
        def append_edges(s, label, t):
            edges.append({
                    "source": s,
                    "target": t,
                    "label": label,
                    # weight: 2
                })
        append_edges(root, 'EFFECT', i.get('x').identity)
        append_edges(i.get('y').identity, 'EFFECT', i.get('x').identity)
    nodes = list(nodes.values())
    return ret


@app.get("/")
@app.get("/random")
def random():
    ret = graph.run('match (cve:CVE) with cve, rand() as number return cve order by number limit 10').data()
    return ret


@app.get("/frontconf",
    summary="获取前端相关配置",
    description="前端可能需要一些配置持久化到后端，比如配色、图形的色值、半径，字体大小等。",
)
async def frontconf():
    return {
        "graph": {
            "Product": {
                "color": "#6699CC",
            },
            "CVE": {
                "color": "#99CCFF",
            },
            "Vendor": {
                "color": "#66CCCC",
            },
            "Proversion": {
                "color": "#FFCCCC",
            }
        }
    }


class CateName(str, Enum):
    vendor = "Vendor"
    product = "Product"
    proversion = "Proversion"
    cve = "CVE"
    unknown = "unknown"
@app.get("/search",
    summary="搜索关键字",
    description="如果是某种类型的搜索，会精准匹配。默认类型搜索的是product，模糊匹配",
)
async def search(
    deep: int = Query(
        1,
        description="图的遍历深度",
        le = 3,
        ge = 1,
        ),
    cate: CateName = Query(
        "CVE",
        description="搜索的类型",
        ),
    keyword: str = Query(
        None,
        description="关键字",
        max_length=50,
        )
    ):
    if cate == "unknown":
        raise HTTPException(status_code=404, detail="Please specify the cate!")
    return neo4j_strict_match(cate, keyword, deep)


@app.get("/sug",
    summary="猜想",
    description="根据传入的参数，猜想用户想搜的关键字",
)
async def sug(
    prefix: str = Query(
        None,
        description="以此参数为前缀，猜想出相关的实体。实体类型可能是：CVE",
        max_length=50,
        )
    ):
    # keys = graph.run('match (x:Vendor) where x.name starts with "{}" return x limit 5 union match (x:Product) where x.name starts with "{}" return x limit 5'.format(prefix, prefix)).data()
    keys = graph.run('match (x:CVE) with x, rand() as number where toLower(x.name) starts with toLower("{}") return x order by number limit 5'.format(prefix, prefix)).data()
    return [i.get('x').get('name') for i in keys]


@app.get("/cve",
    summary="cve搜索",
    description="精准匹配cve编号",
)
async def scann_cve(
    deep: int = Query(
        1,
        description="图的遍历深度",
        le = 3,
        ge = 1,
        ),
    cve_id: str = Query(
        None,
        description="精确的cve编号，如CVE-2000-0981",
        max_length=50,
        )
    ):
    if not cve_id:
        raise HTTPException(status_code=404, detail="No cve_id specified!")
    cve = graph.run('match (cve:CVE) where cve.name="{}" return cve'.format(cve_id)).data()[0]
    cve['relations'] = cve_relate_nodes_v3(cve_id, deep)
    cve['counts'] = []
    sortednodes = sorted(cve['relations'].get('nodes', []), key=lambda x: x.get('class', ''))
    for k, g in groupby(sortednodes, lambda x: x.get('class', '')):
        glen = len(list(g))
        cve['counts'].append({k: glen})
    return {cve_id: cve}


def neo4j_strict_match(label, name, deep=1):
    if not name:
        return None
    ret = graph.run('match (meta:{}) where meta.name="{}" return meta'.format(label, name)).data()
    if not ret:
        raise HTTPException(status_code=404, detail="{}:{} not found!".format(label, name))
    ret = ret[0]
    if deep > 0:
        ret['relations'] = related_nodes(ret.get('meta').identity, deep)
        ret['counts'] = count_nodes(ret['relations'].get('nodes', []))
    return {name: ret}


@app.get("/vendor",
    summary="vendor厂商搜索",
    description="精准匹配厂商名字",
)
async def search_vendor(vendor_name: str= Query(
        None,
        description="厂商，如mysql",
        max_length=50,
        )
    ):
    if not vendor_name:
        raise HTTPException(status_code=404, detail="No vendor_name specified!")
    vendor = graph.run('match (vendor:Vendor) where vendor.name="{}" return vendor'.format(vendor_name)).data()
    if not vendor:
        raise HTTPException(status_code=404, detail="vendor_name:{} not found!".format(vendor_name))
    vendor = vendor[0]
    vendor['relations'] = related_nodes(vendor.get('vendor').identity, 1)
    vendor['counts'] = count_nodes(vendor['relations'].get('nodes', []))
    return {vendor_name: vendor}


@app.get("/product",
    summary="product产品搜索",
    description="精准匹配产品名字",
)
async def search_product(product_name: str= Query(
        None,
        description="产品名字，如linux",
        max_length=50,
        )
    ):
    return neo4j_strict_match("Product", product_name)


@app.get("/proversion/{proversion_name}")
async def proversion(proversion_name: str):
    return neo4j_strict_match("Product", product_name)

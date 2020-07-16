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


@app.get("/random",
    summary="随机实体",
    description="随机生成若干个实体，一般用在首页的搜索建议",
)
def random():
    ret = graph.run('match (n) with n, rand() as number return n order by number limit 10').data()
    return [{'class': list(i.get('n')._labels)[0], 'name':i.get('n').get('name', '')} for i in ret]


@app.get("/sug",
    summary="猜想",
    description="根据传入的参数，猜想用户想搜的关键字",
)
async def sug(
    prefix: str = Query(
        None,
        description="以此参数为前缀，猜想出相关的实体。实体类型可能是CVE、Product、Vendor",
        max_length=50,
        )
    ):
    ret = graph.run('match (n) where (n:CVE OR n:Product OR n:Vendor) AND toLower(n.name) starts with "{}" return n limit 10'.format(prefix)).data()
    return sorted([{'class': list(i.get('n')._labels)[0], 'name':i.get('n').get('name', '')} for i in ret],
                key=lambda x: x.get('class', ''))


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

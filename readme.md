# xcve

xcve是一个基于cve和一系列相关数据（如nvd、cvss、软件、软件厂商）的检索平台。底层使用图数据库进行存储。可以基于cve查询相关信息，或者通过软件、厂商等反查出相关的cve。xcve通过api提供接口。并且有一个简单的web界面，供用户查询使用。
相关技术：

* neo4j
* cypher
* fastapi
* docker / docker-compose

## Installation

使用docker-compose启动
```bash
git clone git@github.com:q8s-io/xcve.git
cd xcve
docker-compose build
docker-compose up -d
```

首次启动，数据库中还没有cve数据，还需将数据导入（导入过程可能花费数个小时。如果不需要完整cve数据可以尝试截断 neo4j/import/cves.csv 为更小的文件，以加快导入速度）：
```bash
docker exec -ti xcve-neo4j bash
/var/lib/neo4j  cypher-shell -u neo4j -p streams
neo4j@neo4j> :source /app/csv2neo.cypher
```
#### 关于cve数据源
neo4j支持从csv导入数据，cves.csv来自于开源漏扫工具openvas。openvas中有一个结构化的sqlite数据库scap.db，其中包含了从CVE-1999-0001到CVE-2019-9978的cve漏洞。要通过scap.db生成可用的cves.csv还需要做一些适配工作：
1、将scap.db:cves保存为csv文件。
2、修改csv文件中的\"替换为\\"    否则neo4j会解析错误。

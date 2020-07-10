# xcve

xcve是一个基于cve和一系列相关数据（如nvd、cvss、软硬件、软硬件厂商）的检索平台。底层使用图数据库进行存储。可以基于cve查询相关信息，或者通过软件、厂商等反查出相关的cve。xcve通过api提供接口。并且有一个简单的web界面，供用户查询使用。
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
docker-compose [-f docker-compose-dev.yml] build
docker-compose [-f docker-compose-dev.yml] up -d
```

首次启动，数据库中还没有cve数据，还需将数据导入（导入过程可能花费数个小时。如果不需要完整cve数据可以尝试截断 neo4j/import/cves.csv 为更小的文件，以加快导入速度）：
```bash
docker exec -ti xcve-neo4j bash
[in container] cypher-shell -u neo4j -p streams -f /app/csv2neo.cypher
```

或者一行命令
```bash
docker exec --interactive --tty xcve-neo4j bin/cypher-shell -u neo4j -p streams -f /app/csv2neo.cypher
```
#### 关于cve数据源
neo4j支持从csv导入数据，cves.csv来自于开源漏扫工具openvas。openvas中有一个结构化的sqlite数据库scap.db，其中包含了从CVE-1999-0001到CVE-2019-9978的cve漏洞。要通过scap.db生成可用的cves.csv还需要做一些适配工作：
1、将scap.db:cves保存为csv文件。
2、修改csv文件中的\\"替换为\\\\"，但不要存在\\\\\\"。否则neo4j会解析错误。csv中不要有\\""，""本来是把"转义了，但是\会把前一个"给再次转义，导致""孤立。替换可分2步替换（注意以markdown解析器显示为准，勿参考md原文，否则符号层数有区别）：
>\\" -> \\\\"     
>\\\\\\" -> \\\\"

（避免混淆，再次口述：csv中不要有：3个backslash后跟引号；1个backslash后跟引号。如果有的话，只能是2个backslash后跟引号）
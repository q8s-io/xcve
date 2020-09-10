from py2neo import Graph,Node,Relationship
from kafka import KafkaConsumer
import json

# 连接Neo4j数据库
graph = Graph(host='123.59.120.93',password='streams')
# 连接kakfa
consumer = KafkaConsumer(auto_offset_reset='earliest', bootstrap_servers= ['117.50.109.103:9092'], value_deserializer=lambda m: json.loads(m.decode('ascii')))
# kafka订阅topic
consumer.subscribe(topics= ('imageLayers'))

for message in consumer:
    print(message.value['data']['image_name'])
    print(message.value['data']['vuln_data'])
    # 从kafka读取数据并存入Neo4j中，同时为有相同层级的镜像建立关系
    graph.run('MERGE (n:Image {name:$name})'
              'SET n.layers=$layers '
              'WITH n '
              'UNWIND n.layers as layer '
              'WITH layer , n  '
              'MATCH (m:Image) '
              'where layer in m.layers '
              'AND ID(m)<>ID(n) '
              'MERGE (n)-[:EFFECT]-(m)', parameters={"name":message.value['image_name'],"layers":message.value['image_layers']})

    #graph.run('MERGE (i:Image {name: $image_name}) '
    #          'SET i.status=$status, i.time=$time '
    #          'WITH i '
    #          'UNWIND $vuln_data AS cve '
    #          'MERGE (c:CVE {name:cve.cve}) '
    #          'MERGE (c)-[:EFFECT]->(i)', parameters={"image_name":message.value['data']['image_name'],
    #                                                "status":message.value['data']['task_status'],
    #                                                "time":message.value['data']['create_time'],
    #                                                "vuln_data":message.value['data']['vuln_data']}
    #                                                )
CREATE CONSTRAINT ON (c:Vendor) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Product) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Proversion) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Image) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:CVE) ASSERT c.name IS UNIQUE;

USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///cves.csv' AS line
MERGE (c:CVE {name: line.name})
SET c.id=line.id, c.uuid=line.uuid, c.comment=line.comment, c.description=line.description, c.creation_time=line.creation_time, c.modification_time=line.modification_time, c.vector=line.vector, c.complexity=line.complexity, c.authentication=line.authentication, c.confidentiality_impact=line.confidentiality_impact, c.integrity_impact=line.integrity_impact, c.availability_impact=line.availability_impact, c.products=line.products, c.cvss=line.cvssWITH line, c
WHERE line.products <> ""
WITH split(trim(line.products), ' ') AS products, c
UNWIND products AS product
WITH split(product, ':') AS cpe, c
MERGE (v:Vendor {name:cpe[2]})
MERGE (p:Product {name:cpe[3]})
MERGE (pv:Proversion {name:cpe[3]+'#'+coalesce(cpe[4], "Unknown")})
WITH c,v,p,pv 
MERGE (c)-[:EFFECT]->(v)
MERGE (c)-[:EFFECT]->(p)
MERGE (c)-[:EFFECT]->(pv)
MERGE (v)-[:PRODUCE]->(p)
MERGE (p)-[:FORK]->(pv);

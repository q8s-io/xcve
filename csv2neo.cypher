CREATE CONSTRAINT ON (c:Vendor) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Product) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Proversion) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Image) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:CVE) ASSERT c.name IS UNIQUE;

USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM 'file:///cves.csv' AS line
CREATE (c:CVE {id: line.id,uuid: line.uuid,name: line.name,comment: line.comment,description: line.description,creation_time: line.creation_time,modification_time: line.modification_time,vector: line.vector,complexity: line.complexity,authentication: line.authentication,confidentiality_impact: line.confidentiality_impact,integrity_impact: line.integrity_impact,availability_impact: line.availability_impact,products: line.products,cvss: line.cvss})
WITH line, c
WHERE line.products <> ""
WITH split(trim(line.products), ' ') AS products, c
UNWIND products AS product
WITH split(product, ':') AS cpe, c
MERGE (v:Vendor {name:cpe[2]})
MERGE (p:Product {name:cpe[3]})
MERGE (pv:Proversion {name:cpe[3]+':'+coalesce(cpe[4], "Unknown")})
MERGE (c)-[:EFFECT]->(v)
MERGE (c)-[:EFFECT]->(p)
MERGE (c)-[:EFFECT]->(pv)
MERGE (v)-[:PRODUCE]->(p)
MERGE (p)-[:FORK]->(pv);

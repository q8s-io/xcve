CREATE CONSTRAINT ON (c:Vendor) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Product) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Proversion) ASSERT c.name IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 'file:///cves.csv' AS line
CREATE (c:CVE {name: line.name, description: line.description})
WITH line
WHERE line.products <> ""
WITH split(trim(line.products), ' ') AS products
UNWIND products AS product
WITH split(product, ':') AS cpe
MERGE (v:Vendor {name:cpe[2]})
MERGE (p:Product {name:cpe[3]})
MERGE (pv:Proversion {name:cpe[3]+':'+coalesce(cpe[4], "Unknown")})
CREATE (c)-[:EFFECT_VENDOR]->(v)
CREATE (c)-[:EFFECT_PRODUCT]->(p)
CREATE (c)-[:EFFECT_VERSION]->(pv)
CREATE (v)-[:FROM]->(c)
CREATE (p)-[:FROM]->(c)
CREATE (pv)-[:FROM]->(c)
MERGE (v)-[:PRODUCE]->(p)
MERGE (p)-[:FORK]->(pv);
//Connect categories to metrics
MATCH (c:Categories), (m:Metrics)
WHERE c.title = m.category
MERGE (c)-[:SUMMARIZES]->(m)

// Connect metrics to keywords
MATCH(m:Metrics)
WITH m
    UNWIND(SPLIT(m.keywords, ',')) as keyword
WITH m, keyword
    MATCH (k:Keywords {title: keyword})
    MERGE (m)-[:CONTAINS]->(k)

// Connect metrics to subcategory_foci
MATCH (m:Metrics)
WITH m
    UNWIND(SPLIT(m.subcategory_foci, ',')) as focus
WITH m, focus
    MATCH (sf:Subcategory_Focus {subcategory_foci: focus})
    MERGE (m)-[:CONTAINS]->(sf)

//Connect programs to organizations
MATCH (p1:Programs)
WITH p1
    UNWIND SPLIT(p1.link_to_org, '|') as links
WITH p1, links
    MERGE (o:Organizations {uid: links})
    MERGE (p1)<-[:LED_AND_SPONSOR]-(o)

//Connect programs to protocols
MATCH (p1:Programs)
WITH p1
    UNWIND SPLIT(p1.link_to, '|') as links
WITH p1, links
    MATCH (p2:Protocols {uid: links})
    MERGE (p1)-[:USES]->(p2)

// Connect protocol - category link
MATCH (c: Categories), (p: Protocols) 
WHERE c.title IN apoc.convert.fromJsonList(p.metric_category)
MERGE (c)-[:TAGGED]->(p)

// Connect protocol - keyword link
MATCH (k: Keywords), (p: Protocols) 
WHERE toLower(k.title) IN apoc.convert.fromJsonList(p.metric_title)
MERGE (k)-[:TAGGED]->(p)

// Connect protocol - metric link
MATCH (m: Metrics), (p: Protocols) 
WHERE m.title IN apoc.convert.fromJsonList(p.metric_subcategory)
MERGE (m)-[:TAGGED]->(p)

//Connect protocols to methods
MATCH (p:Protocols)
WITH p
    UNWIND SPLIT(p.link_to, '|') as links
WITH p, links
    MATCH (m:Methods {uid: links})
    MERGE (p)-[:IMPLEMENT]->(m)

// Connect sites to Categories
MATCH (c: Categories)
MATCH (s: Sites)
WHERE s.category CONTAINS c.title
MERGE (c)-[r:LOCATED_AT]->(s)

// Connect sites to organizations
MATCH (o: Organizations)
MATCH (s: Sites)
WHERE o.name CONTAINS s.organization
MERGE (o)-[r:LOCATED_AT]->(s)

// Connect sites to programs
MATCH (p2: Programs)
MATCH (s: Sites)
WHERE s.program = p2.name
MERGE (p2)-[r:LOCATED_AT]->(s)

// Connect sites to protocols
MATCH (s: Sites)
MATCH (p1: Protocols)
WHERE s.protocol = p1.title
MERGE (p1)-[:LOCATED_AT]->(s)

// Connect STYN_GOLD protocol to keywords
MATCH (p:Protocols), (k:Keywords)
WHERE ', ' + p.keywords + ',' CONTAINS ', '+ k.title + ','
MERGE (p)-[:HAS_KEYWORD]->(k)

// Connect STYN_GOLD protocol to tags
MATCH (p:Protocols), (t:Tags)
WHERE ', ' + p.tags + ',' CONTAINS ', '+  t.title + ','
MERGE (p)-[:HAS_TAG]->(t)

//Connect subjects to categories
MATCH (s:Subject), (c:Categories)
WHERE s.name = c.subject
MERGE (s)-[:SUMMARIZES]->(c)

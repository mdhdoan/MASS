// A lot changes since the jsons invaded

// Connect organizations to programs
MATCH (o:Organizations)
MATCH (p:Programs)
WHERE o.title in p.organization
MERGE (o)-[:SPONSORS]->(p)

//Connect programs to protocols
MATCH (p1: Programs)
MATCH (p2: Protocols)
WHERE p2.programUrl = p1.uid
MERGE (p2)-[:USED_IN]->(p1)

// Connect methods to protocols
MATCH (m: Methods)
MATCH (p: Protocols)
WHERE m.uid IN p.methods
MERGE (m)-[:USED_IN]->(p)

// Connect metrics to protocols
MATCH (m: Metrics)
MATCH (p: Protocols)
WHERE toInteger(m.uid) IN p.metric
MERGE (m)-[:USED_IN]->(p)

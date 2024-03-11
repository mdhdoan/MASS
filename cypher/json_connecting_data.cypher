// A lot changes since the jsons invaded

// Connect organizations to programs
MATCH (o:Organizations)
MATCH (p:Programs)
WHERE o.programs_url = p.url
MERGE (o)-[:SPONSORS]->(p)

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
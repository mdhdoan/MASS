// A lot changes since the jsons invaded

// Connect organizations to programs
MATCH (o:Organizations)
MATCH (p:Programs)
WHERE o.programs_url = p.url
MERGE (o)-[:SPONSORS]->(p)

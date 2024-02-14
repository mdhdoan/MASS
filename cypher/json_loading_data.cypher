// A lot of things changes when you use the full APOC and their stuff
// Load organization data
CALL apoc.load.directory('*.json', 'programs') YIELD value
WITH value as json_file
    CALL apoc.load.json(json_file) YIELD value as json_data
WITH json_data
    UNWIND json_data['organizations'] as organization
WITH json_data, organization
MERGE (o:Organizations {uid: organization})
    SET o.title = organization,
        o.programs_title = json_data['title'],
        o.programs_url = json_data['url']

// Load programs data
CALL apoc.load.directory('*.json', 'programs') YIELD value
WITH value as json_file
    CALL apoc.load.json(json_file) YIELD value as json_data
MERGE (m:Programs {uid: json_data['url']})
    SET m.title = json_data['title'], 
        m.mid = json_data['id'],
        m.primary_contact_name = json_data['primaryContactName'],
        m.primary_contact_email = json_data['primaryContactEmail'],
        m.organization = json_data['organizations'],
        m.url = json_data['url']

// Load protocols data
CALL apoc.load.directory('*.json', 'protocols') YIELD value
WITH value as json_file
    CALL apoc.load.json(json_file) YIELD value as json_data
MERGE (p:Protocols {uid: json_data['url']})
    SET p.title = json_data['title'], 
        p.background = json_data['background'],
        p.url = json_data.url,
        p.pid = json_data.id,
        p.assumptions = json_data.assumptions,
        p.methods = json_data.methods,
        p.objectives = json_data.objectives,
        p.ownername = json_data.ownerName,
        p.ownerEmail = json_data.ownerEmail,
        p.programUrl = json_data.programUrl

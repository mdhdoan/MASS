// A lot of things changes when you use the full APOC and their stuff
// Load organization data
CALL apoc.load.directory('*.json', 'programs') YIELD value
WITH value as json_file
    CALL apoc.load.json(json_file) YIELD value as json_data
WITH json_data
    UNWIND json_data['organizations'] as organization
WITH json_data, organization
MERGE (o:Organizations {uid: organization})
    SET o.title = organization

// Load programs data
CALL apoc.load.directory('*.json', 'programs') YIELD value
WITH value as json_file
    CALL apoc.load.json(json_file) YIELD value as json_data
MERGE (m:Programs {uid: json_data['url']})
    SET m.title = json_data['title'], 
        m.mid = json_data['id'],
        m.primary_contact_name = json_data['primaryContactName'],
        m.primary_contact_email = json_data['primaryContactEmail'],
        m.organization = json_data['organizations']
WITH m, json_data
    UNWIND json_data['protocols'] as protocol
WITH m, protocol
    SET m.protocol_title = protocol.title,
        m.protocol_url = protocol.url


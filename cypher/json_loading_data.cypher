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
MERGE (p:Programs {uid: json_data['url']})
    SET p.title = json_data['title'], 
        p.pid = json_data['id'],
        p.primary_contact_name = json_data['primaryContactName'],
        p.primary_contact_email = json_data['primaryContactEmail'],
        p.organization = json_data['organizations'],
        p.url = json_data['url']

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
        p.metric = [],
        p.objectives = json_data.objectives,
        p.ownername = json_data.ownerName,
        p.ownerEmail = json_data.ownerEmail,
        p.programUrl = json_data.programUrl
WITH json_data, p
    UNWIND json_data.metrics as metric_data
WITH p, metric_data
    SET p.metric = p.metric + [metric_data.id]
    SET p.metric = apoc.coll.toSet(p.metric)

// Load method data - topic
CALL apoc.load.json('full_details.json') YIELD value as json_data
WITH json_data
    MATCH(m:Methods)
    WHERE m.instruction = json_data.Document
    SET m.topic_id = json_data.Topic,
        m.representative = json_data.Representative_document,
        m.represent_words = json_data.Representation
    
// Load method synth data
CALL apoc.load.directory('*_synth.json', 'methods-synth') YIELD value
WITH value as json_file_name
CALL apoc.load.json(json_file_name) YIELD value as json_data
WITH split(substring(json_file_name, 14), '._')[0] as method_name, keys(json_data)[0] as json_key, json_data
MERGE (m:Methods {title: method_name})
    SET m += json_data

// LOAD topic name 
CALL apoc.load.json('topics.json') yield value
WITH value as topic_data
    MATCH(m: Methods)
WITH m, topic_data['custom_labels'] as topic_labels
    SET m.topic = topic_labels[m.topic_id + 1]
//Load MR geo data
LOAD CSV WITH HEADERS FROM 'file:///MRgeodata.csv' AS row 
WITH row
    WHERE row IS NOT NULL
WITH row
    MERGE(s: Sites {uid: TRIM(row.`Site Name`) + TRIM(row.`Event Name`) + TRIM(row.Lat) + TRIM(row.Long) + TRIM(row.Date)})
        SET
            s.name = TRIM(row.`Site Name`),
            s.event = TRIM(row.`Event Name`),
            s.lat = TRIM(row.Lat),
            s.long = TRIM(row.Long),
            s.date = TRIM(row.Date),
            s.state = TRIM(row.State),
            s.county = TRIM(row.County),
            s.category = TRIM(row.Category),
            s.protocol = TRIM(row.Protocol),
            s.protocol_url = TRIM(row.`Protocol Url`),
            s.study_plan = TRIM(row.`Study Plan`),
            s.study_plan_url = TRIM(row.`Study Plan Url`),
            s.program = TRIM(row.Program),
            s.program_url = TRIM(row.`Program Url`),
            s.organization = TRIM(row.Organization),
            s.organization_url = TRIM(row.`Organization Url`),
            s.url = TRIM(row.URL),
            s.data_provider = TRIM(row.`Data Provider`)

//Load categories data
LOAD CSV WITH HEADERS FROM 'file:///CATEGORIES-AllCategories.csv' AS row
WITH row
    WHERE row IS NOT NULL
WITH row
    MERGE (n:Categories {category_id: TRIM(row.`Category ID`)})
        SET
            n.subject = TRIM(row.Subject),
            n.title = TRIM(row.`Category Name`),
            n.category_description = TRIM(row.`Category Description`),
            n.no_of_subcategories = TRIM(row.`# Subcategories`)

// Load Manually subject data
CREATE 
(s1: Subjects {name: 'Biological', no_of_categories: 10}), 
(s2: Subjects {name: 'Chemical', no_of_categories: 2}), 
(s3: Subjects {name: 'Economic', no_of_categories: 0}), 
(s4: Subjects {name: 'General', no_of_categories: 3}), 
(s5: Subjects {name: 'Physical', no_of_categories: 8}), 
(s6: Subjects {name: 'Social', no_of_categories: 0})

//Load methods data
LOAD CSV WITH HEADERS FROM 'file:///methods.tsv' AS row FIELDTERMINATOR '\t'
WITH row
    WHERE row IS NOT NULL AND row.url IS NOT NULL
WITH row
    MERGE (n:Methods {uid: TRIM(row.url)})
        SET
            n.html = TRIM(row.html),
            n.version = TRIM(row.version),
            n.abstractText = TRIM(row.abstractText),
            n.equipment = TRIM(row.equipment),
            n.instructions = TRIM(row.instructions),
            n.citation = TRIM(row.citation),
            n.images = TRIM(row.images),
            n.protocols = TRIM(row.protocols),
            n.customizedMethods = TRIM(row.customizedMethods),
            n.ownerName = TRIM(row.ownerName),
            n.ownerEmail = TRIM(row.ownerEmail),
            n.id = TRIM(row.id),
            n.type = TRIM(row.type),
            n.status = TRIM(row.status),
            n.title = TRIM(row.title),
            n.lastUpdated = TRIM(row.lastUpdated);

//Load metrics data
LOAD CSV WITH HEADERS FROM 'file:///METRICS-AllMetrics.csv' AS row
WITH row
    WHERE row IS NOT NULL
WITH row
    MERGE (n:Metrics {uid: TRIM(row.`Metric Subcategory ID`)})
        SET
            n.category = TRIM(row.Category),
            n.title = TRIM(row.Subcategory),
            n.description = TRIM(row.Description),
            n.keywords = TRIM(row.Keywords),
            n.no_of_protocols = TRIM(row.`# Protocols`),
            n.subcategory_foci = TRIM(row.`Subcategory Foci`),
            n.most_recent_cmtr = TRIM(row.`Most Recent Commenter`),
            n.no_of_cmt = TRIM(row.`Count of Comments/Replies`)

//Load programs and organization data
LOAD CSV WITH HEADERS FROM 'file:///programs.tsv' AS row FIELDTERMINATOR '\t'
WITH row
    WHERE row IS NOT NULL AND row.url IS NOT NULL
WITH row
    MERGE (n:Programs {uid: TRIM(row.url)})
        SET
            n.protocols = TRIM(row.protocols),
            n.projects = TRIM(row.projects),
            n.organizations = TRIM(row.organizations),
            n.id = TRIM(row.id),
            n.name = TRIM(row.name),
            n.citation = TRIM(row.citation),
            n.url = TRIM(row.url),
            n.primaryContactName = TRIM(row.primaryContactName),
            n.primaryContactEmail = TRIM(row.primaryContactEmail),
            n.link_to = TRIM(row.link_to),
            n.link_to_org = TRIM(row.link_to_org)
    MERGE (o:Organizations {uid:row.organizations})
        SET o.name = TRIM(row.organization);

//Load protocols data
LOAD CSV WITH HEADERS FROM 'file:///protocols.tsv' AS row FIELDTERMINATOR '\t'
WITH row
    WHERE row IS NOT NULL AND row.url IS NOT NULL
WITH row
    MERGE (n:Protocols {uid: TRIM(row.url)})
        SET
            n.version = TRIM(row.version),
            n.html = TRIM(row.html),
            n.background = TRIM(row.background),
            n.programUrl = TRIM(row.programUrl),
            n.objectives = TRIM(row.objectives),
            n.assumptions = TRIM(row.assumptions),
            n.methods = TRIM(row.methods),
            n.metric_title = TRIM(row.metric_title),
            n.metric_category = TRIM(row.metric_category),
            n.metric_subcategory = TRIM(row.metric_subcategory),
            n.tags = TRIM(row.tags),
            n.metrics = TRIM(row.metrics),
            n.citation = TRIM(row.citation),
            n.images = TRIM(row.images),
            n.ownerName = TRIM(row.ownerName),
            n.ownerEmail = TRIM(row.ownerEmail),
            n.id = TRIM(row.id),
            n.literatureCited = TRIM(row.literatureCited),
            n.status = TRIM(row.status),
            n.url = TRIM(row.url),
            n.title = TRIM(row.title),
            n.lastUpdated = TRIM(row.lastUpdated),
            n.link_to = TRIM(row.link_to);

//Load protocols golden data
LOAD CSV WITH HEADERS FROM 'file:///protocol_golden.tsv' AS row FIELDTERMINATOR '\t'
WITH row
    WHERE row IS NOT NULL AND row.url IS NOT NULL
WITH row
    MERGE (n:Protocols {uid: TRIM(row.url)})
        SET
            n.version = TRIM(row.version),
            n.html = TRIM(row.html),
            n.background = TRIM(row.background),
            n.programUrl = TRIM(row.programUrl),
            n.objectives = TRIM(row.objectives),
            n.assumptions = TRIM(row.assumptions),
            n.methods = TRIM(row.methods),
            n.metric_title = TRIM(row.metric_title),
            n.metric_category = TRIM(row.metric_category),
            n.metric_subcategory = TRIM(row.metric_subcategory),
            n.tags = TRIM(row.tags),
            n.metrics = TRIM(row.metrics),
            n.citation = TRIM(row.citation),
            n.images = TRIM(row.images),
            n.ownerName = TRIM(row.ownerName),
            n.ownerEmail = TRIM(row.ownerEmail),
            n.id = TRIM(row.id),
            n.literatureCited = TRIM(row.literatureCited),
            n.status = TRIM(row.status),
            n.url = TRIM(row.url),
            n.title = TRIM(row.title),
            n.lastUpdated = TRIM(row.lastUpdated),
            n.link_to = TRIM(row.link_to);

//Load Subcategory Focus data
LOAD CSV WITH HEADERS FROM 'file:///SUBCATEGORYFOCUSOPTIONS-AllSubcategoryFocusOptions.csv' AS row
WITH row
    WHERE row IS NOT NULL
WITH row
    MERGE (n:Subcategory_Focus {uid: TRIM(row.`Subcategory Focus Option ID`)})
        SET
            n.subcategory_foci = TRIM(row.`Subcategory Focus`),
            n.title = TRIM(row.`Subcategory Focus Option`),
            n.description = TRIM(row.Description),
            n.keywords = TRIM(row.Keywords)

//Load synthetic golden keywords data
LOAD CSV WITH HEADERS FROM 'file:///Synthetic_golden_data.tsv' AS row FIELDTERMINATOR '\t'
WITH row
    WHERE row IS NOT NULL
WITH row
    UNWIND SPLIT(row.Keywords, ', ') as keywords
WITH row, keywords
    MERGE (k: Keywords {uid: keywords})
        SET
            k.title = keywords
WITH k
    MATCH (p: Protocols)
        WHERE k.title in p.keywords
        MERGE (p)-[:CONTAINS]->(k)

//Load synthetic golden protocols data
LOAD CSV WITH HEADERS FROM 'file:///Synthetic_golden_data.tsv' AS row FIELDTERMINATOR '\t'
WITH row
    WHERE row IS NOT NULL
WITH row
    MERGE (n:Protocols {uid: TRIM(row.Protocol_ID)})
        SET
            n.pid = TRIM(row.Protocol_ID),
            n.title = TRIM(row.Protocol_Name),
            n.keywords = TRIM(row.Keywords),
            n.background = TRIM(row.Background),
            n.values = TRIM(row.Values),
            n.problem_statement = TRIM(row.Problem_Statement),
            n.desired_outcomes = TRIM(row.Desired_Outcomes),
            n.description = TRIM(row.Description),
            n.objectives = TRIM(row.Objectives),
            n.target = TRIM(row.Target),
            n.method = TRIM(row.Method),
            n.metrics = TRIM(row.Metrics),
            n.tags = TRIM(row.Tags);

//Load synthetic golden tags data
LOAD CSV WITH HEADERS FROM 'file:///Synthetic_golden_data.tsv' AS row FIELDTERMINATOR '\t'
WITH row
    WHERE row IS NOT NULL
WITH row
    UNWIND SPLIT(row.Tags, ', ') as tags
WITH row, tags
    MERGE (k: Tags {uid: tags})
        SET
            k.title = tags

// Create keywords data from metrics
MATCH(m:Metrics)
WITH m
    UNWIND(SPLIT(m.keywords, ',')) as keyword
WITH m, keyword
    MERGE (k:Keywords {title: keyword})

// Create keywords data from subcategory_focus
MATCH (sf:Subcategory_Focus)
WITH sf
    UNWIND(SPLIT(sf.keywords, ',')) as keyword
WITH sf, keyword
    MERGE (k:Keywords {title: keyword})

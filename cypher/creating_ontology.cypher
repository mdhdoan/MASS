CREATE
// SITE and its subcategories
(:Category {name: 'SITE'})-[:HAS_CATEGORY]->(:Category {name: 'Habitat', definition: 'The natural environment where an organism lives, including both biotic (living) and abiotic (non-living) components.'}),
(:Category {name: 'Habitat'})-[:HAS_CATEGORY]->(:Category {name: 'Physical', definition: 'Attributes of the habitat related to its physical properties.'}),
(:Category {name: 'Physical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Flow', definition: 'Movement and distribution of water within the habitat.'}),
(:Category {name: 'Physical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Temperature', definition: 'Heat levels within the habitat.'}),
(:Category {name: 'Physical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Structure', definition: 'Physical formation and arrangement of the habitat.'}),
(:Category {name: 'Physical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Sediment Composition', definition: 'Characteristics and types of sediment present in the habitat.'}),
(:Category {name: 'Physical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Hydraulic Connectivity', definition: 'Degree to which water bodies within the habitat are connected.'}),

(:Category {name: 'Habitat'})-[:HAS_CATEGORY]->(:Category {name: 'Ecological', definition: 'Attributes related to the living organisms and their interactions within the habitat.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Population', definition: 'Study of groups of organisms of the same species within the habitat.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Environmental Disturbance Monitoring', definition: 'Tracking and assessing environmental changes that impact the habitat.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Reproductive Success', definition: 'Studying reproduction rates and success of species in the habitat.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Food Webs', definition: 'Interactions between different organisms based on their feeding relationships.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Vegetation or Plant Life', definition: 'Ecological aspects related to plant species within the habitat.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Behavioral Studies', definition: 'Monitoring and analyzing animal behavior within the habitat.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Species Interactions', definition: 'Interactions among different species within the habitat.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Habitat Fragmentation', definition: 'Division of habitats into smaller, isolated patches, often due to human activities.'}),

(:Category {name: 'Habitat'})-[:HAS_CATEGORY]->(:Category {name: 'Chemical', definition: 'Attributes related to the chemical composition and processes within the habitat.'}),
(:Category {name: 'Chemical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Constituents', definition: 'Chemical components present in the habitat.'}),
(:Category {name: 'Chemical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Pollutant', definition: 'Substances contaminating the habitat, often due to human activities.'}),
(:Category {name: 'Chemical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Nutrient Levels', definition: 'Amounts and types of nutrients present in the habitat.'}),
(:Category {name: 'Chemical'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Water Quality', definition: 'Overall quality of water in the habitat, including various chemical parameters.'}),

// METHODS and its subcategories
(:Category {name: 'METHODS'})-[:HAS_CATEGORY]->(:Category {name: 'Data Collection', definition: 'Techniques and processes used to gather information from the environment.'}),
(:Category {name: 'Data Collection'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Sampling Design', definition: 'Planning and structuring of data collection methods to ensure accurate and representative results.'}),
(:Category {name: 'Data Collection'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Field Methods', definition: 'Techniques used in the field for direct data collection.'}),
(:Category {name: 'Data Collection'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Monitoring Techniques', definition: 'Methods used to continuously observe and record environmental or biological parameters.'}),
(:Category {name: 'Data Collection'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Remote Sensing', definition: 'Collection of data from a distance, typically using satellite or aerial imagery.'}),
(:Category {name: 'Data Collection'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Acoustic Monitoring', definition: 'Use of sound to monitor animal presence, movement, and behavior.'}),
(:Category {name: 'Data Collection'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Survey Methods', definition: 'Methods for estimating populations or distributions through systematic surveys.'}),

(:Category {name: 'METHODS'})-[:HAS_CATEGORY]->(:Category {name: 'Data Analysis', definition: 'Processes used to interpret, summarize, and draw conclusions from collected data.'}),
(:Category {name: 'Data Analysis'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Statistical Analysis', definition: 'Application of statistical methods to understand relationships and trends in the data.'}),
(:Category {name: 'Data Analysis'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Descriptive Statistics & Confidence Intervals', definition: 'Techniques for summarizing data and estimating the reliability of those summaries.'}),
(:Category {name: 'Data Analysis'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Spatial Analysis', definition: 'Analyzing geographical patterns and distributions in the data.'}),
(:Category {name: 'Data Analysis'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Temporal Analysis', definition: 'Studying changes in data over time.'}),
(:Category {name: 'Data Analysis'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Population Estimation', definition: 'Techniques for estimating the size and structure of populations within the habitat.'}),

// FISHERIES MANAGEMENT and its subcategories
(:Category {name: 'FISHERIES MANAGEMENT'})-[:HAS_CATEGORY]->(:Category {name: 'Population Estimation', definition: 'Methods used to determine the size and dynamics of fish populations.'}),
(:Category {name: 'Population Estimation'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Mark-Recapture', definition: 'A method of estimating population size by capturing, marking, and releasing individuals.'}),
(:Category {name: 'Population Estimation'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Survey Methods', definition: 'Techniques used to estimate population sizes through observation and sampling.'}),

(:Category {name: 'FISHERIES MANAGEMENT'})-[:HAS_CATEGORY]->(:Category {name: 'Ecological', definition: 'Studies and practices related to the management of fish populations and their habitats.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Tagging and Tracking', definition: 'Techniques for tagging and tracking the movement and behavior of fish.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Non-lethal Sampling', definition: 'Methods of collecting biological samples from fish without causing harm.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Genetics', definition: 'Study of genetic diversity and inheritance within fish populations.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Biodiversity', definition: 'Study of the variety of life within fish populations and their ecosystems.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Reproductive Biology', definition: 'Study of the reproductive systems, cycles, and success of fish.'}),
(:Category {name: 'Ecological'})-[:HAS_SUBCATEGORY]->(:Category {name: 'Physiology', definition: 'Study of the physical and biochemical functions of fish.'});

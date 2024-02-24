// Creating in memory graph
CALL gds.graph.project(
    'myGraph',
    ['Protocols','Categories'],
    {
        TAGGED: {
            orientation: 'NATURAL'
        }
    }
)

//Remove graph
CALL gds.graph.drop('myGraph') YIELD graphName

// Stream louvain to check communityID
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId, intermediateCommunityIds
RETURN gds.util.asNode(nodeId).title AS title, communityId
ORDER BY communityId ASC

// Stream louvain to check communityID
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId, intermediateCommunityIds
RETURN gds.util.asNode(nodeId).title AS title, communityId
ORDER BY communityId ASC

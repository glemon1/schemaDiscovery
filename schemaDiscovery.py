from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLWrapper2

sparql = SPARQLWrapper("http://83.212.77.24:8890/sparql/")

dataSet = "Conference"#Conference"#"DBpedia"BNF
#1. all trilets
sparql.setQuery("""
    select ?s ?p ?o 
    from <http://localhost:8890/""" + dataSet +""">
    where { ?s ?p ?o}
    order by ?s ?p ?o
""")
sparql.setReturnFormat(JSON)
tripletsAll = sparql.query().convert()

#2. machine learning input layer: all predicates (properties) except type, ordered. Based on predicates of each subject we conclude it s type, ordered
sparql.setQuery("""
SELECT distinct  ?predicate
from <http://localhost:8890/""" + dataSet +""">
WHERE
{
  ?subject  ?predicate ?object.
FILTER (?predicate!= <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
}   
order by ?predicate
""")
sparql.setReturnFormat(JSON)
inputNN = sparql.query().convert()

#3. types (NN output), machine learning output layer: all objects with predicate ‘type’ ordered. All types ordered. They are the outputs plus one for the ones not classified which will be processed in second phase
sparql.setQuery("""
    SELECT distinct ?o
    from <http://localhost:8890/""" + dataSet +""">
    WHERE
    {
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o.
    }   
    order by ?o
""")
sparql.setReturnFormat(JSON)
outputNN = sparql.query().convert()

#4. all subjects (instances)
sparql.setQuery("""
    SELECT distinct ?s
    from <http://localhost:8890/""" + dataSet +""">
    WHERE
    {
    ?s ?p ?o.
    }   
    order by ?s
""")
sparql.setReturnFormat(JSON)
instancesAll = sparql.query().convert()

#5. all instances (subjects) having type property
sparql.setQuery("""
    SELECT distinct ?s
    from <http://localhost:8890/""" + dataSet +""">
    WHERE
    {
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o.
    }   
    order by ?s
""")
sparql.setReturnFormat(JSON)
insstancesWithKnownTypes = sparql.query().convert()


found = 'false'
instancesUnknown = [{}]
tripletsAll
inputNN
outputNN
instancesAll
insstancesWithKnownTypes

# for triplet in tripletsAll["results"]["bindings"]:
#     if tripletsAll['s']['value'] not in insstancesWithKnownTypes['s']:
#         print (triplet['s']['value'])

for instance in instancesAll["results"]["bindings"]:
    for knownInstance in insstancesWithKnownTypes["results"]["bindings"]:
        if instance['s']['value'] == knownInstance['s']['value']:
            found = 'true'
            break
    if found == 'true': 
        found = 'false'
    else:
        instancesUnknown.append(instance)
        #print('unknown ' + instance['s']['value'])
instancesUnknown   
# for type in outputNN["results"]["bindings"]:
#     print (type['o']['value'])


#     queryString = "SELECT ?subj ?o ?opt WHERE { ?subj <http://a.b.c> ?o. OPTIONAL { ?subj ˓→<http://d.e.f> ?opt }}"
# sparql = SPARQLWrapper2("http://example.org/sparql")
# sparql.setQuery(queryString)
# try :
# ret = sparql.query()
# print ret.variables # this is an array consisting of "subj", "o", "opt"
# if (u"subj",u"prop",u"opt") in ret :
# # there is at least one binding covering the optional "opt", too
# bindings = ret[u"subj",u"o",u"opt"]
# # bindings is an array of dictionaries with the full bindings
# for b in bindings :
# subj = b[u"subj"].value
# o = b[u"o"].value
# opt = b[u"opt"].value
# # do something nice with subj, o, and opt
# # another way of accessing to values for a single variable:
# # take all the bindings of the "subj"
# subjbind = ret.getValues(u"subj") # an array of Value instances
# ...
# except:
# deal_with_the_exception()
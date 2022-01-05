from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLWrapper2

sparql = SPARQLWrapper("http://83.212.77.24:8890/sparql/")

#dataSet = "Conference"
#all trilets
sparql.setQuery("""
    select ?s ?p ?o 
    from <http://localhost:8890/Conference>
    where { ?s ?p ?o}
    order by ?s ?p ?o
""")
sparql.setReturnFormat(JSON)
tripletsAll = sparql.query().convert()

#all subjects
sparql.setQuery("""
    SELECT distinct ?s
    from <http://localhost:8890/Conference>
    WHERE
    {
    ?s ?p ?o.
    }   
    order by ?s
""")
sparql.setReturnFormat(JSON)
subjectsAll = sparql.query().convert()
#types (NN output) 
sparql.setQuery("""
    SELECT distinct ?o
    from <http://localhost:8890/Conference>
    WHERE
    {
    ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o.
    }   
    order by ?o
""")
sparql.setReturnFormat(JSON)
types = sparql.query().convert()


for type in types["results"]["bindings"]:
    print(type)



    # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    # http://localhost:8890/Conference
    # SELECT *
    # WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }

    # for result in results["results"]["bindings"]:
    # print(result["label"]["value"])


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
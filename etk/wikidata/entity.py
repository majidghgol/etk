from etk.knowledge_graph.subject import Subject
from etk.knowledge_graph.node import URI, Literal
from etk.wikidata.statement import Statement, Rank
from etk.wikidata.value import Item, Property, Datatype
from collections import defaultdict


change_recorder = set()


def serialize_change_record(fp):
    fp.writelines('{}\t{}\n'.format(node, prop) for node, prop in change_recorder)


class Entity(Subject):
    def __init__(self, node, creator):
        super().__init__(URI('wd:'+node))
        self.node_id = node
        self.creator = URI(creator) if creator else None

    def add_label(self, s: str, lang='en'):
        literal = Literal(s, lang=lang)
        self.add_property(URI('rdfs:label'), literal)
        self.add_property(URI('schema:name'), literal)
        self.add_property(URI('skos:prefLabel'), literal)

    def add_alias(self, s: str, lang='en'):
        self.add_property(URI('skos:altLabel'), Literal(s, lang=lang))

    def add_description(self, s: str, lang='en'):
        self.add_property(URI('schema:description'), Literal(s, lang=lang))

    def add_statement(self, p: str, v, rank=Rank.Normal):
        change_recorder.add((self.node_id, p))
        statement = Statement(self.node_id, rank)
        statement.add_value(p, v)
        statement.add_property(URI('http://www.isi.edu/etk/createdBy'), self.creator)
        self.add_property(URI('p:'+p), statement)
        return statement


class WDItem(Entity, Item):
    def __init__(self, s: str, creator='http://www.isi.edu/datamart'):
        Entity.__init__(self, s, creator)
        Item.__init__(self, s)
        self.add_property(URI('rdf:type'), URI('wikibase:Item'))


class WDProperty(Entity, Property):
    def __init__(self, s: str, property_type, creator='http://www.isi.edu/datamart'):
        Entity.__init__(self, s, creator)
        Property.__init__(self, s)
        self.add_property(URI('rdf:type'), URI('wikibase:Property'))
        type_uri = property_type if not isinstance(property_type, Datatype) else Datatype(property_type)
        self.add_property(URI('wikibase:propertyType'), type_uri.type)

        self.add_property(URI('wikibase:directClaim'), URI('wdt:'+s))
        self.add_property(URI('wikibase:directClaimNormalized'), URI('wdtn:'+s))
        self.add_property(URI('wikibase:claim'), URI('p:'+s))
        self.add_property(URI('wikibase:statementProperty'), URI('ps:'+s))
        self.add_property(URI('wikibase:statementValue'), URI('psv:'+s))
        self.add_property(URI('wikibase:statementValueNormalized'), URI('psn:'+s))
        self.add_property(URI('wikibase:qualifier'), URI('pq:'+s))
        self.add_property(URI('wikibase:qualifierValue'), URI('pqv:'+s))
        self.add_property(URI('wikibase:qualifierValueNormalized'), URI('pqn:'+s))
        self.add_property(URI('wikibase:reference'), URI('pr:'+s))
        self.add_property(URI('wikibase:referenceValue'), URI('prv:'+s))
        self.add_property(URI('wikibase:referenceValueNormalized'), URI('prn:'+s))
        self.add_property(URI('wikibase:novalue'), URI('wdno:'+s))

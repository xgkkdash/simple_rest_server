from mongoengine import Document, StringField
from model.kvpair import KvPair


class KvpairDocument(Document):
    key = StringField(required=True)
    value = StringField(required=True)
    meta = {
        'collection': 'kvpairs',
        'indexes': ['key'],
    }

    @classmethod
    def from_kvpair(cls, kvpair: KvPair):
        return cls(**vars(kvpair))

    def to_kvpair(self) -> KvPair:
        doc_dict = self.to_mongo().to_dict()
        doc_dict.pop('_id')
        return KvPair(**doc_dict)

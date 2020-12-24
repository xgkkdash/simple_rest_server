import mongoengine
from mongoengine import DoesNotExist

from database.KvpairDocument import KvpairDocument


class MyMongoDB:
    def __init__(self, db_name, db_url):
        self.db_connection = mongoengine.connect(db=db_name, host=db_url)

    def save_kvpair(self, kvpair):
        doc = KvpairDocument.from_kvpair(kvpair)
        return doc.save()

    def get_kvpair(self, **kwargs):
        try:
            doc = KvpairDocument.objects.get(**kwargs)
            return doc.to_kvpair()
        except DoesNotExist:
            return None

    def remove_kvpair(self, **kwargs):
        doc = KvpairDocument.objects.get(**kwargs)
        doc.delete()

    def update_kvpair(self, key, new_value):
        try:
            doc = KvpairDocument.objects.get(key=key)
            return doc.update(value=new_value)
        except DoesNotExist:
            return None

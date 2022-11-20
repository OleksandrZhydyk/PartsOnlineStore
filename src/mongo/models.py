from mongoengine import (Document, EmailField, EmbeddedDocument,
                         EmbeddedDocumentField, FloatField, ListField,
                         StringField)


class Basket(EmbeddedDocument):
    part = StringField(max_length=255)
    price = FloatField()


class Customer(Document):
    name = StringField(max_length=255)
    email = EmailField()
    baskets = ListField(EmbeddedDocumentField(Basket))

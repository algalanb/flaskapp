import datetime
from flask import url_for
from app import db

class ExtraIngredient(db.EmbeddedDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	ingredient = db.StringField(verbose_name="Extra ingredient", required=True)
	ing_price = db.DecimalField(min_value=0,max_value=None,precision=2, required=True)

class Plate(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	name = db.StringField(max_length=255, required=True)
	description = db.StringField(max_length=511, required=True)
	price = db.DecimalField(min_value=0,max_value=None,precision=2, required=True)
	image = db.ImageField(size=(800, 600, True))
	allergies = db.StringField(max_length=255) 
	extra_ingredients = db.ListField(db.EmbeddedDocumentField('ExtraIngredient'))
	slug = db.StringField(max_length=255, required=True)

	def get_absolute_url(self):
        	return url_for('plate', kwargs={"slug": self.slug})

	def __unicode__(self):
        	return self.name

	meta = {
        	'allow_inheritance': True,
        	'indexes': ['-created_at', 'slug'],
        	'ordering': ['-created_at']
	}

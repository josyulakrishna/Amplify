# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime, random, feedparser
from collections import defaultdict
import httplib, urllib, json
from bs4 import BeautifulSoup
import html5lib
from html5lib import sanitizer
from html5lib import treebuilders
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
import json

gravatar = local_import("gravatar")
Gravatar = gravatar.Gravatar

db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
response.generic_patterns = ['*'] if request.is_local else []
from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()
auth.define_tables(username=True, signature=False)
auth.define_tables(username=True)
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False
auth.settings.register_next = URL(c='default',f='interests')
auth.settings.login_next = URL(c='news',f='social') 

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('user_interests', Field('user_id',db.auth_user), Field("Science",'boolean'),Field("Arts",'boolean'), Field("BusinessEconomy",'boolean'), Field("ComputersTechnology",'boolean'), Field("Health",'boolean'), Field("HomeDomesticLife",'boolean'), Field("News",'boolean'), Field("RecreationActivities",'boolean'), Field("ReferenceEducation",'boolean'), Field("Shopping",'boolean'), Field("Society",'boolean'), Field("Sports",'boolean') )

#db.define_table('user_likes', Field('user_id',db.auth_user), Field("Science",'integer'),Field("Arts",'integer'), Field("BusinessEconomy",'integer'), Field("ComputersTechnology",'integer'), Field("Health",'integer'), Field("HomeDomesticLife",'integer'), Field("News",'integer'), Field("RecreationActivities",'integer'), Field("ReferenceEducation",'integer'), Field("Shopping",'integer'), Field("Society",'integer'), Field("Sports",'integer') )

db.define_table('user_post', Field('posted_by_user', db.auth_user), Field('liked_by_user','list:integer'), Field('topic'), Field('url'), Field('description'))

#db.define_table( 'model_posts', Field('link'), Field('description'), Field('topic') )

db.define_table('user_clusters', Field('user_id',db.auth_user),Field('cluster_id'))

db.define_table('knnRef', Field('cluster_id'),Field("Science",'double'),Field("Arts",'double'), Field("BusinessEconomy",'double'), Field("ComputersTechnology",'double'), Field("Health",'double'), Field("HomeDomesticLife",'double'), Field("News",'double'), Field("RecreationActivities",'double'), Field("ReferenceEducation",'double'), Field("Shopping",'double'), Field("Society",'double'), Field("Sports",'double')) 

total = len(db(db.auth_user.id>0).select())

#print(total)
#db.user_interests._after_insert.append(make_clusters)
#db.user_interests._after_update.append(make_clusters)
#db(db.user_post.topic=="ComputersTechonology").update(topic="ComputersTechnology")
allCategories = ['Science', 'Arts', 'Bussiness and Economy', 'Computers and Technology', 'Health', 'Home and Domestic Life', 'News','Recreation Activities', 'Reference Education', 'Shopping', 'Society', 'Sports']

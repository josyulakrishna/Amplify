# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()

    """
    #drone_posts()
    #create_drones()
    #create_news()
    #make_clusters()
    
    if auth.is_logged_in():
        name  = db.auth_user[auth.user_id].first_name
    else:
        name  = "Guest"
    return locals()

@auth.requires_login()
def userprofile():
     print "userprofile", datetime.datetime.now()
     user = db.auth_user(db.auth_user.username==request.args(0)) or redirect(URL('error'))
     print user
     print "getting username"
     name=user.first_name+" "+user.last_name
     if name=="":
         name = user['username']
     posts = db(db.user_post.posted_by_user == user).select()
#     print posts
     return locals()

def news():
    redirect(URL(c="news",f="social"))
    
def user():
    if request.args(0) == 'profile':
        response.view = 'default/profile.html'
    if request.args(0) == 'register':
        for field in ['first_name', 'last_name', 'email']:
            db.auth_user[field].readable = db.auth_user[field].writable = False
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def profile():
    return locals()

@auth.requires_login()    
def interests():
    row = db(db.user_interests.user_id == auth.user_id).select()
    field_list = ['Science', 'Arts', 'Bussiness and Economy', 'Computers and Techonology', 'Health', 'Home and Domestic Life', 'News','Recreation Activities', 'Reference Education', 'Shopping', 'Society', 'Sports']
    filled_interests = dict()
    if row:
        for i,word in enumerate(db.user_interests.fields[2:]):
            filled_interests[field_list[i]] = row[0][word]
        print filled_interests
    else:
        noInterest = 'none'
    return locals()

def set_interests():
    print "in set interest"
    print(auth.user_id)
    field_list = ['Science', 'Arts', 'Bussiness and Economy', 'Computers and Techonology', 'Health', 'Home and Domestic Life', 'News','Recreation Activities', 'Reference Education', 'Shopping', 'Society', 'Sports']
    for interest in request.vars.values()[0]:
        if interest in field_list:
            field_list[field_list.index(interest)] = True
    for index,interest in enumerate(field_list):
        if interest!=True:
            field_list[index] = False
    fieldDict = dict(zip(db.user_interests.fields[2:], field_list))
    fieldDict['user_id']  = auth.user_id
    print fieldDict
    row = db(db.user_interests.user_id==auth.user_id).select()
    print row
    row = db(db.user_interests.user_id==auth.user_id).count()
    print row
    if row:
        print "if"
        db(db.user_interests.user_id==auth.user_id).update(**fieldDict)
        if db(db.user_clusters.id > 0).count() > 100: 
            print "calling knn select"
            knnSelect(auth.user_id)
        else:
            print "calling make_clusters"
            make_clusters()
    else:
        print "in else"
        db.user_interests.insert(**fieldDict)
        if db(db.user_clusters.id > 0).count() > 100: 
            print "calling knn select"
            knnSelect(auth.user_id)
        else:
            print "calling make_clusters"
            make_clusters()

    
    #db.user_interests.insert(user_id = auth.user_id , *field_list)
    return True

#Getting posts for the user
def get_posts(): 
    #user id of the user
     userid = auth.user_id
     row = db(db.user_clusters.user_id == userid).select().first()
     clusterid =  int(row.cluster_id)
     #getting users in the cluster
     rows = db(db.user_clusters.cluster_id == clusterid).select()

     #users in the cluster
     users = []
     for row in rows: 
        users.append(row.user_id)
      
    #getting the user posts
     posts ={}
     for user in users: 
        for post in db(db.user_post.posted_by_user == user).select(): # selecting the user posts
            posts.setdefault(user, []).append((post.description, post.url, post.liked_by_user))
     return posts

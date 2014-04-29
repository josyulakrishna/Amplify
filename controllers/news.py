# coding: utf8
# try something like
import urllib2
import json
from bs4 import BeautifulSoup
@auth.requires_login()
def social(): 
    print db(db.user_interests.user_id==auth.user_id).select()
    if db(db.user_interests.user_id==auth.user_id).select():
        fill = True
        posts = get_posts()
        return locals()
    else:
        fill = False
        return locals()    

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
     idEmailUsername = []
     for user in users:      
         for row in db(db.auth_user.id == user).select():
             idEmailUsername.append((row.id, row.email, row.username))
    #getting the user posts
     posts ={}
     for user in idEmailUsername: 
        for post in db(db.user_post.posted_by_user == user[0]).select(): # selecting the user posts
            posts.setdefault(user, []).append((post.description, post.url, post.liked_by_user,post.topic,post.id))
     return posts
     
def fetchNews(): 
    category = request.vars.category
    print category
    category = category.replace("and",'').replace(" ",'')
    print category
    news = db(db.user_post.topic==category).select()
    #print news.url
    #print new.description

#ajax method at new/social.html
def post_news(): 
    description,link,category =  request.vars['des'], request.vars['link'],request.vars['category']
    val =  link.startswith("http://www.")
    if not val:
        link = ''.join(("http://www." ,link))
        print link
    if description=="":
        print "getting description"
        opener = urllib2.build_opener()
        external_sites_html = opener.open(link).read()
        soup = BeautifulSoup(external_sites_html)
        title = soup.title.string
        description= title
    print "out of control"
    print [ category, link, description]
    topicDeUrl = dict(zip( db.user_post.fields[3:], [ category, link, description] ))
    print topicDeUrl, dict(zip(['posted_by_user','url',],[auth.user_id,link]))
    db.user_post.insert(posted_by_user=auth.user_id, **topicDeUrl)
    print "done!"


def like():
    print "called like" ,datetime.datetime.now()
    row = db(db.user_post.id == request.vars.id).select()
    likedUsers = row[0].liked_by_user
    if likedUsers:
        likedUsers = map(int, likedUsers)
        if int(request.vars.userid) in likedUsers:
            print "remove"
            likedUsers.remove(int(request.vars.userid))
            db(db.user_post.id == request.vars.id).update(**{'liked_by_user':likedUsers})
            return response.json(json.dumps({"like":"unlike"}))
        else: 
            print "append else if"
            likedUsers.append(int(request.vars.userid))
            print likedUsers
            db(db.user_post.id == request.vars.id).update(**{'liked_by_user':likedUsers})
            return response.json(json.dumps({"like":"like"}))
    else:
        print "append else"
        likedUsers = [] 
        likedUsers.append(int(request.vars.userid))
        print request.vars.userid, request.vars.id
        db(db.user_post.id == request.vars.id).update(**{'liked_by_user':likedUsers})
        return response.json(json.dumps({"like":"like"}))

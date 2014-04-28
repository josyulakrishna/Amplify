# coding: utf8
# try something like
import urllib2
from bs4 import BeautifulSoup
@auth.requires_login()
def social(): 
    print db(db.user_interests.user_id==auth.user_id).select()
    if db(db.user_interests.user_id==auth.user_id).select():
        fill = True
        return locals()
    else:
        fill = False
        return locals()    

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

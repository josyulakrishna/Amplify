# coding: utf8
# coding: utf8
#from __future__ import print_function
import datetime, random, feedparser
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn import neighbors
import json
import random

total = len(db(db.auth_user.id>0).select())
print total

def make_clusters():
    if total<=10:
        clusters = 2
    elif total>10 and total<=50:
        clusters = 5
    elif total>50 and total<101:
        clusters = 10
    else:
        return 0
    aggregate = []
    user_index = []
    i=0
    db(db.user_clusters.id>0).delete()
    for row in db(db.user_interests).select():
        i+=1
        user_index.append(int(row.user_id))
        empty = []
        for topic in db.user_interests.fields[2:]:
            empty.append(row[topic])
        aggregate.append(empty)
        print "aggregate ",aggregate
    aggregate = np.array(aggregate)
    t_aggregate = np.zeros((i,12))
    t_aggregate[aggregate] = 1
    print "t_aggregate ",t_aggregate
    kmeans = KMeans(n_clusters=clusters,init='random',n_jobs=1,n_init=20,max_iter=500)
    d = kmeans.fit_predict(t_aggregate)
    d = d.tolist()
    print user_index
    print d
    for j in range(len(d)):
        pass
        db.user_clusters.insert(user_id = user_index[j], cluster_id = d[j] )
    #knnMake()
    return 0

def knnMake():
    db(db.knnRef.id>0).delete()
    clusterId = []
    userId = []
    clusterUser={}

    #get the rows for each cluster
    rows = db(db.user_clusters).select()
    for row in rows:
        clusterId.append(row.cluster_id)
    clusterId = set(clusterId)
    print clusterId
    for cluster in clusterId:
        rows = db(db.user_clusters.cluster_id==cluster).select() #get rows where clusterid=clusterid
        for row in rows:
            clusterUser.setdefault(cluster,[]).append(row.user_id)
    print "finished getting rows"

    #get users interests
    clusterInterests = {}
    temp = []
    for cluster in clusterId:
        print cluster, datetime.datetime.now()
        for v in clusterUser[cluster]:
            rows = db(db.user_interests.user_id == v).select(*db.user_interests.fields[2:])
            for row in rows:
                for f in db.user_interests.fields[2:]:
                    temp.append(row[f])
                clusterInterests.setdefault(cluster,[]).append(temp)
                temp = []
        print clusterInterests
        print "finished getting clusterInterests"

    #converting the arrays to numpy format with zeros and ones
    zeros = np.zeros(len(db.user_interests.fields[2:]))
    temp = [] #for holding the user interests
    for k in clusterInterests.keys():
       tArrayUserInterests =  np.array(clusterInterests[k])
       T,F = tArrayUserInterests == 'T', tArrayUserInterests == 'F'
       tArrayUserInterests[T] = 1.0
       tArrayUserInterests[F] = 0.0
       tArrayUserInterests = tArrayUserInterests.astype(np.float)
       nArrayUserInterests = scale(tArrayUserInterests, axis=0, with_mean=True, with_std=True, copy=True )
       avgtArrayUserInterests = tArrayUserInterests.sum(axis=0)/float(len(clusterInterests[k]))
       db.knnRef.insert(cluster_id = k ,**dict(zip(db.knnRef.fields[2:],avgtArrayUserInterests)))
    print "finished making clusters"
    return 0
    
    
    
#code for selecting the appropriate cluster to the newly registered user.
#triggers when the on_register of db event has occured
def knnSelect():
    #getting all rows into an numpy array
    aggregateRows = [] 
    for row in db(db.knnRef.id>0).select(): 
        aRow = []
        for field in db.knnRef.fields[1:]:
               aRow.append(row[field])
        aggregateRows.append(aRow)
    #making the knn operations
    aggregateRows = np.array(aggregateRows)
    aggregateRows = aggregateRows.astype(float)
    knnOut = aggregateRows[:, 0]
    knnIn = aggregateRows[:,1:]
    knn = neighbors.KNeighborsClassifier( weights='distance',metric='minkowski')
    knn.fit(knnIn, knnOut) 
    print knn.predict(np.array([random.randrange(2) for i in range(12)]))
    
    
knnSelect()
#knnMake()
#make_clusters()
#from gluon.scheduler import Scheduler
#scheduler = Scheduler(db)
#scheduler.queue_task(make_clusters, repeats=0, start_time=datetime.datetime.now(), period=86400)

#from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
from osf.models import Timeline
from osf.serializers import TimelineSerializer

#this is for the second part.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser

from osf.models import Timeline
import datetime
from rest_framework.parsers import JSONParser
from django.db import connection
import json




def proper_creation_request(data):
    if 'wiki' not in data or not data['wiki']:
        return False
    if 'title' not in data or not data['title']:
        return False
    if 'author' not in data or not data['author']:
        return False
    if 'date' not in data or not data['author']:
        return False
    if 'project_id' not in data or not data['project_id']:
        return False
    return True



#{"wiki":"w1", "title":"t1", "author":"a1", "project_id": 3}
@csrf_exempt
@api_view(['POST'])
def create_new_project(request):
    print "new proj called"
    if request.method == 'POST':
        print str(request.DATA)

        p_id = int(request.DATA['project_id'])

        if not proper_creation_request(request.DATA):
            return Response("proper input not provided",status=status.HTTP_400_BAD_REQUEST)

        try:

            timeline = Timeline.objects.get(project_id=p_id)

           #if project with given project id exists, then throw error.
            return Response("project already exists",status=status.HTTP_400_BAD_REQUEST)
        except:
            #if error then project doesnt exist. this is good.
            pass

        try:

            post_date = request.DATA['date'].split("-")
            d = datetime.datetime(month=int(post_date[0]), day=int(post_date[1]),year=int(post_date[2])) # 09-20-2014


            data = request.DATA.copy()
            data['date']=d
            data['project_id'] = int(request.DATA['project_id'])


            serializer = TimelineSerializer(data=data)


            if serializer.is_valid():
                serializer.save()
                out = {p_id:"Project Created."}
                return Response(out, status=status.HTTP_201_CREATED)
            return Response("input data exists, but is not valid.", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("project unable to be created.",status=status.HTTP_400_BAD_REQUEST)






@csrf_exempt
@api_view(['GET'])
def project_detail(request):
    print "get called"
    if request.method == "GET":
        if 'project_id' not in request.GET or not request.GET['project_id']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        date_given = False
        if 'date' in request.GET and request.GET['date']:
            date_given=True
            url_date = request.GET['date'].split("-")
            d = datetime.datetime(month=int(url_date[0]), day=int(url_date[1]),year=int(url_date[2])) # 09-20-2014
    #########################POTENTIALLY ADD day+1 HERE since you want to get data back from anytime on input date as well. THUS should start checking from one day after input day.
        try:

            t = Timeline.objects.filter(project_id=int(request.GET['project_id']))

            #actual values of the historical object
            author = ""
            title=""
            wiki=""

            #have the values of the historical object been set?
            hasauthor=False
            hastitle=False
            haswiki=False


            #for i in t.history:
            #    print i.date

            #sort by date (note that date in this case SHOULD actually in ms so its all good but it is not currently :( )
            hist = sorted(t, key=lambda t: t.date, reverse=True)
            """
            for i in hist:
                print i.title, i.title=="", i.title==None, i.title is not None
            for i in hist:
                print i.wiki
            print "#################################################################"
            """
            for h in hist:

                #print h.date,d,'this is it'
                #print "historical date:",h.date,"input date:", d
                #SHOULD MAKE FUNCTION HERE TO DRY BUT NO TIME RIGHT NOW!!

                if date_given: #if there is actually a given date, then go through and care about date.
                    #print str(h.date)[:-6], d
                    #print datetime.datetime.strptime("1995-08-20 20:56:12+0000"[:-6], "%Y-%m-%d %H:%M:%S")
                    #print datetime.datetime.strptime(str(h.date)[:-6], "%Y-%m-%d %H:%M:%S"),"should be less than or equal to",d
                    #print not hasauthor, not hastitle, not haswiki
                    #print h.date == h.date
                    #print h.date <= h.date
                    db_date = datetime.datetime.strptime(str(h.date)[:-6], "%Y-%m-%d %H:%M:%S")

                    if db_date <= d:#00:00:00+00:00
                        #print db_date,"should be less than or equal to", d
                        if not hasauthor or not hastitle or not haswiki:

                            if not hasauthor and not is_empty(h.author):
                                author = h.author
                                #print "author:",author
                                hasauthor = True
                            if not hastitle and not is_empty(h.title):
                                title = h.title
                                #print "title:",title, "is_empty(h.title) returned true in this case"
                                hastitle = True
                            if not haswiki and not is_empty(h.wiki):
                                wiki = h.wiki
                                #print "wiki:",wiki
                                haswiki=True

                        else:
                            break
                else:

                    if not hasauthor or not hastitle or not haswiki:
                        if not hasauthor and not is_empty(h.author):
                            author = h.author
                            #print "author:",author
                            hasauthor = True
                        if not hastitle and not is_empty(h.title):
                            title = h.title
                            #print "title:",title, "is_empty(h.title) returned true in this case"
                            hastitle = True
                        if not haswiki and not is_empty(h.wiki):
                            wiki = h.wiki
                            #print "wiki:",wiki
                            haswiki=True

                    else:
                        break
            #print title, author, wiki
            most_recent_hist = {'title':title,
                                'author':author,
                                'wiki':wiki
            }
            #print str(most_recent_hist)
            #print "#################################################################"

        except:
            return Response("failed to create proper historical object", status=status.HTTP_400_BAD_REQUEST)

        out  = {"project_id":int(request.GET['project_id']),
                         "title": title,
                         "author": author,
                         "wiki":wiki}
        return Response(out , status = status.HTTP_200_OK)
    else:
        return Response("method not allowed" , status = status.HTTP_405_METHOD_NOT_ALLOWED)




def is_empty(x):
    if x is None:
        return True
    if x==None:
        return True
    if x=="":
        return True
    return False



@api_view(['POST'])
def update_project(request):
    if request.method=="POST":
        print '"update project called'
        #print str(request.DATA)
        if 'project_id' not in request.DATA or not request.DATA['project_id']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if 'date' not in request.DATA or not request.DATA['date']: #written yyyy-dd-mm
            return Response("must add date for when this historical value was added", status=status.HTTP_400_BAD_REQUEST)
        try:

            url_date = request.DATA['date'].split("-")
            d = datetime.datetime(month=int(url_date[0]), day=int(url_date[1]),year=int(url_date[2])) # 09-20-2014
            p_id = int(request.DATA['project_id'])






            #sanitize data to use for new input to table
            data = request.DATA.copy()
            data['date']=d
            data['project_id'] = p_id

            #if the number of projects is multiple of 10 then put data.
            t = Timeline.objects.filter(project_id=p_id)
            if len(t)%250==0:
                hist = sorted(t, key=lambda t: t.date, reverse=True)
                has_title = 'title' in data
                has_wiki = 'wiki' in data
                has_author = 'author' in data

                for h in hist:
                    if not has_title or not has_wiki or not has_author:
                        if not has_author and not is_empty(h.author):
                            data['author'] = h.author
                            #print "author:",author
                            has_author = True
                        if not has_title and not is_empty(h.title):
                            data['title'] = h.title
                            #print "title:",title, "is_empty(h.title) returned true in this case"
                            has_title = True
                        if not has_wiki and not is_empty(h.wiki):
                            data['wiki'] = h.wiki
                            #print "wiki:",wiki
                            has_wiki=True
                    else:
                        break


            #data should have date, project_id and whatever values that are actually supposed to be updated
            serializer = TimelineSerializer(data=data)

            if serializer.is_valid():

                #print serializer.data
                serializer.save()

                out = {p_id: "Project Updated."}
                return Response(out, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response("input data was not valid", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("failed.", status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)





#NOTE: can only delete one at a time using this method. :(
@api_view(['DELETE'])
def delete_project(request):
    if request.method=="DELETE":
        print '"delete project called'
        try:
            cursor = connection.cursor()
            p_id = int(request.DATA['project_id'])
            cursor.execute("delete from osf_timeline where project_id=$;", p_id)
            return Response("deleted project_id="+str(id),status.HTTP_200_OK )
        except:
            Response("failed to delete project_id "+p_id, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_all_projects(request):
    if request.method=="DELETE":
        print 'delete all projects called'
        try:
            cursor = connection.cursor()
            cursor.execute("delete from osf_timeline where project_id in (select distinct project_id from osf_timeline);")
            return Response("all projects deleted.",status.HTTP_200_OK )
        except:
            Response("failed to delete all projects ", status=status.HTTP_400_BAD_REQUEST)
#from django.test import TestCase
import unittest
from unittest import TestCase

__author__ = 'himanshu'

#from osf.models import Timeline,History

import requests
import urllib
import datetime
import time
from datetime import tzinfo
import calendar
#--data "csrfmiddlewaretoken=QX4YKZLbWnYH6RGBdcEqe6CezwHlLej1
# &_content_type=application%2Fx-www-form-urlencoded
# &_content=author%3Da2%26wiki%3Dw2%26project_id%3D2%26date%3D09-21-2014"
#
#
# http://localhost:8000/update_project/



def create_project(project_id, date, title, wiki, author, port):
    payload = {'project_id': project_id, 'date': date,'title':title, 'wiki':wiki, 'author':author}
    payload = urllib.urlencode(payload) # date=09-20-2014&wiki=w1&project_id=3&author=a1&title=t1   ???correct????

    #print payload
    data = {'csrfmiddlewaretoken':'QX4YKZLbWnYH6RGBdcEqe6CezwHlLej1',
            '_content_type':'application/x-www-form-urlencoded',
            '_content': payload}#after application, not sure if %2F or /
    r = requests.post('http://localhost:'+str(port)+'/create_new_project/', data=data)
    #returns a list? can you turn it into json?
    print r.status_code
    ret=r.json()
    if ret[str(project_id)] == "Project Created." and r.status_code < 300:
        ret[project_id] = "Project Created."
        del ret[str(project_id)]
        return ret
    return ret


def get_project(project_id,port, date=None, ):
    if date is None:
        payload = {'project_id': project_id}
        r = requests.get('http://localhost:'+str(port)+'/project_detail/', params=payload)
        if r.status_code<300:
            return r.json()
        else:
            return {project_id:"status code was not 2xx"}
    else:
        payload = {'project_id': project_id, 'date': date}
        r = requests.get('http://localhost:'+str(port)+'/project_detail/', params=payload)
        if r.status_code<300:
            return r.json()
        else:
            return {project_id:"status code was not 2xx"}





def update_project(project_id, date, port, title=None, wiki=None, author=None):
    #buid payload
    payload=dict()
    payload['project_id']= project_id
    payload['date']= date
    if title is not None:
        payload['title']=title
    if wiki is not None:
        payload['wiki']=wiki
    if author is not None:
        payload['author']=author

    payload = urllib.urlencode(payload) # date=09-20-2014&wiki=w1&project_id=3&author=a1&title=t1   ???correct????

    #print payload
    data = {'csrfmiddlewaretoken':'QX4YKZLbWnYH6RGBdcEqe6CezwHlLej1',
            '_content_type':'application/x-www-form-urlencoded',
            '_content': payload}#after application, not sure if %2F or /
    r = requests.post('http://localhost:'+str(port)+'/update_project/', data=data)
    ret= r.json()
    if ret[str(project_id)] == "Project Updated." and r.status_code < 300:
        ret[project_id] = "Project Updated."
        del ret[str(project_id)]
        return ret
    return ret


def delete_project(project_id, port):
#csrfmiddlewaretoken=zuqEpa8H4yg3v8Ba4zfFEhWXRjP5nzmP&_method=DELETE
    payload={'project_id':int(project_id)}
    payload = urllib.urlencode(payload)
    data = {'csrfmiddlewaretoken':'zuqEpa8H4yg3v8Ba4zfFEhWXRjP5nzmP',
            '_method':'DELETE',
            'project_id': int(project_id)}#after application, not sure if %2F or /
    r = requests.delete('http://localhost:'+str(port)+'/delete_project/', data=data)

def delete_all_projects_in_range(start, end, port):
    for i in range(start, end):
        delete_project(i, port)

def delete_all_projects(port):
    payload={}
    payload = urllib.urlencode(payload)
    data = {'csrfmiddlewaretoken':'zuqEpa8H4yg3v8Ba4zfFEhWXRjP5nzmP',
            '_method':'DELETE'}
    r = requests.delete('http://localhost:'+str(port)+'/delete_all_projects/', data=data)



#can make more complex.
def convert_utc_format(month, day, year):
    #2014-09-20T00:00:00
    return year+"-"+month+"-"+day+"T"+"00:00:00"


class TestTimelineEndpoints(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def tearDown(self):
        delete_all_projects(9000)

    def test_simple_get(self):
        create_project(project_id=1,date="09-20-1995", title="t1", wiki="w1", author="a1", port=9000 )
        x=get_project(project_id=1, port=9000)
        self.assertEquals(x,{"title":"t1", "wiki":"w1", "author":"a1", "project_id":1})
        delete_all_projects(9000)

    def test_simple_update(self):
        create_project(project_id=1,date="09-20-1995", title="t1", wiki="w1", author="a1", port=9000 )

        x = update_project(project_id=1, date="09-21-1995", title="t2", port=9000)
        self.assertEqual({1:"Project Updated."}, x)

        x = update_project(project_id=1, date="09-22-1995", wiki="w3",port=9000)
        self.assertEqual({1:"Project Updated."}, x)

        x = update_project(project_id=1, date="09-21-1996", author="ta4",port=9000)
        self.assertEqual({1:"Project Updated."}, x)

        delete_all_projects(9000)


    def test_nodate_get_varying_values(self):
        create_project(project_id=1,date="09-20-1995", title="t1", wiki="w1", author="a1", port=9000 )

        x = update_project(project_id=1, date="09-21-1995", title="t2", port=9000)
        self.assertEqual({1:"Project Updated."}, x)
        v =get_project(project_id=1, port=9000)
        self.assertEquals(v,{"title":"t2", "wiki":"w1", "author":"a1", "project_id":1})

        x = update_project(project_id=1, date="09-22-1995", wiki="w3",port=9000)
        self.assertEqual({1:"Project Updated."}, x)
        v =get_project(project_id=1, port=9000)
        self.assertEquals(v,{"title":"t2", "wiki":"w3", "author":"a1", "project_id":1})

        x = update_project(project_id=1, date="09-21-1996", author="a4",port=9000)
        self.assertEqual({1:"Project Updated."}, x)
        v =get_project(project_id=1, port=9000)
        self.assertEquals(v,{"title":"t2", "wiki":"w3", "author":"a4", "project_id":1})

        x = update_project(project_id=1, date="09-22-1996", author="a5", wiki="w5" ,port=9000)
        self.assertEqual({1:"Project Updated."}, x)
        v =get_project(project_id=1, port=9000)
        self.assertEquals(v,{"title":"t2", "wiki":"w5", "author":"a5", "project_id":1})


        x = update_project(project_id=1, date="09-23-1996", title="t6", wiki="w6" ,port=9000)
        self.assertEqual({1:"Project Updated."}, x)
        v =get_project(project_id=1, port=9000)
        self.assertEquals(v,{"title":"t6", "wiki":"w6", "author":"a5", "project_id":1})

        x = update_project(project_id=1, date="09-24-1996", title="t7", wiki="w7", author="a7" ,port=9000)
        self.assertEqual({1:"Project Updated."}, x)
        v =get_project(project_id=1, port=9000)
        self.assertEquals(v,{"title":"t7", "wiki":"w7", "author":"a7", "project_id":1})

        x = update_project(project_id=1, date="09-29-1996", author="a8" ,port=9000)
        self.assertEqual({1:"Project Updated."}, x)
        v =get_project(project_id=1, port=9000)
        self.assertEquals(v,{"title":"t7", "wiki":"w7", "author":"a8", "project_id":1})

        delete_all_projects(9000)



    def test_get_with_time(self):
        create_project(project_id=1,date="09-20-1995", title="t1", wiki="w1", author="a1", port=9000)####t1, w1, a1
        update_project(project_id=1, date="09-21-1995", title="t2", port=9000)###########################t2
        x=get_project(project_id=1,date="09-20-1995" ,port=9000)
        self.assertEquals(x,{"title":"t1", "wiki":"w1", "author":"a1", "project_id":1})

        x=get_project(project_id=1,date="09-22-1995" ,port=9000)
        self.assertEquals(x,{"title":"t2", "wiki":"w1", "author":"a1", "project_id":1})

        update_project(project_id=1, date="09-23-1995", title="t3", port=9000)###########################t3
        v =get_project(project_id=1,date="09-23-1995", port=9000)
        self.assertEquals(v,{"title":"t3", "wiki":"w1", "author":"a1", "project_id":1})

        v =get_project(project_id=1,date="09-22-1995", port=9000)
        self.assertEquals(x,{"title":"t2", "wiki":"w1", "author":"a1", "project_id":1})

        update_project(project_id=1, date="09-25-1995", wiki="w3",port=9000)
        v =get_project(project_id=1, date="09-29-1995",port=9000)
        self.assertEquals(v,{"title":"t3", "wiki":"w3", "author":"a1", "project_id":1})

        v =get_project(project_id=1, date="09-25-1995",port=9000)
        self.assertEquals(v,{"title":"t3", "wiki":"w3", "author":"a1", "project_id":1})

        v =get_project(project_id=1, date="09-24-1995",port=9000)
        self.assertEquals(v,{"title":"t3", "wiki":"w1", "author":"a1", "project_id":1})


        v =get_project(project_id=1, date="09-23-1995",port=9000)
        self.assertEquals(v,{"title":"t3", "wiki":"w1", "author":"a1", "project_id":1})

        v =get_project(project_id=1, date="09-22-1995",port=9000)
        self.assertEquals(v,{"title":"t2", "wiki":"w1", "author":"a1", "project_id":1})

        v =get_project(project_id=1, date="09-20-1995",port=9000)
        self.assertEquals(v,{"title":"t1", "wiki":"w1", "author":"a1", "project_id":1})

        delete_all_projects(9000)


    def test_possible_issue_from_runs(self):

        original = {}
        original['project_id'] = 3000
        original['title']='t1'
        original['wiki']='w1'
        original['author']='a1'


        x= create_project(3000,'09-20-2014', 't1','w1','a1', port=9000)
        self.assertEqual({3000:"Project Created."}, x)


        original['title']='t2'

        y= update_project(3000, date="09-21-2014", title= "t2", port=9000)
        self.assertEqual({3000: "Project Updated."},y)

        z = get_project(3000, port=9000)
        self.assertEqual(original, z)

        q = get_project(3000,date="09-20-2014", port=9000)
        original['title']='t1'
        self.assertEqual(original,q)

        delete_all_projects(9000)


    def test_adding_snapshots(self):

        original = {}
        original['project_id'] = 3000
        original['title']='t1'
        original['wiki']='w1'
        original['author']='a1'


        x= create_project(3000,'09-20-2014', 't1','w1','a1', port=9000)
        self.assertEqual({3000:"Project Created."}, x)


        original['title']='t2'

        for i in range(1,100):
            y= update_project(3000, date="09-21-"+str(2014+i), title= "t"+str(2+i), port=9000)
            self.assertEqual({3000: "Project Updated."},y)



        delete_all_projects(9000)

if __name__ == '__main__':
    unittest.main()



    delete_all_projects(port=9000)
"""
    create_project(project_id=1,date="09-20-1995", title="t1", wiki="w1", author="a1", port=9000 )
    create_project(project_id=1,date="09-21-1995", title="t2", port=9000 )
    create_project(project_id=1,date="09-20-1996", wiki="w3",  port=9000 )
    x = get_project(project_id=1, date="09-20-1995" ,port=9000)
    print x=={"title":"t1", "wiki":"w1", "author":"a1"}
    x = get_project(project_id=1, date="09-20-1995" ,port=9000)
    print x=={"title":"t1", "wiki":"w1", "author":"a1"}
    x = get_project(project_id=1, date="09-20-1995" ,port=9000)
    print x=={"title":"t1", "wiki":"w1", "author":"a1"}
    delete_all_projects(port=9000)

"""


from django.db import models

class Timeline(models.Model):


    #the parameters to the models are:
        #max_length - max length we allow varchar
        #null - makes it so blank values are stored as null in database.
        #default  - default value given to a value. None=null in database
        #blank - allowed to be blank in terms of validation when True.
            # if blank, then null=True will make it null in db
    title = models.CharField(max_length=256, null=True, blank=True)#null= makes it so blank values are stored as null which is what you want.
    author = models.CharField(max_length=256, null=True,blank=True)
    wiki = models.TextField(max_length=256, null=True, blank=True)
    project_id = models.IntegerField(blank=False, null=False)#cant be empty
    #version = models.IntegerField()
    date = models.DateTimeField(blank=False)#cant be empty since by default blank=False(+specified)

    #class Meta:
    #    ordering = ['project_id', '-date']#awesome optimization that keeps your timeline sorted. Do so in mongo as well to take advantage of it. :)





"""

python manage.py makemigrations   <- makes migrations based on updates in model
python manage.py migrate          <- actually runs migrations created at previous step!!!!!!! do both!!!!!!


"""
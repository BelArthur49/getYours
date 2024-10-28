from django.db import models

# Create your models here.

#when you add a new thing to the database
#(which you do by creating new classes here in model)
#you have to migrate it to the python database otherwise it will not be stored
#you migrate by doing makemigrations and then migrate

#model is what is in your database

class Search(models.Model): #the model on database called search
    #which has a field called search
    search_field = models.CharField(max_length=200) 
    #the time stamp of when it has been created
    created = models.DateTimeField(auto_now_add=True)

    #we add this function in order to get thing readable in english
    #not returned as an object when we search it
    #by this it return the search field of it
    #which is written in human readable form in other words what you searched
    #the function __str__ represent an object as a string
    def __str__(self):
        return "{}".format(self.search)

    #we add this line of code because in database it was written Searchs and not Searches
    #and by addind this line of code we changed it into Searches
    class Meta:
        verbose_name_plural ="Searches"
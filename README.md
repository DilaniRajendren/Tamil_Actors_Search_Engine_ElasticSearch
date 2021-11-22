# Tamil_Actors_Search_Engine_ElasticSearch

The repo contain more than 100 actors scrap from https://en.wikipedia.org/wiki/List_of_Tamil_film_actors and stored at Actors_Scrapped.csv(Actors_Scrapped.json) file. Some of the metadata such as  "நடிகர்கள்","அறிமுகஆண்டு" "குறிப்பிடத்தக்க படங்கள்"are in English. For scrapping the data from websites scraping_data.py is used.


###  Sample actors data in JSON Format
  ```
  {
    "நடிகர்": "வினய்",
    "அறிமுகஆண்டு": 2007,
    "அறிமுகதிரைபடம்": "உன்னாலே உன்னாலே",
    "பாலினம்": "ஆண்",
    "குறிப்பிடத்தக்க படங்கள்": "உன்னாலே உன்னாலே, வானா,ஜெயம் கொண்டான்,டேம் 999"
  }
  
  ```
Randomly selected 100 Actors data are scraped and fully traslated to Tamil in CSV file and some extra meta data suchas "திரைப்பட எண்ணிக்", "பிறந்த இடம்","பண"
Randomly selected 500 songs data are fully translated to Tamil and extra metadata such as "மதிப்பீடு", "வகை", "கிளிக்குகள்" are added to improve the quality of the search.  preprocess-finalize.py is used to produce these JSON data.

### Sample JSON data of a processed Actor

  ```
  {
    "நடிகர்": "வினய்",
    "அறிமுகஆண்டு": 2007,
    "அறிமுகதிரைபடம்": "உன்னாலே உன்னாலே",
    "பாலினம்": "ஆண்",
    "குறிப்பிடத்தக்க படங்கள்": "உன்னாலே உன்னாலே, வானா,ஜெயம் கொண்டான்,டேம் 999",
    "பிறப்பு": 1979,
    "அகவை": 44,
    "பிறந்த இடம்": "பெங்களூர், இந்தியா",
    "பணி": "நடிகர்",
    "திரைப்பட எண்ணிக்கை": 15
   }
   ```
   The following Query DSL are supported for all the diiferent types of user queries.
  
  
  ## Query DSL for ElasticSearch search engine
   
```
# deleting an index(database)
DELETE /actors_db


##########################################################################################
#########          This must be run before creating the index(database)       ############
#######      Make a folder named analysis in elasticserach config folder       ###########
####   Please copy tamil_stopwords.txt & tamil_stemming.txt to the analysis folder #######
##########################################################################################


# custom stop words and stemming new analyzer along with the standard analyzer
PUT /actors_db/
{
       "settings": {
           "analysis": {
               "analyzer": {
                   "my_analyzer": {
                       "tokenizer": "standard",
                       "filter": ["custom_stopper","custom_stems"]
                   }
               },
               "filter": {
                   "custom_stopper": {
                       "type": "stop",
                       "stopwords_path": "analysis/tamil_stopwords.txt"
                   },
                   "custom_stems": {
                       "type": "stemmer_override",
                       "rules_path": "analysis/tamil_stemming.txt"
                   }
               }
           }
       }
   }
   
# checking the custom analyzer(stopwords, stemming)
GET /actors_db/_analyze
{
 "text": ["மிகவும்சிறப்பான 10 தமிழ்த்திரைப்படநடிகர்கள்"],
 "analyzer": "my_analyzer"
}

# Uploading data using bulk API
POST /_bulk
{ "index" : { "_index" : "actors_db", "_type" : "actors", "_id" :1 } }
{ "நடிகர்" : "வினய்","அறிமுகஆண்டு":"2007","அறிமுகதிரைபடம்":"உன்னாலே உன்னாலே","பாலினம்":"ஆண்","குறிப்பிடத்தக்க படங்கள்":"உன்னாலே உன்னாலே, வானா,ஜெயம் கொண்டான்,டேம் 999","பிறப்பு":"1979","அகவை":"44","பிறந்த இடம்":"பெங்களூர், இந்தியா","பணி":"நடிகர்","திரைப்பட எண்ணிக்கை":"15"  }
{ "index" : { "_index" : "actors_db", "_type" : "actors", "_id" :2 } }
{"நடிகர்":"கார்த்திக் சிவகுமார் ","அறிமுகஆண்டு":"2007","அறிமுகதிரைபடம்":"பருத்திவீரன்","பாலினம்":"ஆண்","குறிப்பிடத்தக்க படங்கள்":"பருத்தி வீரன்,ஆயிரத்தில் ஒருவன்,பையா, நான் மகான் அல்ல,சகுனி, கொம்பன்,காற்று வெளியிடை","பிறப்பு":"1977","அகவை":"44","பிறந்த இடம்":"சென்னை, தமிழ்நாடு, இந்தியா","பணி":"நடிகர்","திரைப்பட எண்ணிக்கை":"30"  }

# Using custom indexing for search
# பிரித்வராஜ் details with spelling mistake
GET /actors_db/actors/_search
{
   "query": {
       "multi_match" : {
           "query" : "பிரித்ராவஜ்",
           "fuzziness": "AUTO",
       "analyzer": "my_analyzer"
       }
   }
}

# Using standard indexing for search
# பிரித்வராஜ் details with spelling mistake
GET /actors_db/actors/_search
{
   "query": {
       "multi_match" : {
           "query" : "பிரித்ராவஜ்",
           "fuzziness": "AUTO",
       "analyzer": "standard"
       }
   }
}

# top 10 actors introduced within 1990 to 2010 using திரைப்பட எண்ணிக்கை"
GET /actors_db/actors/_search
{
   "size" : 10,
    "sort" : [
       { "திரைப்பட எண்ணிக்கை" : {"order" : "desc"}}
   ],
   "query": {
       "range" : {
           "அறிமுகஆண்டு" : {
               "gte" : "1990",
               "lte" :  "2010"
           }
       }
   }
}

# top 10 actors born within 1970 to 1990 using திரைப்பட எண்ணிக்கை"
GET /actors_db/actors/_search
{
   "size" : 10,
    "sort" : [
       { "திரைப்பட எண்ணிக்கை" : {"order" : "desc"}}
   ],
   "query": {
       "range" : {
           "பிறப்பு" : {
               "gte" : "1970",
               "lte" :  "1990"
           }
       }
   }
}

# top 10 actors born with in 1980 to 1990 filter output
GET /actors_db/actors/_search?filter_path=hits.hits._source.நடிகர்,hits.hits._source.அறிமுகதிரைபடம்,hits.hits._source.பிறப்பு
{
  
   "size" : 10,
    "sort" : [
       { "திரைப்பட எண்ணிக்கை" : {"order" : "desc"}}
   ],
   "query": {
       "range" : {
           "பிறப்பு" : {
               "gte" : "1980",
               "lte" :  "1990"
           }
       }
   }
}

# top 10 actors introduced within 2000 to 2010 filter output
GET /actors_db/actors/_search
{
   "_source":["நடிகர்", "அறிமுகஆண்டு","அறிமுகதிரைபடம்" ],
   "size" : 10,
    "sort" : [
       { "திரைப்பட எண்ணிக்கை" : {"order" : "desc"}}
   ],
   "query": {
       "range" : {
           "அறிமுகஆண்டு" : {
               "gte" : "2000",
               "lte" :  "2010"
           }
       }
   }
}

#  top 10 actors introduced from 2010
GET /actors_db/actors/_search
{
   "size":10,
   "sort" : [
        { "திரைப்பட எண்ணிக்கை" : {"order" : "desc"}}
   ],
   "query": {
       "multi_match": {
             "query" : "2010",
           "fields":["அறிமுகஆண்டு"],
           "fuzziness": "AUTO"
       }
   }
}

```
  
   

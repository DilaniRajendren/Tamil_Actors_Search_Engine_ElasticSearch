import json
import codecs
import random


actors_category = [ "நடிகர்" ,"அறிமுகஆண்டு","அறிமுகதிரைபடம்","பாலினம்","குறிப்பிடத்தக்க படங்கள்","பிறப்பு","அகவை","பிறந்த இடம்","பணி","திரைப்பட எண்ணிக்கை"]
f = codecs.open('processed_actors_bulk_api.txt', 'w', encoding='utf-8')

json_file = open("actors.csv", encoding='utf-8', errors='ignore')

i=1
for line in json_file:
    try:
        print(i)
        actors_json = json.loads(line)

        actors_json["திரைப்பட எண்ணிக்கை"] = random.randint(1, 500)

        f.write('{ "index" : { "_index" : "actors_db", "_type" : "actors", "_id" :' + str(i) + ' } }\n')
        json.dump(actors_json, f, ensure_ascii=False)
        f.write('\n')
        i += 1
        print(actors_json)
        print()

    except Exception as e:
        print("Something else went wrong")





# for attribute, value in song_json.items():
#     # print(attribute, value)
#     song_json[attribute] = unicodedata.normalize("NFKD", str(value))

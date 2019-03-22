#imports row as a list, columns become row[0], row[1], etc
#need to match the correct attribute to the correct field
#have to insert site last

import csv
from unesco.models import Category, iso, Region, States, Site
fh = open('unesco/whc-sites-2018-small.csv')
rows = list(csv.reader(fh))


Category.objects.all().delete()
iso.objects.all().delete()
Region.objects.all().delete()
States.objects.all().delete()
Site.objects.all().delete()

"""
i = 0
for row in rows:
    if len(row[0]) < 1 : continue
    print(row[0])
    i = i + 1
    if i > 5 : break
"""

for row in rows[1:]:
    try:
        c = Category.objects.get(name=row[7])
    except:
        print("Inserting category",row[7])
        c = Category(name=row[7])
        c.save()

    try:
        i = iso.objects.get(name=row[10])
    except:
        print("Inserting iso",row[10])
        i = iso(name=row[10])
        i.save()

    try:
        r = Region.objects.get(name=row[9])
    except:
        print("Inserting region",row[9])
        r = Region(name=row[9])
        r.save()

    try:
        s = States.objects.get(name=row[8])
    except:
        print("Inserting state",row[8])
        s = States(name=row[8])
        s.save()

    try:
        area=float(row[6])
    except:
        area=None

    try:
        longitude=float(row[4])
    except:
        longitude=None

    try:
        latitude=float(row[5])
    except:
        latitude=None

    site=Site(name=row[0],description=row[1],year=row[3],justification=row[2],longitude=longitude,latitude=latitude,area_hectares=area,category=c,iso=i,region=r,states=s)
    site.save()


#formation
#['Cultural Landscape and Archaeological Remains of the Bamiyan Valley', '<p>The cultural landscape and archaeological remains of the Bamiyan Valley represent the artistic and religious developments which from the 1st to the 13th centuries characterized ancient Bakhtria, integrating various cultural influences into the Gandhara school of Buddhist art. The area contains numerous Buddhist monastic ensembles and sanctuaries, as well as fortified edifices from the Islamic period. The site is also testimony to the tragic destruction by the Taliban of the two standing Buddha statues, which shook the world in March 2001.</p>', '<p><em>Criterion (i):</em> The Buddha statues and the cave art in Bamiyan Valley are an outstanding representation of the Gandharan school in Buddhist art in the Central Asian region.</p>\n<p><em>Criterion (ii)</em> : The artistic and architectural remains of Bamiyan Valley, and an important Buddhist centre on the Silk Road, are an exceptional testimony to the interchange of Indian, Hellenistic, Roman, Sasanian influences as the basis for the development of a particular artistic expression in the Gandharan school. To this can be added the Islamic influence in a later period.</p>\n<p><em>Criterion (iii):</em> The Bamiyan Valley bears an exceptional testimony to a cultural tradition in the Central Asian region, which has disappeared.</p>\n<p><em>Criterion (iv):</em> The Bamiyan Valley is an outstanding example of a cultural landscape which illustrates a significant period in Buddhism.</p>\n<p><em>Criterion (vi):</em> The Bamiyan Valley is the most monumental expression of the western Buddhism. It was an important centre of pilgrimage over many centuries. Due to their symbolic values, the monuments have suffered at different times of their existence, including the deliberate destruction in 2001, which shook the whole world.</p>', '2003', '67.82525', '34.84694', '158.9265', 'Cultural', 'Afghanistan', 'Asia and the Pacific', 'af']

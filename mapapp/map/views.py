from django.http import HttpResponse
from django.template import loader
import googlemaps
import json

log = ['Logs :'];
pathss = [];
n=0;
cost = 0;
completed = []

def index(request):
    template = loader.get_template('map/index.html')
    context = {
        'none':1
    }
    return HttpResponse(template.render(context,request))

def submitform(request):
    gg = request.POST['lat']
    gh = request.POST['long']
    latar = gg.split(',')
    longar = gh.split(',')

    global log,n,cost,completed,pathss

    log = []
    completed = []
    pathss = []

    ii = 2
    gmaps = googlemaps.Client(key='API-KEY')
    jj = len(longar)
    n = jj
    for xx in range(jj):
        completed.append(0)

    cost = 0
    DMatrix = [[0 for x in range(jj)] for y in range(jj)]
    for x in range(jj-1):
        for y in range(x+1,jj):
            co1 = latar[x]+","+longar[x]
            co2 = latar[y]+","+longar[y]
            my_dist = gmaps.distance_matrix(co1,co2)['rows'][0]['elements'][0]
            d2 = int(my_dist["distance"]["value"])
            DMatrix[x][y] = d2;
            DMatrix[y][x] = d2;

    print(str(DMatrix))

    log.append("Latitudes: "+str(latar));
    log.append("Longitudes: "+str(longar));
    log.append("Adjency Matrix: "+str(DMatrix));

    mincost(0,DMatrix);
    #strr = shortest(jj,DMatrix);

    sttar = pathss;
    log.append("Route: "+str(sttar));

    latarn = []
    longarn = []
    for i in range(jj):
        latarn.append(latar[sttar[i]-1]);
        longarn.append(longar[sttar[i]-1]);

    template = loader.get_template('map/path2.html')
    context = {
        'lat1':latarn,
        'long1':longarn,
        'myl': zip(latarn, longarn),
        'log':log,
        'counter' : 0
    }
    return HttpResponse(template.render(context,request))


def mincost2(city,ary):
    global pathss,cost,n
    completed[city] = 1
    return 0

def mincost(city,ary):
    global pathss,cost,n,completed
    if(city==9999999):
        city = 0
    completed[city] = 1
    pathss.append(city+1)
    ncity=least(city,ary);
    if(ncity==9999999):
        ncity=0;
        pathss.append(ncity+1)
        cost+=ary[city][ncity];
        return
    mincost(ncity,ary)


def least(c,ary):
    nc=9999999
    min=9999999
    global pathss,cost,n,completed
    for i in range(n):
        if((ary[c][i]!=0)and(completed[i]==0)):
            if(ary[c][i]+ary[i][c] < min):
                min=ary[i][0]+ary[c][i];
                kmin=ary[c][i];
                nc=i;
    if(min!=9999999):
        cost+=kmin;
    return nc

def givefour():
    return 4;

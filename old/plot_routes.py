 # -*- coding: utf-8 -*-
 # 55.7522200 широта
 # 37.6155600 долгота
 # working google key for google maps directions API!
 # AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog
 # example request 
 # https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog

import json, requests#, ittertools

def get_pairs_list_from_dicts_list(coords_list_of_dicts):
    p_list = []
    for a_dict in coords_list_of_dicts:
        p_list.append((a_dict[u'lat'],a_dict[u'lng']))
    return p_list

def get_lat_lon_by_address(address_string):
    url = "http://maps.google.com/maps/api/geocode/json"
    # ?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&sensor=false
    address_string+=',Russia'
    params = dict(
        address=address_string,
        sensor='false',
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    # print(data)
    # for key,val in (data[u'results'][0]).iteritems():
    #     print(key, len(val),type(val))
    geo = (data[u'results'][0][u'geometry'])
    # for key,val in (geo).iteritems():
    #     print(key, len(val),type(val))
    location_dict = geo[u'location']
    # print(location_dict)
    return location_dict

def get_route_from_gmaps(origin,dest):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = dict(
        # origin='Toronto',
        origin='%f,%f' % (origin[u'lat'],origin[u'lng']),
        # origin='55.7522200,37.6155600',
        # destination='Montreal',
        destination='%f,%f' % (dest[u'lat'],dest[u'lng']),
        # destination='59.9386300,30.3141300',
        # waypoints='Joplin,MO|Oklahoma+City,OK',
        sensor='false',
        key='AIzaSyDhefiliHi_T2eke5NRHzKWvGqj7OteDog'
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    routes = data["routes"]
    print(len(routes[0]))    
    print(type(routes[0]))
    for key, val in routes[-1].iteritems():
        print(key)
    # print("routes[0]['bounds']")    
    # print(routes[0]['bounds']) 
    # print("routes[0]['legs']")    
    # print(routes[0]['legs'])
    # print(type(routes[0]['legs'][-1]))
    # print(len(routes[0]['legs'][-1]))
    for key,val in (routes[0]['legs'][-1]).iteritems():
        print(key, len(val),type(val))
    a_step = routes[0]['legs'][-1][u'steps'][0]
    print("a_step")
    print(type(a_step), len(a_step))
    for key,val in (a_step.iteritems()):
        print(key, len(val),type(val))


    # print(len(routes[0]['legs']))
    # print(routes[0]['legs'][-1])



    duration_text = routes[0]['legs'][-1][u'duration']['text']
    total_duration_value = routes[0]['legs'][-1][u'duration']['value']
    distance_text = routes[0]['legs'][-1][u'distance']['text']
    total_distance_value = routes[0]['legs'][-1][u'distance']['value']
    annotations=[u"Source",u"Tver",u"Reciever\n%s\n%s" % (duration_text,distance_text)]

    coord_pairs = [(origin[u'lat'],origin[u'lng']),(56.8583600,35.9005700),(dest[u'lat'],dest[u'lng'])]

    coords_list_of_dicts = []
    annotes4points = []
    coords_list_of_dicts.append(origin)
    annotes4points.append(u"Source")
    print(origin)
    for i,step in enumerate(routes[0]['legs'][-1][u'steps']):
        print("step No %i: %s" % (i,str(step[u'end_location'])))
        coords_list_of_dicts.append(step[u'end_location'])
        annotes4points.append(step[u'duration']['text'])
    print(dest)
    coords_list_of_dicts.append(dest)
    annotes4points.append(u"Reciever\n%s\n%s" % (duration_text,distance_text))
    print(annotes4points)

    list_of_coords_pairs = get_pairs_list_from_dicts_list(coords_list_of_dicts)

    print("total points_count = %i" % len(coords_list_of_dicts))
    print("total annotes count = %i" % len(annotes4points))

    return list_of_coords_pairs, annotes4points, total_distance_value, total_duration_value


import numpy as np
import matplotlib
# matplotlib.use('nbagg')
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import mpld3
# matplotlib.use('nbagg')

def plot_route(coord_pairs,annotes):
    # matplotlib.use('nbagg')
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    MIN_L_WIDTH=10
    POINT_SIZE=2*MIN_L_WIDTH
    fig = plt.figure("caption",figsize=(10,10))
    ax = fig.add_subplot(111)

    # colors_list = cm.rainbow(np.linspace(0,1,len(coord_pairs)))
    ax.plot(*zip(*coord_pairs),ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='r')
    for i, txt in enumerate(annotes):
        ax.annotate(txt, (coord_pairs[i][0],coord_pairs[i][1]), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points')
        # ax.annotate(txt, (coord_pairs[i][0],coord_pairs[i][1]), xytext=(1,1))
    ax.set_xlim([0.9*min(zip(*coord_pairs)[0]),1.1*max(zip(*coord_pairs)[0])]) # must be after plot
    ax.set_ylim([0.9*min(zip(*coord_pairs)[1]),1.1*max(zip(*coord_pairs)[1])])

    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    # mpld3.show() # bad rendering
    plt.show()

# plot_route(coord_pairs,annotations)
# plot_route(list_of_coords_pairs,annotes4points)

from mpl_toolkits.basemap import Basemap

def plot_route_on_basemap(coord_pairs,annotes,added_points_param_list=None):
    matplotlib.use('nbagg')
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    # matplotlib.use('nbagg')
    fig=plt.figure(figsize=(16,12))
    ax=fig.add_axes([0.05,0.05,0.95,0.95])

    lat_list, lng_list = zip(*coord_pairs)

    # setup mercator map projection.
    m = Basemap(llcrnrlon=min(lng_list)-2,llcrnrlat=min(lat_list)-2,urcrnrlon=max(lng_list)+2,urcrnrlat=max(lat_list)+2,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_0=0.,lon_0=0.,lat_ts=0.)
    
    MIN_L_WIDTH=7
    POINT_SIZE=2*MIN_L_WIDTH

    m.drawcoastlines()
    m.fillcontinents()
    x_all=[]
    y_all=[]
    for i,point in enumerate(coord_pairs):
        lon = point[-1]
        lat = point[0]
        x,y = m(*[lon,lat])
        x_all.append(x)
        y_all.append(y)
        if (i!=0 and i!=len(annotes)-1):
            plt.annotate(annotes[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7), ec="none"))
    plt.annotate(annotes[-1], xy=(x_all[-1],y_all[-1]), xytext=(POINT_SIZE/2,POINT_SIZE), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7)))
    plt.annotate(annotes[0], xy=(x_all[0],y_all[0]), xytext=(POINT_SIZE/2,POINT_SIZE), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.7, 0.7)))

    plt.plot(x_all,y_all,ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='r')

    #----
    # plt, m = add_points_to_basemap_plot(plt,m,[1,1])
    #----
    with open("x.txt",'w') as f:
        pass
    if added_points_param_list!=None:
        added_points_coords = added_points_param_list[0]
        names = added_points_param_list[1]
        # x_added=[]
        # y_added=[]
        for i,point in enumerate(added_points_coords):
            lat = point[0]
            lon = point[-1]
            x,y = m(*[lon,lat])
            # x_added.append(x)
            # y_added.append(y)
            # if (i!=0 and i!=len(names)-1):
            # plt.annotate(names[i], xy=(x,y), xytext=(POINT_SIZE/2,POINT_SIZE/2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.5, 0.7), ec="none"))
            plt.annotate(names[i], xy=(x,y), xytext=(0,-POINT_SIZE*2), textcoords='offset points',bbox=dict(boxstyle="round", fc=(1.0, 0.5, 0.7)))
            plt.plot(x,y,ls='-',marker='o',ms=POINT_SIZE,lw=MIN_L_WIDTH,alpha=0.5,solid_capstyle='round',color='pink')
            with open("x.txt",'a') as f:
                f.write("plotted %f,%f\n" % (x,y))


    # draw parallels
    m.drawparallels(np.arange(-20,0,20),labels=[1,1,0,1])
    # draw meridians
    m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
    # ax.set_title('Great Circle from New York to London')
    m.bluemarble()
    plt.show()
    # mpld3.show() # bad rendering

def test():
    origin = {u'lat':55.7522200,u'lng':37.6155600}
    dest = {u'lat':59.9386300,u'lng':30.3141300}

    list_of_coords_pairs, annotes4points, dist,dur = get_route_from_gmaps(origin,dest)

    print(dist,dur/(60*60.))

    plot_route_on_basemap(list_of_coords_pairs,annotes4points)

if __name__ == "__main__":
    # test()
    
    # plot_route_on_basemap(list_of_coords_pairs,annotes4points)
    coords_tver = get_lat_lon_by_address('Tver')
    coords_krasnogorsk = get_lat_lon_by_address('Krasnogorsk')
    coords_moscow = get_lat_lon_by_address('Moscow')
    coords_sarov = get_lat_lon_by_address('Sarov')
    print(coords_tver)
    print(coords_krasnogorsk)
    print(coords_moscow)

    list_of_coords_pairs, annotes4points, dist,dur = get_route_from_gmaps(coords_moscow,coords_sarov)
    # list_of_coords_pairs, annotes4points, dist,dur = get_route_from_gmaps(coords_moscow,coords_tver)
    plot_route_on_basemap(list_of_coords_pairs, annotes4points)
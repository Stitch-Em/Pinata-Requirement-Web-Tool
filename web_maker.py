#Imports
#Make sure to have graphviz installed
import graphviz
import json
import os


##############################################################################################################################
#Edit these parameters to change how the program runs
##############################################################################################################################
data_file = 'data.json'
level_groups = False

#edge booleans
draw_appear = True
draw_capture = True
draw_visit = True
draw_resident = True
draw_romance = True

##############################################################################################################################

##############################################################################################################################
#These are constants - You can edit them if you knwo what you're doing
##############################################################################################################################
location_colour = {
        'Garden':'black',
        'Jungle':'green',
        'Artic':'blue',
        'Desert':'yellow'
    }
##############################################################################################################################

#Read the json data file 
with open(data_file) as in_file:
    data = json.load(in_file)


#Create the path to the graph including its name
path = f'{os.getcwd()}/food-web.gv'


#Initialise the graph setting the name ot the correct path so it saves ot the correct location 
graph = graphviz.Digraph(filename = path)


#keep track of nodes defined in the json file
names = []
lvls = []


#add all the nodes
for pinata in data['pinatas']:
    lvl = pinata['Lvl']

    #create level lsit
    if not (lvl in lvls):
        lvls.append(lvl)

    #set the node colour to one that matches
    colour = location_colour[pinata['Location']]

    #put in groups or not
    if level_groups:
        with graph.subgraph(name = f'cluster_{lvl}') as c:
            c.attr(label = f'Level {lvl}')
            #c.attr(rank='same')
            c.node(str(lvl), style='invisible')
            c.node(pinata['Name'], shape = 'box', color= colour)
    else:
        graph.node(pinata['Name'], shape = 'box', color= colour)

    #record names
    names.append(pinata['Name'])


#add plants
for plant in data['plants']:
    lvl = plant['Lvl']
    if not (lvl in lvls):
        lvls.append(lvl)

    if level_groups:
        with graph.subgraph(name = f'cluster_{lvl}') as c:
            c.attr(label = f'Level {lvl}')
            #c.attr(rank='same')
            c.node(str(lvl), style='invisible')
            c.node(plant['Name'], shape = 'diamond')
    else:
        graph.node(plant['Name'], shape = 'diamond')
   
    names.append(plant['Name'])


#go through each pinatas requirements
for pinata in data['pinatas']:
    #if draw appear
    if draw_appear:
        if pinata['Appear']:
            for req in pinata['Appear']:
                #if it's in the lsit of requirements drawn an edge
                if req in names:
                    graph.edge(pinata['Name'],req)
                #if it's not in the lsit of requirements draw a red edge
                else:
                    graph.edge(pinata['Name'],req, color = 'red')

    #capture                    
    if draw_capture:
        if pinata['Capture']:
            for req in pinata['Capture']:
                #if it's in the lsit of requirements drawn an edge
                if req in names:
                    graph.edge(pinata['Name'],req, color = 'green')
                #if it's not in the lsit of requirements draw a red edge
                else:
                    graph.edge(pinata['Name'],req, color = 'red')

    if draw_visit:
        if pinata['Visit']:
            for req in pinata['Visit']:
                #if it's in the lsit of requirements drawn an edge
                if req in names:
                    graph.edge(pinata['Name'],req, color='blue')
                #if it's not in the lsit of requirements draw a red edge
                else:
                    graph.edge(pinata['Name'],req, color = 'red')

    if draw_resident:
        if pinata['Resident']:
            for req in pinata['Resident']:
                #if it's in the lsit of requirements drawn an edge
                if req in names:
                    graph.edge(pinata['Name'],req, color='orange')
                #if it's not in the lsit of requirements draw a red edge
                else:
                    graph.edge(pinata['Name'],req, color = 'red')

    if draw_romance:
        if pinata['Romance']:
            for req in pinata['Romance']:
                #if it's in the lsit of requirements drawn an edge
                if req in names:
                    graph.edge(pinata['Name'],req, color='pink')
                #if it's not in the lsit of requirements draw a red edge
                else:
                    graph.edge(pinata['Name'],req, color = 'red')


lvls.sort(reverse=True)

if level_groups:
    for i, lvl in enumerate(lvls):
        if (i+1) != len(lvls):
            graph.edge(str(lvls[i]), str(lvls[i+1]), style='invisible', arrowhead='none')
        


graph.render(directory=os.getcwd(), view=True)

graph.format = 'png'

graph.render(directory=os.getcwd())

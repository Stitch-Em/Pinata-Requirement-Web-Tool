#Imports
#Make sure to have graphviz installed amnd added to your path
import graphviz
import json
import os


##############################################################################################################################
#Edit these parameters to change how the program runs
##############################################################################################################################


#The name of the json file we're going to load
data_file = 'data.json'


#Whether we group nodes by their object level
level_groups = False


#These booleans control whether a particular connection type is drawn
draw_connection = {
    'Appear':True,
    'Capture':True,
    'Visit':True,
    'Resident':True,
    'Romance':True
    }


#These booleans control the which object types we add to the graph
draw_type = {
    'Pinata':True,
    'Plant':True,
    'Gameplay':True
    }

#If set to true it won't make a red node for requirements that are missing in the data
surpress_missing_data_nodes = False

#The colour given to nodes based off their primary location
location_colour = {
    'NA':'white',
    'Garden':'white',
    'Jungle':'green',
    'Artic':'blue',
    'Desert':'yellow'
    }


#The colour coding given to different requirement types
link_colour = {
    'Appear':'white',
    'Capture':'green',
    'Visit':'blue',
    'Resident':'orange',
    'Romance':'pink',
    'Undefined':'red'
    }


#The shape used for each object type
type_shapes = {
    'Pinata':'polygon',
    'Plant':'diamond',
    'Gameplay':'pentagon'
    }


##############################################################################################################################


#Read the json data file
with open(data_file) as in_file:
    data = json.load(in_file)


#Create the path to the graph including its name
path = f'{os.getcwd()}/food-web.gv'


#Initialise the graph setting the name ot the correct path so it saves ot the correct location 
graph = graphviz.Digraph(filename = path)#, engine='neato')

#Make the graph black with white text
graph.attr(bgcolor="black", fontcolor='white')


#graph.attr(overlap="scalexy")


#Keep track of nodes defined in the json file
names = []
lvls = []


#Add nodes
#Loop through all the objects in the data
for obj in data['Objects']:
    #Check to see if we want to draw the type of object it is
    if draw_type[obj['Type']]:
        #Keep track of object levels
        if not (obj['Lvl'] in lvls):
            lvls.append(obj['Lvl'])

        #whether to place node in level subgraph
        if level_groups:
            with graph.subgraph(name = f'cluster_{lvl}') as c:
                #Name the subgraph
                c.attr(label = f'Level {lvl}')
                #Make invisible level node, this is used later to ensure a level hierarchy 
                c.node(str(lvl), style='invisible')
                #Create node in subgraph
                c.node(obj['Name'], shape = type_shapes[obj['Type']], color = location_colour[obj["Primary_Location"]], fontcolor='white')
        else:            
            #Just make node in main graph if we aren't using a subgraph
            graph.node(obj['Name'], shape = type_shapes[obj['Type']], color = location_colour[obj['Primary_Location']], fontcolor='white')

        #Keep a list of all the objects to be drawn
        names.append(obj['Name'])


#Add edges representing requirements
#Loop through all the objects in the data
for obj in data['Objects']:
    #Get the requirements for an object
    requirements = obj['Requirements']

    #Loop through all the requiremnt types 
    for requirement_type in requirements.keys():
        #Check to see if we are drawing that requirement type
        if draw_connection[requirement_type]:
            #Loop through all the requirememnts in the type
            for req in requirements[requirement_type]:
                #If the requirement is in the graph draw a normal node
                if req in names:
                    graph.edge(obj['Name'],req, color = link_colour[requirement_type])
                    
                #If it's not in the list of requirements
                else:
                    #If we are not surpressing missing requirement nodes
                    if not(surpress_missing_data_nodes):
                        #Make a red node and draw a red edge to it to denote that this object is missing from the data
                        graph.node(req, color = 'red', fontcolor='white')
                        graph.edge(obj['Name'], req, color = 'red')


#Sort the object levels in reverse
lvls.sort(reverse=True)


#Make the connections between the level nodes such that the highest level is at the top of the graph.
if level_groups:
    for i, lvl in enumerate(lvls):
        if (i+1) != len(lvls):
            graph.edge(str(lvls[i]), str(lvls[i+1]), style='invisible', arrowhead='none')
        

#show the graph as a pdf
graph.render(directory=os.getcwd(), view=True)


#Save the graoh as a png with ahigher DPI than default
graph.format = 'png'
graph.attr(dpi = '200')
graph.render(directory=os.getcwd())

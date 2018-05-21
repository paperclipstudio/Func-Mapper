import math
import plotly.plotly as py  #
import plotly.offline as offline
from plotly.graph_objs import *
from random import random
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import networkx as nx
import os


def split_into_lines(string):
    return string.split('\n')


def find_indent(string):
    out = 0
    # returns as INT how many tabs a line is indented
    while True:
        if string[:4] == '    ':
            out += 1
            string = string[4:]
        else:
            break
    return out


def is_list(lst):
    if isinstance(lst, (list, tuple)):
        return True
    return False


def flatten_list(input_list):
    output = []
    for e in input_list:
        if isinstance(e, list):
            output = output + flatten_list(e)
        else:
            output.append(e)
    return output


def remove_whitespace(string):
    """
    Removes white space from the head of a string
    str -> str
    """
    if not is_list:
        return ''
        print ('Error, remove_whitespace() given a list')
    if string == '':
        return ''
    if string[0] == ' ':
        return remove_whitespace(string[1:])
    else:
        return string


def split_into_blocks_of_code(input_list):
    """
    Takes a list where each element is a line of code
    and creates nests of list to reflect the blocks of code

    E.G.
    ['print("start")',
    'if true:',
    '    print ('this')',
    '    pass',
    'else:',
    '    pass']

    becomes

    ['print("start")',
    'if true:',
    ['print ('this')', 'pass'],
    'else',
    ['pass']]

    list - > nested list
    """
    code_blocks = []
    for line in input_list:
        if line == '':
            continue
        if find_indent(line) > 0:
            code_blocks[-1].append(remove_whitespace(line))
        else:
            code_blocks.append([line])
    return code_blocks


def add_functions_to_dict(string, dict=None):
    '''
     takes in a string and finds all functions that are defined and adds them to a dict
     returns the dict, but also mutates input dict
    '''
    if dict == None:
        dict = {}
    start = string.find('def')
    while not start < 0:
        end = string.find('(', start + 1)
        dict[string[start + 4:end]] = 0
        string = string[end:]
        start = string.find('def')
    return dict


def flatten_second_layer(input_list):
    """
    Flattens the second layer of nested lists
    """
    output = []
    for i in range(len(input_list)):
        if isinstance(input_list[i], list):
            output.append(flatten_list(input_list[i]))
        else:
            output.append(input_list[i])
    return output


def remove_non_definition_code(code_blocks):
    output = []
    for block in code_blocks:
        if block[0][:3] == 'def':
            output.append(block)
    return output


def build_dict(code_blocks):
    output = {}
    for function in code_blocks:
        output[function[0].split('(')[0]] = []
    return output


def add_refrences(dict_of_func, code_blocks):
    for block in code_blocks:
        for word in block[1:]:
            first_word = word.split('(')[0]
            if first_word in dict_of_func:
                func_string = (block[0].split('(')[0])
                if first_word not in dict_of_func[func_string]:
                    dict_of_func[func_string].append(first_word)


def break_lines_into_words(code_block):
    for i in range(len(code_block)):
        new_func = []
        for j in range(len(code_block[i])):
            # print (code_block[i][j].split())
            new_func = new_func + code_block[i][j].split()
        code_block[i] = new_func[1:]


def create_function_graph(input_code):
    code_by_lines = (split_into_lines(input_code))
    code_blocks = split_into_blocks_of_code(code_by_lines)
    code_blocks = remove_non_definition_code(code_blocks)
    break_lines_into_words(code_blocks)
    function_digraph = build_dict(code_blocks)
    add_refrences(function_digraph, code_blocks)
    return function_digraph

def get_code_from_file(file_dir: str):
    file = open(file_dir, 'r')
    code = file.read()
    file.close()
    return code



def render_output(function_digraph):
    if function_digraph == {}:
        print("Empty input")
        return False


    graph_network = nx.DiGraph()


    key = 0
    # lookup is used to map function to graph_network's first int
    lookup = {}

    for i in function_digraph:
        # Add functions as Nodes and with X,Y positioning
        graph_network.add_node(key, name=i, x=0, y=0)
        twopi = math.pi * 2
        x0, y0 = math.cos(twopi * key / len(function_digraph)), math.sin(twopi * key / len(function_digraph))
        graph_network.add_node(key, name=i, x=x0, y=y0)

        # Fills lookup
        lookup[i] = key
        key += 1


    for i in function_digraph:
        for j in function_digraph[i]:
            graph_network.add_edge(lookup[i], lookup[j])

    # Builds a plotly scatter diagram from the edge connectors
    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=5, color='#000'),
        hoverinfo='all',
        mode='Lines')

    for edge in graph_network.edges():
        # print(edge, G.node[edge[0]])
        x0, y0 = graph_network.node[edge[0]]['x'], graph_network.node[edge[0]]['y']
        x1, y1 = graph_network.node[edge[1]]['x'], graph_network.node[edge[1]]['y']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='marker+text',
        hovertext='None',
        hoverinfo='text',
        textfont=dict(
            size=25,
            family="Courier New"
        ),
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='YIGnBu',
            reversescale=True,
            color=[],
            size=2,

            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in graph_network.nodes():
        x, y = graph_network.node[node]['x'], graph_network.node[node]['y']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(graph_network.node[node]['name'])

    list = [[], [], [], []]
    for i in (range(int(len((edge_trace['x'])) / 3))):
        list[0].append(edge_trace['x'][i * 3] + edge_trace['x'][i * 3 + 1] * 0.1)
        list[1].append(edge_trace['y'][i * 3] + edge_trace['y'][i * 3 + 1] * 0.1)
        list[2].append((edge_trace['x'][i * 3 + 1] - edge_trace['x'][i * 3]) * 9)
        list[3].append((edge_trace['y'][i * 3 + 1] - edge_trace['y'][i * 3]) * 9)
    print (list)
    fig = ff.create_quiver(list[0], list[1], list[2], list[3], arrow_scale=0.1)
    fig['data'].append(node_trace)
    offline.plot(fig, filename='networkx.html')


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
pd.set_option('display.max_rows', 18)
pd.set_option('display.max_columns', 18)
pd.set_option('display.width', 140)
np.set_printoptions(linewidth=500)

class Road:
    def __init__(self, graph, node1, node2, ftt, ca):
        self.key = graph.add_edge(node1, node2, weight=ftt, ca=ca)
        roadlist.append(self)
        self.node1 = node1
        self.node2 = node2
        self.ftt = ftt
        self.ca = ca
        self.va = 0
        self.att = ftt

    def BPR(self):
        self.att = self.ftt * (1 + 0.15 * (self.va / self.ca)**4)
        return self.att

def first_iter(matrix):
    hor_sum = np.sum(matrix, axis=0)
    nieuw = np.zeros([18,18])
    for i in range(len(matrix)):
        nieuw[i]=matrix.iloc[i]*trips[i]/hor_sum.iloc[i]
    return nieuw

def iterate(matrix):
    hor_sum = np.sum(matrix, axis=0)
    nieuw = np.zeros([18, 18])
    for i in range(len(matrix)):
        nieuw[i] = np.transpose(matrix)[i] * trips[i] / hor_sum[i]
    return nieuw

def sum_spots(data,spots):
    sum = 0
    for i in range(len(spots)):
        sum += data.iloc[spots[i][0], spots[i][1]]
    return sum

def att_to_dist(matrix, itt, ett):
    new = np.copy(matrix)
    for i in range(len(itt)):
        for j  in range(len(new)):
            new[i, j] += 0.5 * itt[i]
            new[j, i] += 0.5 * itt[i]
    for i in range(len(ett)):
        for j in range(len(new)):
            new[i + 9, j] += ett[i]
            new[j, i + 9] += ett[i]
    return new

def route_assignment(dist_hour_results, loops):
    att_matrix = np.zeros([18,18])
    for i in range(loops):
        for j in range(len(locations)):
            for k in range(len(locations)):
                if j != k:
                    path_length, path = nx.single_source_dijkstra(G, locations[j], locations[k], weight="weight")
                    if i == loops - 1:
                        att_matrix[j, k] = path_length
                    for l in range(len(path)-1):
                        for m in range(len(roadlist)):
                            if path[l] == roadlist[m].node1 and path[l+1] == roadlist[m].node2:
                                roadlist[m].va += dist_hour_results[j, k]/loops
                                roadlist[m].BPR()
                                G.edges[path[l], path[l+1], roadlist[m].key]["weight"] = roadlist[m].att
                                break
    return att_matrix



trips = [53808, 58528, 54000, 120055, 55021, 57026, 89151, 38976, 58521,
         14947, 26113, 35867, 20044, 30073, 18314, 21331, 16131, 45738]
#trips = [i/2 for i in trips]
beta = 0.1

labels = ["Dukenburg", "Lindenholt", "Centrum", "Midden", "Nieuw-West", "Noord", "Oost", "Oud-West", "Zuid",
          "A73 Zuid", "A73 Midden", "A73 Noord", "N324", "N326", "Malden", "Duitsland", "A15", "Arnhem"]


roadlist = []
G = nx.MultiDiGraph()
r1Az = Road(G, "Az", "a", 1.75, 3600)
r1a = Road(G, "a", "Az", 1.75, 3600)
r2a = Road(G, "a", "b", 2, 3600)
r2b = Road(G, "b", "a", 2, 3600)
r3zb = Road(G, "b", "M", 2, 1800)
r3zM = Road(G, "M", "b", 2, 1800)
r3nM = Road(G, "M", "c", 2, 1800)
r3nc = Road(G, "c", "M", 2, 1800)
r4a = Road(G, "a", "D", 2.5, 3600)
r4D = Road(G, "D", "a", 2.5, 3600)
r5D = Road(G, "D", "e", 3.25, 3600)
r5e = Road(G, "e", "D", 3.25, 3600)
r6D = Road(G, "D", "g", 1.75, 3600)
r6g = Road(G, "g", "D", 1.75, 3600)
r7g = Road(G, "g", "N4", 1, 3600)
r7N4 = Road(G, "N4", "g", 1, 3600)
r8g = Road(G, "g", "h", 0.75, 3600)
r8h = Road(G, "h", "g", 0.75, 3600)
r9h = Road(G, "h", "Am", 1.75, 3600)
r9Am = Road(G, "Am", "h", 1.75, 3600)
r10h = Road(G, "h", "i", 3.25, 3600)
r10i = Road(G, "i", "h", 3.25, 3600)
r11i = Road(G, "i", "j", 2.5, 3600)
r11j = Road(G, "j", "i", 2.5, 3600)
r12j = Road(G, "j", "C", 3.25, 3000)
r12C = Road(G, "C", "j", 3.25, 3000)
r13zh = Road(G, "h", "L", 1.75, 3600)
r13zL = Road(G, "L", "h", 1.75, 3600)
r13nL = Road(G, "L", "k", 1.75, 3600)
r13nk = Road(G, "k", "L", 1.75, 3600)
r14k = Road(G, "k", "An", 1.25, 3600)
r14An = Road(G, "An", "k", 1.25, 3600)
r15k = Road(G, "k", "m", 1, 3600)
r15m = Road(G, "m", "k", 1, 3600)
r16n = Road(G, "n", "o", 1.5, 1800)
r16o = Road(G, "o", "n", 1.5, 1800)
r17o = Road(G, "o", "j", 1.25, 1800)
r17j = Road(G, "j", "o", 1.25, 1800)
r18o = Road(G, "o", "OW", 1.25, 1800)
r18OW = Road(G, "OW", "o", 1.25, 1800)
r19NW = Road(G, "NW", "OW", 2, 1800)
r19OW = Road(G, "OW", "NW", 2, 1800)
r20OW = Road(G, "OW", "z", 1.25, 3600)
r20z = Road(G, "z", "OW", 1.25, 3600)
r21z = Road(G, "z", "r", 4, 1800)
r21r = Road(G, "r", "z", 4, 1800)
r22gg = Road(G, "gg", "ff", 1.75, 1800)
r22ff = Road(G, "ff", "gg", 1.75, 1800)
r23ff = Road(G, "ff", "Z", 1.25, 1800)
r23Z = Road(G, "Z", "ff", 1.25, 1800)
r24Z = Road(G, "Z", "b", 2.5, 1800)
r24b = Road(G, "b", "Z", 2.5, 1800)
r25b = Road(G, "b", "e", 2.5, 1800)
r25e = Road(G, "e", "b", 2.5, 1800)
r26e = Road(G, "e", "f", 0.25, 3600)
r26f = Road(G, "f", "e", 0.25, 3600)
r27f = Road(G, "f", "i", 0.5, 3600)
r27i = Road(G, "i", "f", 0.5, 3600)
r28i = Road(G, "i", "m", 1.25, 3600)
r28m = Road(G, "m", "i", 1.25, 3600)
r29m = Road(G, "m", "n", 1.5, 3600)
r29n = Road(G, "n", "m", 1.5, 3600)
r30n = Road(G, "n", "NW", 1, 3600)
r30NW = Road(G, "NW", "n", 1, 3600)
r31NW = Road(G, "NW", "r", 0.75, 3600)
r31r = Road(G, "r", "NW", 0.75, 3600)
r32r = Road(G, "r", "s", 2.25, 3600)
r32s = Road(G, "s", "r", 2.25, 3600)
r33s = Road(G, "s", "N", 1, 3600)
r33N = Road(G, "N", "s", 1, 3600)
r34N = Road(G, "N", "v", 3, 3600)
r34v = Road(G, "v", "N", 3, 3600)
r35v = Road(G, "v", "N6", 1, 1800)
r35N6 = Road(G, "N6", "v", 1, 1800)
r36v = Road(G, "v", "x", 0.5, 3600)
r36x = Road(G, "x", "v", 0.5, 3600)
r37v = Road(G, "v", "w", 0.5, 1800)
r37w = Road(G, "w", "v", 0.5, 1800)
r38w = Road(G, "w", "x", 0.5, 1800)
r38x = Road(G, "x", "w", 0.5, 1800)
r39w = Road(G, "w", "bb", 4, 1800)
r39bb = Road(G, "bb", "w", 4, 1800)
r40bb = Road(G, "bb", "O", 2.5, 1800)
r40O = Road(G, "O", "bb", 2.5, 1800)
r41O = Road(G, "O", "gg", 2.75, 1800)
r41gg = Road(G, "gg", "O", 2.75, 1800)
r42O = Road(G, "O", "aa", 1.75, 1800)
r42aa = Road(G, "aa", "O", 1.75, 1800)
r43O = Road(G, "O", "cc", 0.5, 1800)
r43cc = Road(G, "cc", "O", 0.5, 1800)
r44cc = Road(G, "cc", "ff", 3.5, 1800)
r44ff = Road(G, "cc", "ff", 3.5, 1800)
r45cc = Road(G, "cc", "aa", 1.5, 1800)
r45aa = Road(G, "aa", "cc", 1.5, 1800)
r46aa = Road(G, "aa", "y", 1.5, 1800)
r46y = Road(G, "y", "aa", 1.5, 1800)
r47y = Road(G, "y", "x", 0.75, 3600)
r47x = Road(G, "x", "y", 0.75, 3600)
r48y = Road(G, "y", "C", 1, 3600)
r48C = Road(G, "C", "y", 1, 3600)
r49aa = Road(G, "aa", "q", 1.25, 1800)
r49q = Road(G, "q", "aa", 1.25, 1800)
r50d = Road(G, "d", "cc", 1.25, 1800)
r50cc = Road(G, "cc", "d", 1.25, 1800)
r51z = Road(G, "z", "C", 0.5, 3600)
r51C = Road(G, "C", "z", 0.5, 3600)
r52C = Road(G, "C", "q", 0.5, 3600)
r52q = Road(G, "q", "C", 0.5, 3600)
r53q = Road(G, "q", "d", 2, 1800)
r53d = Road(G, "d", "q", 2, 1800)
r54d = Road(G, "d", "c", 0.5, 3600)
r54c = Road(G, "c", "d", 0.5, 3600)
r55c = Road(G, "c", "Z", 3.75, 3600)
r55Z = Road(G, "Z", "c", 3.75, 3600)
r56d = Road(G, "d", "p", 1.5, 1800)
r56p = Road(G, "p", "d", 1.5, 1800)
r57p = Road(G, "p", "f", 1.25, 1800)
r57f = Road(G, "f", "p", 1.25, 1800)
r58p = Road(G, "p", "j", 2, 1800)
r58j = Road(G, "j", "p", 2, 1800)
r59N = Road(G, "N", "u", 2, 3600)
r59u = Road(G, "u", "N", 2, 3600)
r60u = Road(G, "u", "A", 0.5, 3600)
r60A = Road(G, "A", "u", 0.5, 3600)
r61s = Road(G, "s", "t", 3, 1800)
r61t = Road(G, "t", "s", 3, 1800)
r62t = Road(G, "t", "u", 1.25, 1800)
r62u = Road(G, "u", "t", 1.25, 1800)
r63t = Road(G, "t", "A5", 1.75, 1800)
r63A5 = Road(G, "A5", "t", 1.75, 1800)

nx.draw_spring(G, with_labels=True)
#plt.show()

locations = ["D", "L", "C", "M", "NW", "N", "O", "OW", "Z",
             "Az", "Am", "An", "N4", "Am", "M", "N6", "A5", "A"]

ftt_matrix = np.zeros([18,18])
itt = [4, 4, 4, 7, 4, 5, 4, 3, 3] #internal travel time
diags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 10**100, 10**100, 10**100, 10**100, 10**100, 10**100, 10**100, 10**100, 10**100]
ett = [30, 40, 45, 10, 30, 10, 30, 45, 15] #external travel time
for i in range(len(locations)):
    row = []
    for j in range(len(locations)):
        row.append(nx.dijkstra_path_length(G, locations[i], locations[j], weight="weight"))
    ftt_matrix[i] = row
np.fill_diagonal(ftt_matrix, diags)
(ftt_matrix[9,10], ftt_matrix[10,9], ftt_matrix[9,11], ftt_matrix[11,9], ftt_matrix[10,11], ftt_matrix[11,10],
 ftt_matrix[16,17], ftt_matrix[17, 16]) = 10**100, 10**100, 10**100, 10**100, 10**100, 10**100, 10**100, 10**100,

att_matrix = ftt_matrix

for i in range(1):
    dist_matrix = att_to_dist(att_matrix, itt, ett)
    dtt_data = pd.DataFrame(dist_matrix, columns=labels, index=labels)
    for j in range(len(roadlist)): roadlist[j].va = 0

    weerstand = np.e**(-beta*dist_matrix)
    iteration = iterate(weerstand)
    for j in range(10000):
        iteration = iterate(iteration)
    dist_results = iteration
    dist_data = pd.DataFrame(iteration, columns=labels, index=labels)

    att_matrix = route_assignment(dist_results/24, 100)
    np.fill_diagonal(att_matrix, diags)
    (att_matrix[9, 10], att_matrix[10, 9], att_matrix[9, 11], att_matrix[11, 9], att_matrix[10, 11], att_matrix[11, 10],
     att_matrix[16, 17],
     att_matrix[17, 16]) = 10 ** 100, 10 ** 100, 10 ** 100, 10 ** 100, 10 ** 100, 10 ** 100, 10 ** 100, 10 ** 100,
    print("loop", i)

print(dtt_data)
print(dist_data)


singles = ["z", "C", "y", "x", "v"]
singles_names = ["Nassau", "Oranje", "Oranje", "Sint Canisius"]
through_traffic = 0
for i in range(len(singles)-1):
    for m in range(len(roadlist)):
        if singles[i] == roadlist[m].node1 and singles[i + 1] == roadlist[m].node2:
            through_traffic += roadlist[m].va * 24
            print(f"Intensity {singles_names[i]}singel equals {roadlist[m].va} per hour and {roadlist[m].va*24} per day")
        elif singles[i + 1] == roadlist[m].node1 and singles[i] == roadlist[m].node2:
            through_traffic += roadlist[m].va * 24
            print(f"Intensity {singles_names[i]}singel equals {roadlist[m].va} per hour and {roadlist[m].va*24} per day")
print(through_traffic / 4)

s100 = ["gg", "ff", "Z", "b", "e", "f", "i", "m", "n", "NW", "r", "s", "N", "v"]
s100_traffic_zn = 0
s100_traffic_nz = 0
for i in range(len(s100)-1):
    for m in range(len(roadlist)):
        if s100[i] == roadlist[m].node1 and s100[i + 1] == roadlist[m].node2:
            s100_traffic_zn += roadlist[m].va
            print(f"Verkeer tussen {s100[i]} en {s100[i + 1]}")
            print(roadlist[m].va)
        elif s100[i + 1] == roadlist[m].node1 and s100[i] == roadlist[m].node2:
            s100_traffic_nz += roadlist[m].va
            print(roadlist[m].va)
print(f"Zuid noord is {s100_traffic_zn} en noord zuid is {s100_traffic_nz}")

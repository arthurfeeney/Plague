
# Plague
### A Web Crawler

Not much at the moment... can crawl webpages for absolute and "/xyz/..." urls pretty well. 

(Kept the graphs small for now because they take a while to draw on my laptop.)   
Both used stackoverflow.com as the seed but use different frontiers.  

FIFOFrontier (esssentially does a breadth first search):
![Small Stackoverflow](/image/stackoverflow_graph.png)

DomainPriorityFrontier (prioritizes looking at domains not seen in a while):
![dpf stackoverflow](/image/stackoverflow_dpf_graph4.png)

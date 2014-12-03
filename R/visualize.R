library(arulesViz)

plot(itemsets , method="paracoord", control=list(main="Parallel coordinates plot, Certified=0", reorder=TRUE))

plot(itemsets , method="graph", control=list(main="Certified=0"))



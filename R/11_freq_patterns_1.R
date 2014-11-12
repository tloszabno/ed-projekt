library(arules)

#data <- list(select course_id, user_id, region_id, explored from users_on_courses where certified = 1)

res <- dbSendQuery(con, "SELECT course_id, user_id, region_id, explored from users_on_courses where certified = 1 limit 7") 
#res <- dbSendQuery(con, "SELECT grade from users_on_courses where certified = 1") 

dataList <- dbFetch(res)
dbClearResult(res)

col_1 <- as.factor(dataList$course_id)
dataList$course_id <- col_1

col_2 <- as.factor(dataList$user_id)
dataList$user_id <- col_2

col_3 <- as.factor(dataList$region_id)
dataList$region_id <- col_3

col_4 <- as.factor(dataList$explored)
dataList$explored <- col_4

## Mine itemsets with tidLists.
f <- eclat(dataList , parameter = list(support = 0.3, tidLists = TRUE))
 
## Get dimensions of the tidLists.
dim(tidLists(f))
 
## Coerce tidLists to list.
as(tidLists(f), "list")
 
## Inspect visually.
image(tidLists(f))
 
##Show the Frequent itemsets and respectives supports
inspect(f)
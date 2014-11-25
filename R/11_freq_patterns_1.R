library(arules)

#data <- list(select course_id, user_id, region_id, explored from users_on_courses where certified = 1)

res <- dbSendQuery(con, "SELECT region_id, viewed, explored, grade_normalized, number_of_played_videos_normalized, number_of_interactions_normalized, number_of_activity_days_normalized FROM users_on_courses WHERE certified=0 ") # LIMIT 1000") 
#res <- dbSendQuery(con, "SELECT grade from users_on_courses where certified = 1") 

dataList <- dbFetch(res)
dbClearResult(res)

col_0 <- as.factor(dataList$region_id)
dataList$region_id<- col_0

col_1 <- as.factor(dataList$viewed)
dataList$viewed <- col_1

col_2 <- as.factor(dataList$explored)
dataList$explored <- col_2

col_3 <- as.factor(dataList$grade_normalized)
dataList$grade_normalized<- col_3

col_4 <- as.factor(dataList$number_of_played_videos_normalized)
dataList$number_of_played_videos_normalized<- col_4

col_5 <- as.factor(dataList$number_of_interactions_normalized)
dataList$number_of_interactions_normalized<- col_4

col_6 <- as.factor(dataList$number_of_activity_days_normalized)
dataList$number_of_activity_days_normalized<- col_4


## Mine itemsets with tidLists.
f <- eclat(dataList , parameter = list(support = 0.3, tidLists = TRUE, minlen=4))
 
## Get dimensions of the tidLists.
#dim(tidLists(f))
 
## Coerce tidLists to list.
#as(tidLists(f), "list")
 
## Inspect visually.
#image(tidLists(f))
 
##Show the Frequent itemsets and respectives supports
inspect(f)
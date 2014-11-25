res <- dbSendQuery(con, "SELECT number_of_interactions, number_of_activity_days, number_of_played_videos FROM users_on_courses") 
#res <- dbSendQuery(con, "SELECT * FROM users_on_courses") 

dataList <- dbFetch(res)
dbClearResult(res)

summary(dataList)

res <- dbSendQuery(con, "SELECT number_of_played_videos FROM users_on_courses") 
#res <- dbSendQuery(con, "SELECT * FROM users_on_courses") 

dataList <- dbFetch(res)
dbClearResult(res)

summary(dataList)

res <- dbSendQuery(con, "SELECT number_of_activity_days FROM users_on_courses") 
#res <- dbSendQuery(con, "SELECT * FROM users_on_courses") 

dataList <- dbFetch(res)
dbClearResult(res)

summary(dataList)

res <- dbSendQuery(con, "SELECT number_of_interactions FROM users_on_courses") 
#res <- dbSendQuery(con, "SELECT * FROM users_on_courses") 

dataList <- dbFetch(res)
dbClearResult(res)

summary(dataList)


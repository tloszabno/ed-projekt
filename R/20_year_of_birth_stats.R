
res <- dbSendQuery(con, "SELECT year_of_birth FROM users WHERE year_of_birth is not NULL AND year_of_birth != 'NA'") 
dataList <- dbFetch(res)
dbClearResult(res)
users_year_of_birth <- (as.numeric(dataList$year_of_birth))
summary(users_year_of_birth)
hist(users_year_of_birth)

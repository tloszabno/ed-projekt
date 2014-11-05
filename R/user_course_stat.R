title <- "Users number in course"

res <- dbSendQuery(con, "select course_id, count(userid_di) from raw_data group by course_id")
data <- dbFetch(res)
barplot(data[,2], names.arg=data[,1], col=c("red", "yellow", "blue", "green"))
title(main = title, font.main = 4)

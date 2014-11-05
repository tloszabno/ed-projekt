title <- "Gender count"

res <- dbSendQuery(con, "select gender, count(*) from raw_data group by gender")
data <- dbFetch(res)
barplot(data[,2], names.arg=data[,1], col=c("red", "yellow", "blue", "green"))
title(main = title, font.main = 4)

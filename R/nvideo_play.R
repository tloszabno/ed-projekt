title <- "nvideo play stats for certified=1"

res <- dbSendQuery(con, "SELECT number_of_played_videos FROM users_on_courses WHERE number_of_played_videos IS NOT NULL AND certified = 1") 
data <- dbFetch(res)
boxplot(data)

title(main = title, font.main = 4, ylab="number of video plays")
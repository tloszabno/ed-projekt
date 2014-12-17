library(party)

res <- dbSendQuery(con,
'SELECT u_o_c.grade_normalized AS "Grade",
usr.year_of_birth AS "Age", 
u_o_c.number_of_interactions_normalized AS "Interactions",
u_o_c.number_of_activity_days_normalized AS "Activity_Days",
u_o_c.number_of_played_videos_normalized AS "Played_Videos",
u_o_c.certified AS "Certified"
FROM users AS usr
JOIN education_levels AS edu_lvl ON usr.education_level_id = edu_lvl.id
JOIN genders AS gend ON usr.gender_id = gend.id
JOIN users_on_courses AS u_o_c ON u_o_c.user_id = usr.id
JOIN courses AS courses_tab ON courses_tab.id = u_o_c.course_id
JOIN periods AS periods_tab ON periods_tab.id = courses_tab.period_id
JOIN regions AS regions_tab ON regions_tab.id = u_o_c.region_id
AND usr.year_categorized IS NOT NULL ')


dataList <- dbFetch(res)
dbClearResult(res)

col_4 <- as.factor(dataList$Grade)
dataList$Grade<- col_4

col_3 <- as.factor(dataList$Age)
dataList$Age<- col_3

col_5 <- as.factor(dataList$Interactions)
dataList$Interactions<- col_5

col_6 <- as.factor(dataList$Activity_Days)
dataList$Activity_Days<- col_6

col_7 <- as.factor(dataList$Played_Videos)
dataList$Played_Videos<- col_7

col_11 <- as.factor(dataList$Certified)
dataList$Certified<- col_11

numData = data.matrix(dataList)
pcares <- prcomp(numData, scale = TRUE, center=TRUE)
summary(pcares)
print(pcares)

plot(pcares, type="l")


library(ggbiplot)
g <- ggbiplot(pcares, obs.scale = 1, var.scale = 1, ellipse = TRUE, 
              circle = TRUE)
g <- g + scale_color_discrete(name = '')
g <- g + theme(legend.direction = 'horizontal', 
               legend.position = 'top')
print(g)


library(party)

res <- dbSendQuery(con, 'SELECT edu_lvl.name AS "Education",
gend.name AS "Gender",
usr.year_categorized AS "Age", 
u_o_c.grade_normalized AS "Grade",
u_o_c.number_of_interactions_categorized AS "Interactions",
u_o_c.number_of_activity_days_categorized AS "Activity_Days",
u_o_c.number_of_played_videos_categorized AS "Played_Videos",
periods_tab.name AS "Course_Start",
courses_tab.name AS "Course_Name",
courses_tab.year AS "Course_Year",
regions_tab.name AS "Region"
FROM users AS usr
JOIN education_levels AS edu_lvl ON usr.education_level_id = edu_lvl.id
JOIN genders AS gend ON usr.gender_id = gend.id
JOIN users_on_courses AS u_o_c ON u_o_c.user_id = usr.id
JOIN courses AS courses_tab ON courses_tab.id = u_o_c.course_id
JOIN periods AS periods_tab ON periods_tab.id = courses_tab.period_id
JOIN regions AS regions_tab ON regions_tab.id = u_o_c.region_id
AND usr.year_categorized IS NOT NULL')


dataList <- dbFetch(res)
dbClearResult(res)

col_1 <- as.factor(dataList$Education)
dataList$Education<- col_1

col_2 <- as.factor(dataList$Gender)
dataList$Gender<- col_2


col_3 <- as.factor(dataList$Age)
dataList$Age<- col_3


col_4 <- as.factor(dataList$Grade)
dataList$Grade<- col_4


col_5 <- as.factor(dataList$Interactions)
dataList$Interactions<- col_5


col_6 <- as.factor(dataList$Activity_Days)
dataList$Activity_Days<- col_6


col_7 <- as.factor(dataList$Played_Videos)
dataList$Played_Videos<- col_7


col_8 <- as.factor(dataList$Course_Start)
dataList$Course_Start<- col_8


col_9 <- as.factor(dataList$Course_Name)
dataList$Course_Name<- col_9


col_10 <- as.factor(dataList$Course_Year)
dataList$Course_Year<- col_10


col_11 <- as.factor(dataList$Region)
dataList$Region<- col_11


# k-means clustering - nie dziala...
#newData <- dataList
#newData$Certified <- NULL
#(kc <- kmeans(newData, 3))

# hierarchical
#idx <- sample(1:dim(dataList)[1], 40)
#dataSample <- dataList[idx,]
#dataSample$Certified <- NULL
#hc <- hclust(dist(dataSample), method="ave")

library(fpc)
library(cluster)
pamk.result <- pamk(dataList)

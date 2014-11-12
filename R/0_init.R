library(RPostgreSQL)

con <- dbConnect(dbDriver("PostgreSQL"), user="postgres", password="postgres", dbname="ed",host="127.0.0.1",port=9876)


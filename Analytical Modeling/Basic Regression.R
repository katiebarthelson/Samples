# Homework 5
# ISYE6501 - Regression
library(DAAG)
crimedata <- read.table("uscrime.txt",header=TRUE)
# Build a regression model
model <- lm(Crime~ M+So+Ed+Po1+Po2+LF+M.F+Pop+NW+U1+U2+Wealth+Ineq+Prob+Time, data=crimedata)
model
summary(model)
par(mar=c(1,1,1,1))
# plot(model)
# Build data frame for prediction data
citydata <- as.data.frame(c(
                          M=14,
                          So=0,
                          Ed = 10.0,
                          Po1 = 12.0,
                          Po2 = 15.5,
                          LF = 0.640,
                          M.F = 94.0,
                          Pop = 150,
                          NW =  1.1,
                          U1 = 0.120,
                          U2 =  3.6,
                          Wealth = 3200,
                          Ineq = 20.1,
                          Prob = 0.04,
                          Time = 39.0))
citydata <- as.data.frame(t(citydata),row.names = "City X")
colnames(citydata)<-colnames(crimedata)[1:15]
# predict the crime rate for the test data city
prediction <- predict(model,citydata)
prediction
# try cv.lm for cross validation
par(mar=c(1,0,2,0))
model2 <- cv.lm(Crime~ M+So+Ed+Po1+Po2+LF+M.F+Pop+NW+U1+U2+Wealth+Ineq+Prob+Time, data=crimedata)
model3 <- lm(cvpred~ M+So+Ed+Po1+Po2+LF+M.F+Pop+NW+U1+U2+Wealth+Ineq+Prob+Time, data=model2)
model3
prediction2 <- predict(model3,citydata)
prediction2
plot(model3)
summary(model3)

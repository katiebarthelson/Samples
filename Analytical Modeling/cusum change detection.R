# ISYE6501 Homework Week 3
# Question 5.1 -------------------------------------------------------------------
# Load the librariesand read in the data
library(outliers)
library(ggplot2)
crimeData = as.data.frame(read.csv("uscrime.csv",header=TRUE))
set.seed(1)
# test to see whether or not there are any outliers in the last column
grubbs.test(crimeData$Crime,type=10, two.sided = FALSE)
grubbs.test(crimeData$Crime,type=11,two.sided = FALSE)
# grubbs.test(crimeData$Crime,type=20,two.sided = FALSE)
par(mar=c(1,1,1,1))
boxplot(crimeData$Crime,main = "US Crime",ylab="Crime Rate")
hist(crimeData$Crime,main = "US Crime" ,xlab="Crime Rate")
# -------------------------------------------------------------------------------
# Question 6.1
library(cusum)
library(qcc)
library(dplyr)
temps = as.data.frame(read.csv("temps.csv",header=TRUE))
# Use a CUSUM approach to identify when unofficial summer ends
temps_daily <- mutate(temps,daily_avg=rowMeans(temps[,-1],na.rm=TRUE))
daily_xbb = mean(as.numeric(temps_daily$daily_avg))
q1 <- qcc(temps_daily[1:87,2:21], type="xbar" , newdata = temps_daily[88:123,2:21],confidence.level = 0.95)
# q2 <- qcc(temps[2:21,],type="R",confidence.level = 0.95)
q2 <- cusum(failure_probability = 0.05, temps,limit=2.96)
summary(q2)
plot(q2, chart.all=FALSE)
# Make a judgment of whether Atlanta's summer climate has gotten warmer
yearly_temps <- temps
yearly_temps["yearly_avg",(2:21)]<-colMeans(yearly_temps[2:21,-1],na.rm=TRUE)
q2 <- qcc(yearly_temps[1:123,2:21], type="xbar",confidence.level = 0.95)
yearly_xbb = mean(as.numeric(yearly_temps$yearly_avg),na.rm = TRUE)

# Western Electric Rules for Reference:
# Rule 1 :- One or more points beyond the control limits
# Rule 2 :- 8/9 points on the same size of the center line.
# Rule 3 :- 6 consecutive points are steadily increasing or decreasing.
# Rule 4 :- 14 consecutive points are alternating up and down.
# Rule 5 :- 2 out of 3 consecutive points are more than 2 sigmas from the center line in the same direction.
# Rule 6 :- 4 out of 5 consecutive points are more than 1 sigma from the center line in the same direction.
# Rule 7 :- 15 consecutive points are within 1 sigma of the center line
# Rule 8 :- 8 consecutive points on either side of the center line with not within 1 sigma.

# Homework 4 ISYE 6501
# 7.2 Build an exponential smoothing model to help make a judgement
# of whether the unofficial end of summer has gotten later over the last 20 years
library(cusum)
library(qcc)
library(dplyr)
# Read in the data
temps = as.data.frame(read.table("temps.txt",header=TRUE))
r_names = as.data.frame(temps[1:123,1])
row.names(temps) <- temps[,1]
#convert all data to one dimensional wrap-around frame
temps_vect <- as.vector(unlist(temps[,2:21]))
# convert vector to a time series object (understands time units)
# frequency is agnostic to actual physical time (full year is not a cycle)
temps_ts <- ts(temps_vect,start=1996,frequency=123)
plot(temps_ts,main="Time Series",ylab="Temperature (F)")
# perform exponential smoothing.
# Additive has lower sse, meaning - as temps get warmer, the temp swings don't necessarily get more extreme
temps_HW <- HoltWinters(temps_ts,alpha=NULL,beta=NULL,gamma=NULL,seasonal=c("additive","multiplicative"))
temps_HW$alpha
temps_HW$beta
temps_HW$gamma
plot(temps_HW,ylab="Observed/Fitted Temperature")
summary(temps_HW)

# Analyze the Holt Winters Model
fitted_output <- temps_HW$fitted # "x-hat = Smoothed model"
head(temps_HW$fitted)
tail(temps_HW$fitted)
temps_HW_sf <- matrix(temps_HW$fitted[,4],nrow=123)
smoothed <- matrix(fitted_output[1:2337,1])

# index the smoothed DF to separate the data back into years 
# (e.g. ts_object[1:123])
# use the cbind function to combine the vectors into a data frame
smoothed_day <- as.data.frame(t(smoothed[1:19,]))
x1=20
for(day in 2:123){
  x2=day*19
  row_yr = t(smoothed[x1:x2,])
  smoothed_day <- merge(smoothed_day,row_yr,all.x=TRUE,all.y = TRUE)
  x1=x2+1
}
smoothed_day
row.names(smoothed_day) <- temps[,1]
head(smoothed_day)
smoothed_ts <- ts(smoothed_day,start=1997,end=2015,frequency = 123)
plot(as.vector(unlist(smoothed_ts[1:19,])),main="Smoothed Data",ylab="Temperature")

# use the smoothed model with cusum to detect change
q2 <- cusum(smoothed_day[1:34,1:19],failure_probability = 0.05, newdata = smoothed_day[35:123,1:19],limit=2.96,main="Cusum Chart Using July as Calibration Data")
summary(q2)
# -----------------------------------------------------------------
# year to year
smoothed_yr <- t(smoothed_day)
q3 <- cusum(smoothed_yr[1:10,],failure_probability = 0.05, newdata = smoothed_yr[11:19,],limit=2.96,main="Cusum Chart Using July as Calibration Data")
summary(q3)

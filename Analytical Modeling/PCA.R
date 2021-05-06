# Homework 6
# ISYE6501
library(DAAG)
library(GGally)
crimedata <- read.table("uscrime.txt",header=TRUE)
ggpairs(crimedata,columns=c("Po1","Po2","U1","Ineq"))
# Run PCA on scaled data. This will rotate the data.
# scale: subtract the mean and divide the standard deviation
# exclude response variable
PCA <- prcomp(crimedata[,1:15],scale=TRUE)
summary(PCA)
# Obtain the matrix of eigenvectors
# use this matrix to rotate the data back and obtain original coefficients
PCA$rotation
# use the screenplot function to plot the variances of each principal component
# where variance = pca$sdev^2 to determine the number of principal components to use
par(mar=c(1,1,1,1))
screeplot(PCA,type="lines",col="blue")
# Get first 4 principal components
PC <- PCA$x[,1:4]
PC
# Multiply by the std dev and add the mean
# take variable (M) in rotation matrix and multiply the row by PC
# add the PC values together and subtract the mean, divide by stdev
# this will give you the equivalent of the first value of M

# build a linear regression model with the first 4 P.C
uscrimePC <- cbind(PC,crimedata[,16]) # pull the response variable back in
modelPCA <- lm(V5~.,data=as.data.frame(uscrimePC))
summary(modelPCA)

# Get the betas from this PC regression model and transform them into the
# alphas that are in terms of the original scaled variables
# Then, from there you can unscale the coefficients to get them in terms of
# the original unscaled coefficients. This is needed to make a prediction
# for the new point given. This requires matrix multiplication.
# compute and compare R^2 value, adj R^2 or CV R^2

# write the coefficients in terms of the original factors
# regression coefficients are bk. multiple these by the rotation vector
# unscale the data.
mu <- colMeans(PC)
Xhat <- (PCA$x %*% t(PCA$rotation))*(1/PCA$scale)+PCA$center
Xhat[1,]
# add back the response variable
newframe <- as.data.frame(cbind(Xhat,crimedata[,16]))
colnames(newframe)<-colnames(crimedata)[1:16]
newmodel <- lm(Crime~ M+So+Ed+Po1+Po2+LF+M.F+Pop+NW+U1+U2+Wealth+Ineq+Prob+Time, data = newframe)
summary(newmodel)
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
prediction <- predict(newmodel,citydata)
prediction
# try cv.lm for cross validation
par(mar=c(1,0,2,0))
model2 <- cv.lm(Crime~ M+So+Ed+Po1+Po2+LF+M.F+Pop+NW+U1+U2+Wealth+Ineq+Prob+Time, data=newframe)
model3 <- lm(cvpred~ M+So+Ed+Po1+Po2+LF+M.F+Pop+NW+U1+U2+Wealth+Ineq+Prob+Time, data=model2)
model3
prediction2 <- predict(model3,citydata)
prediction2
plot(model3)
summary(model2)
summary(model3)

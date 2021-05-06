# ISYE6501 Homework Week 2
# Question 3.1 part a -------------------------------------------------------------------
# Load the librariesand read in the data
library(kknn)
library(kernlab)
library(cluster) 
myData = read.csv("credit_card_data-headers.csv",header=TRUE)
set.seed(1)
# head(myData)
#myData <- read.table("credit_card_data.txt", stringsAsFactors = FALSE, header = FALSE)
# split a random sample of data
m <- dim(myData)[1] 
#val <- sample(1:m, size = round(m/3), replace = FALSE,prob = rep(1/m, m))
val <- sample.int(n=nrow(myData), size = floor(.80*nrow(myData)), replace = FALSE)
# Split the whole dataset into 2 distinct sets: data1 and data2
data1 <- myData[-val,]
data2 <- myData[val,]
# perform cross validation and find the best value of k ~ train.kknn is leave one out
model11 = train.kknn(R1~., data = data1,maxk = 100, kernel = c("triangular", "gaussian", "rectangular", "epanechnikov", "optimal"), scale=TRUE)
model11
# train the chosen model against all of data 1 and validate the model based on data2
prediction <- predict(model11,data1)
bin<-round(prediction)
accuracy1 = sum(bin==data2$R1)/length(data2$R1)
accuracy1
# perform cross validation and find the best value of k ~ cv.kknn is k-fold. in this case 4-fold
model2 = cv.kknn(R1~.,data=data1,2,"rectangular", scale=TRUE)
model2
results <- fitted(model2)
bin2<-round(results)
accuracy2 = (sum(bin2==data2$R1))/length(data2$R1)
accuracy2
# Question 3.1 Part b-----------------------------------------------------------------------------------------------------
# Using kknn - split into training, test, and validation sets
g <- sample(1:3, size = 3, prob = c(.6,.2,.2), replace = FALSE)
data1a <- myData[g==1,]
data2a <- myData[g==2,]
data3a <- myData[g==3,]
#spec = c(train = .6, test = .2, validate = .2)
#g = sample(cut(seq(nrow(myData)),nrow(myData)*cumsum(c(0,spec)),labels = names(spec)))
#res = split(myData, g)
#sapply(res, nrow)/nrow(myData)
## Split the whole dataset
#train_data <- as.data.frame(res[1])
#test_data <- as.data.frame(res[2])
#valid_data <- as.data.frame(res[3])
# perform cross validation and find the best value of k ~ train.kknn is leave one out
combo1 = train.kknn(R1~., data = data1a,maxk = 100, kernel = c("triangular", "gaussian", "rectangular", "epanechnikov", "optimal"), scale=TRUE)
combo2 = train.kknn(R1~., data = data2a,maxk = 100, kernel = c("triangular", "gaussian", "rectangular", "epanechnikov", "optimal"), scale=TRUE)
combo3 = train.kknn(R1~., data = data3a,maxk = 100, kernel = c("triangular", "gaussian", "rectangular", "epanechnikov", "optimal"), scale=TRUE)
combo1
combo2
combo3
# test the model based on the test set
predictionc1 <- predict(combo1,data2a) #train 1a, test 2a, validate 3a
binc1<-round(predictionc1)
predictionc2 <- predict(combo2,data3a) #train 2a, test 3a, validate 1a
binc2<-round(predictionc2)
predictionc3 <- predict(combo3,data1a) #train 3a, test 1a, validate 2a
binc3<-round(predictionc3)
# validate the model based on the validation set
accuracyc1 = sum(binc1==data3a$R1)/length(data3a$R1)
accuracyc1
accuracyc2 = sum(binc2==data1a$R1)/length(data1a$R1)
accuracyc2
accuracyc3 = sum(binc3==data2a$R1)/length(data2a$R1)
accuracyc3
# ------------------------------------------------------------------------------------------------------------------------
# Use k-means clustering on the file "iris"
myData2 <- read.csv("iris.csv",header=TRUE)
myData2
for(x in 1:6){
  k <- kmeans(as.matrix(myData2[,1:5]),centers=x,nstart=25)
  attributes(k)
  clusplot(myData2, k$cluster, color=TRUE, shade=TRUE, labels=x, lines=0)
}
k1 <- kmeans(as.matrix(myData2[,1:5]),centers=1,nstart=25)
table(k1$cluster,iris[,"Species"])
k2 <- kmeans(as.matrix(myData2[,1:5]),centers=2,nstart=25)
table(k2$cluster,iris[,"Species"])
k3 <- kmeans(as.matrix(myData2[,1:5]),centers=3,nstart=25)
table(k3$cluster,iris[,"Species"])
k4 <- kmeans(as.matrix(myData2[,1:5]),centers=4,nstart=25)
table(k4$cluster,iris[,"Species"])
k5 <- kmeans(as.matrix(myData2[,1:5]),centers=5,nstart=25)
table(k5$cluster,iris[,"Species"])
#using the elbow method
set.seed(1)
# Compute and plot wss for k = 1 to k = 6.
wss <- sapply(1:6, function(k){kmeans(as.matrix(myData2[,1:5]), k, nstart=25,)$tot.withinss})
wss
plot(1:6, wss,type="b", pch = 19, frame = FALSE,xlab="Number of clusters K", ylab="Total within-clusters sum of squares")

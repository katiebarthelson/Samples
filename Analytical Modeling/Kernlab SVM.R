# Katie Barthelson's HW1------------------------------------------------------
# Question 2.2 #1 KSVM-----------------------------------------------------------
#### Read data into R ####
library(kernlab)
myData=read.csv("credit_card_data-headers.csv",header=TRUE)
set.seed(1)
#### Display myData ####
# myData
# call ksvm. Vanilladot is a simple linear kernel.
model1 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="vanilladot",C=100,scaled=TRUE)
model1
# calculate a1…am
a <- colSums(model1@xmatrix[[1]] * model1@coef[[1]])
a
# calculate a0
a0 <- model1@b
a0
# see what the model predicts
pred1 <- predict(model1,myData[,1:10])
pred1
# see what fraction of the model’s predictions match the actual classification
sum(pred1 == myData[,11]) / nrow(myData)
#Test other values of C
model1a <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="vanilladot",C=1000,scaled=TRUE)
model1a
pred1a <- predict(model1a,myData[,1:10])
pred1a
sum(pred1a == myData[,11]) / nrow(myData)
model1b <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="vanilladot",C=10000,scaled=TRUE)
model1b
pred1b <- predict(model1b,myData[,1:10])
pred1b
sum(pred1b == myData[,11]) / nrow(myData)
model1c <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="vanilladot",C=1,scaled=TRUE)
model1c
pred1c <- predict(model1c,myData[,1:10])
pred1c
sum(pred1c == myData[,11]) / nrow(myData)
model1d <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="vanilladot",C=100000,scaled=TRUE)
model1d
pred1d <- predict(model1d,myData[,1:10])
pred1d
sum(pred1d == myData[,11]) / nrow(myData)
#---------------------------------------------------------------------------
# Question 2.2 #2 Bonus - use other kernels
# rbfdot
model2 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="rbfdot",C=100,scaled=TRUE)
pred2 <- predict(model2,myData[,1:10])
model2
pred2
sum(pred2 == myData[,11]) / nrow(myData)
# polydot
model3 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="polydot",C=100,scaled=TRUE)
pred3 <- predict(model3,myData[,1:10])
model3
pred3
sum(pred3 == myData[,11]) / nrow(myData)
# tanhdot
model4 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="tanhdot",C=100,scaled=TRUE)
pred4 <- predict(model4,myData[,1:10])
model4
pred4
sum(pred4 == myData[,11]) / nrow(myData)
# laplacedot
model5 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="laplacedot",C=100,scaled=TRUE)
pred5 <- predict(model5,myData[,1:10])
model5
pred5
sum(pred5 == myData[,11]) / nrow(myData)
# besseldot
model6 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="besseldot",C=100,scaled=TRUE)
pred6 <- predict(model6,myData[,1:10])
model6
pred6
sum(pred6 == myData[,11]) / nrow(myData)
# anovadot
model7 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="anovadot",C=100,scaled=TRUE)
pred7 <- predict(model7,myData[,1:10])
model7
pred7
sum(pred7 == myData[,11]) / nrow(myData)
# splinedot
model8 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="splinedot",C=100,scaled=TRUE)
pred8 <- predict(model8,myData[,1:10])
model8
pred8
sum(pred8 == myData[,11]) / nrow(myData)
# matrix
# model9 <- ksvm(as.matrix(myData[,1:10]),as.factor(myData[,11]),type="C-svc",kernel="matrix",C=100,scaled=TRUE)
# pred9 <- predict(model9,myData[,1:10])
# -------------------------------------------------------------------------
# Question 2.2 #3 -------------------------------------------------------------
## Find a good value for k
library(kknn)
myData = as.data.frame(myData)
# m <- dim(myData)[1]
# val <- sample(1:m, size = round(m/3), replace = FALSE,prob = rep(1/m, m)) #R documentation method - what do these terms mean?
# myData.learn <- myData[-val,]
# myData.valid <- myData[val,]
set.seed(1)
check_accuracy = function(X){
  predicted <- rep(0,(nrow(myData)))
  for (i in 1:nrow(myData)){
    model10 = kknn(R1~.,myData[-i,],myData[i,],k=X, scale = TRUE)
    predicted[i] <- as.integer(fitted(model10)+0.5)
  }
  acc = (sum(predicted == myData[,-1])) / nrow(myData)
  return(acc)
}
accurracy=rep(0,50)
for (X in 1:50){
  accurracy[X] = check_accuracy(X)
}
plot(accurracy)
title("K-Nearest-Neighbors")
# Using train.kknn---------------
m <- dim(myData)[1]
val <- sample(1:m, size = round(m/3), replace = FALSE,prob = rep(1/m, m))
myData.learn <- myData[-val,]
myData.valid <- myData[val,]
model11 = train.kknn(formula = R1~., data = myData.learn,maxk = 100, kernel = c("triangular", "gaussian", "rectangular", "epanechnikov", "optimal"), scale=TRUE)
model11
## Show how well it classifies the data points in the full data set-----------
prediction <- predict(model11,myData.valid)
bin<-round(prediction)
prediction_accuracy<-table(bin,myData.valid$R1)
prediction_accuracy
sum(bin==myData.valid$R1)/length(myData.valid$R1)
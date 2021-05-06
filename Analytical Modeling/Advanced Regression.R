# ISYE 6501 HW 8
# Question 11.1 - Using the crime data set uscrime.txt from Questions 8.2, 9.1, and 10.1, 
# build a regression model using:
#  1. Stepwise regression
#  2. Lasso
#  3. Elastic net
# For Parts 2 and 3, remember to scale the data first ¡V otherwise, the regression 
# coefficients will be on different scales and the constraint won¡¦t have the desired effect.
# For Parts 2 and 3, use the glmnet function in R.
set.seed(1)
library(leaps)
library(glmnet)
library(caret)
crimedata <- read.table("uscrime.txt",header=TRUE)
# split into train and test
train = sample(1:nrow(crimedata), nrow(crimedata)*.8)
crime.train = crimedata[train,1:16]
crime.test = crimedata[-train,1:16]
# Stepwise
# set up repeated k-fold cross validation
train.control <- trainControl(method="cv",number=10)
# Train the model
step.model <- train(Crime~.,data=crime.train,method="leapSeq",tuneGrid=data.frame(nvmax=1:15),trControl=train.control)
# Obtain model results
step.model$results
# Obtain best number of tuning values (variables)
step.model$bestTune
# Obtain final model results and coefficients
summary(step.model$finalModel)
coef(step.model$finalModel, 5)
# Create a linear model from the chosen predictors
final <- lm(Crime~M+Ed+Po1+U2+Ineq,data=crime.train)
# Test the model
pred <- predict(final,crime.test)
pred
# Stepwise
swise <- lm(Crime~.,data=crimedata)
step(swise,
     scope=list(lower=formula(lm(Crime~1,data=crimedata)),
            upper=formula(lm(Crime~.,data=crimedata))),
     direction="both")
# Lasso
# obtain a lasso model with scaled data
lasso <- cv.glmnet(x=as.matrix(crimedata[,-16]),y=as.matrix(crimedata[,16]),# alpha is 1 for lasso
                   alpha = 1,nfolds=8,nlambda=20,type.measure = "mse",family="gaussian",standardize=TRUE)
lasso
plot(lasso,main="Lasso Model")
lasso$lambda.min
cbind(lasso$lambda,lasso$cvm,lasso$nzero)
coef(lasso,s=lasso$lambda.min)
# Elastic Net
elastic <- cv.glmnet(x=as.matrix(crimedata[,-16]),y=as.matrix(crimedata[,16]),# alpha 0.5 is elastic
                     alpha=0.5,nfolds=8,nlambda=20,type.measure="mse",family="gaussian",standardize=TRUE) 
elastic
plot(elastic,main="Elastic Model")
elastic$lambda.min
cbind(elastic$lambda,elastic$cvm,elastic$nzero)
coef(elastic,s=elastic$lambda.min)
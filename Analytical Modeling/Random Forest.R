# Homework 7
# ISYE6501
library(tree)
library(rpart)
library(randomForest)
set.seed(1)
crimedata <- read.table("uscrime.txt",header=TRUE)
# ------------------------------------------------------------------------------------------
# Question 10.1- find the best model you can using (a) a regression tree model
rtree <- tree(Crime~.,data=crimedata)
rtree$frame
mean(rtree$frame$dev)
plot(rtree,y=null,type=c("proportional","uniform"))
text(rtree, splits = TRUE, label = "yval", all = FALSE, digits = getOption("digits") - 3,
     adj = par("adj"), xpd = TRUE,main="Regression Tree")
# Plots deviance (or total loss) versus size for a sequence of trees
plot(prune.tree(rtree),main="Regression Tree")
# Cross validate R Tree
cvrtree <- cv.tree(rtree)
cvrtree
plot(cvrtree,main="CV Regression Tree")
# ------------------------------------------------------------------------------------------
# Question 10.1- find the best model you can using (b) a random forest model
rforest <- randomForest(Crime~.,data=crimedata, type="Regression",ntree=500)
rforest
# Highest R2 value of the forest
max(rforest$rsq)
# locate the first instance of this value of all r squared values
i <- match(max(rforest$rsq),rforest$rsq)
# obtain the tree with the highest r squared value
best <- getTree(rforest, k=i, labelVar=TRUE)
best
plot(best)
rforest$predicted

# ------------------------------------------------------------------------------------------
# Question 10.3 part 1- use logistic regression to find a good predictive model for 
# whether credit applicants are good credit risks or not. 
# Show your model (factors used and their coefficients), the software output, 
# and the quality of fit. You can use the glm function in R. 
# To get a logistic regression (logit) model on data where the response is 
# either zero or one, use family=binomial(link="logit") in your glm function call
germancredit <- read.table("germancredit.txt")
# convert the response to a binomial 1 = good, 0  = bad credit
resp <- ifelse(germancredit$V21 ==1, 1, 0)
credit <-cbind(germancredit[,1:20],resp)
# build a logistic regression model
model <- glm(resp~.,data=credit,family=binomial(link="logit"))
model$coefficients
plot(model$fitted.values,main="Probability of Good Credit Applicant",ylab="Probability")
summary(model)
glm.pred2 <- ifelse(model$fitted.values > 0.5, "Good", "Bad")
attach(germancredit)
table(glm.pred2,resp)

# Question 10.3 part 2.	Because the model gives a result between 0 and 1, 
# it requires setting a threshold probability to separate between "good" and "bad"
# answers. In this data set, they estimate that incorrectly identifying a bad 
# customer as good, is 5 times worse than incorrectly classifying a good customer 
# as bad. Determine a good threshold probability based on your model.
glm.pred1 <- ifelse(model$fitted.values > 0.3, "Good", "Bad")
table(glm.pred1,resp)
glm.pred2 <- ifelse(model$fitted.values > 0.5, "Good", "Bad")
table(glm.pred2,resp)
glm.pred3 <- ifelse(model$fitted.values > 0.7, "Good", "Bad")
table(glm.pred3,resp)


# ISYE 6501 HW 10
set.seed(1)
library(dplyr)
library("mice")
library(kknn)
cancerdata <- read.csv("cancerdata.csv",header=TRUE)
# 1. Use the mean/mode imputation method to impute values for the missing data.
all_col7 <- cbind(cancerdata["ID.Number"],cancerdata["Bare.Nuclei"])
row.names(all_col7)
x = row.names(cancerdata)[apply(cancerdata["Bare.Nuclei"], 1, function(value) any(value=="?"))]
y = row.names(cancerdata)[apply(cancerdata["Bare.Nuclei"], 1, function(value) any(value!="?"))]
missingq<- cancerdata[x,]
allothers <- cancerdata[y,]
replace_val <- mean(as.numeric(allothers$Bare.Nuclei))
imputed1 <- mutate(cancerdata, Bare.Nuclei = ifelse(Bare.Nuclei == "?", replace_val, Bare.Nuclei))
# 2. Use regression to impute values for the missing data. 
imp <- mutate(cancerdata, Bare.Nuclei = ifelse(Bare.Nuclei == "?", NA, Bare.Nuclei))
imptemp <- mice(imp, method = "norm.predict", m = 1)
summary(imptemp)
imptemp$imp$Bare.Nuclei
imputed2 <- complete(imptemp,1)
# 3. Use regression with perturbation to impute values for the missing data. 
imptemp2 <- mice(imp, method="norm.nob", m=1)
summary(imptemp2)
imptemp2$imp$Bare.Nuclei
imputed3 <- complete(imptemp2,1)
# 4. (Optional) Compare the results and quality of classification models (e.g., SVM, KNN) build using
# (1) the data sets from questions 1,2,3; 
# (2) the data that remains after data points with missing values are removed; and 
# (3) the data set when a binary variable is introduced to indicate missing values.
set.seed(17)
# create binary variable
binarydf <- cancerdata
binarydf[x,"Binary"]<-1
binarydf[y,"Binary"]<-0
# remove IDs
noID1 <- subset(imputed1, select=-c(ID.Number))
noID2 <- subset(imputed2, select=-c(ID.Number))
noID3 <- subset(imputed3, select=-c(ID.Number))
noID4 <- subset(allothers, select=-c(ID.Number))
noID5 <- subset(binarydf, select=-c(ID.Number))
# define function to split the data set
splitDF <- function(df) {
  smpl_size <- floor(0.8 * nrow(df))
  train_ind <- sample(seq_len(nrow(df)), size = smpl_size)
  train <- df[train_ind, ]
  test <- df[-train_ind, ]
  return (list("training" = train, "test" = test))
}
runKNN <- function(train, test, ks){
  bestK = 0
  bestAccuracy = 0
  fit <- train.kknn(Class ~., train, maxK=k)
  predictions <- predict(fit, test)
  accuracy <- round((sum(predictions == test$Class) / length(test$Class)), digits=3)
  return (list("best_params" = fit$best.parameters, "best_accuracy" = accuracy))
}
setk <- 35
noID1_sets <- splitDF(noID1)
res1 <- runKNN(noID1_sets$training, noID1_sets$test, setk)
noID2_sets <- splitDF(noID2)
res2 <- runKNN(noID2_sets$training, noID2_sets$test, setk)
noID3_sets <- splitDF(noID3)
res3 <- runKNN(noID3_sets$training, noID3_sets$test, setk)
noID4_sets <- splitDF(noID4)
res4 <- runKNN(noID4_sets$training, noID4_sets$test, setk)
noID5_sets <- splitDF(noID5)
res5 <- runKNN(noID5_sets$training, noID5_sets$test, setk)
# Print Results ---------------------------------------------------------------------
print("KNN Imputed with mean")
res1$best_params
res1$best_accuracy
print("KNN Imputed with regression")
res2$best_params
res2$best_accuracy
print("KNN Imputed with perturbation")
res3$best_params
res3$best_accuracy
print("KNN data points removed")
res4$best_params
res4$best_accuracy
print("KNN with binary variable")
res5$best_params
res5$best_accuracy
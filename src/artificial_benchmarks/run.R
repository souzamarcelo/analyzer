source("artificial_landscape.R")

le <- Landscape$new("landscapes/parameters-conditional.txt", "landscapes/simple-conditional-landscape1.txt")


x <- c(1,2,0,0,1)
names(x) <- le$pnames
x<- le$deactivateConfig(x)
cat("Total eval: ",le$getEval(x), "\n")

library("irace")
source("./model_scripts/DataHandling.R")
source("./model_scripts/RFModel.R")

data = list()
SCENARIO_NAME = "artificial2-norm-random-1000"

# read parameter definition
parameters = readParameters(paste("parameters-", SCENARIO_NAME, ".txt", sep=""))

# read the data set from a table
# - each parameter is a column
# - especial columns: instance and .PERFORMANCE.
# The instance column is not need, while .PERFORMANCE. is required
data$data = read.table(paste("data/", SCENARIO_NAME, "-rf.txt", sep=""), header = TRUE)
data$pnames = colnames(data$data)[!(colnames(data$data) %in% ".PERFORMANCE.")]

#impute data
data$data = doImputeCols(data = data$data, parameters = parameters)

#build model
model = RFModel$new(n_trees=100, parameters=parameters)
#train 
model$trainModel(data=data)

#importance can be found in
model$importance_frame

#!/usr/bin/env Rscript
#######################################################################
## export iRace data for processing with fANOVA
######################################################################
library(tibble)
suppressPackageStartupMessages(library(dplyr))
library(tidyr)
suppressPackageStartupMessages(library(optparse))
library(crayon)
library(here)

source(paste(here(),"/fanova/model_scripts/DataHandling.R",sep=""))
source(paste(here(),"/fanova/Export.R",sep=""))

options = list(
    make_option(c("-t","--type"), action="store", default="perf", help="Raw performance (perf), normalized performance (norm), performance quartile (quan), normalized ranking (rank), normalized ranking with imputation (irank), ranking quartile with imputation (qrank)")
)
opt=parse_args(OptionParser(option_list=options),positional_arguments=T)
if (length(opt$args)==0) {
    stop("Please give an irace data file name.\n")
}

## (1) get data
datafile=opt$args[1]
cat(red(paste("Process ",datafile," with type ",opt$options$type,sep="")),"\n")
data=getDataFromIrace(datafile, add.dummy=T, data.type=opt$options$type)$data

## (2) write fANOVA data
exportFeaturesResponse(tools::file_path_sans_ext(basename(datafile)),opt$options$type)

# Export feature and response file to current directory.
# * stem: base name for exported files
exportFeaturesResponse <- function(stem,type) {
    ffname=paste(stem,"-",type,"-features.csv",sep="")
    rfname=paste(stem,"-",type,"-response.csv",sep="")
    cat("Writing features to \"",ffname,"\".\n",sep="")
    write.table(data %>% select(-.PERFORMANCE.), file=ffname, row.names = FALSE, sep=",", quote = FALSE)
    cat("Writing responses to \"",rfname,"\".\n",sep="")
    write.table(data %>% select(.PERFORMANCE.),  file=rfname, row.names = FALSE, col.names = FALSE, sep=",", quote = FALSE)
}

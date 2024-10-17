#Load dependencies
library(reticulate)
library(tidyverse)
library(RCurl)
library(jsonlite)
library(readxl)
source("src/R/olo_import_convert.r")
source("src/R/olo_clean_export.r")

#Load Python modules
api_handling <- import("src.Python.api_handling")

#Define filepaths
olo_path <- "data/raw/OLO_data"

#Import data
data_raw <- import_olo(olo_path)
#Clean data
data_olo <- clean_olo(data_raw, "scapisstudynr", "scapis_spectrum")
#Match it to redcap
data_olo_ammended <- match_to_redcap(data_olo)
#Write to csv
write_to_csv(data_olo_ammended)
#Import it to REDcap
api_handling$import_redcap_data("data/processed/data_olo_ammended.csv")
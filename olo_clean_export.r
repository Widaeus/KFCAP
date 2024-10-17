#' Clean OLO Data
#'
#' This function cleans and processes the raw OLO data by renaming columns and performing necessary transformations.
#'
#' @param raw_data A data frame containing the raw OLO data, but already converted.
#' @param identifier A character string specifying the identifier column name in the REDcap df.
#' @param study A character string specifying the study name. Default is "scapis_spectrum".
#' @return A data frame with cleaned and processed OLO data.
#' @details This function performs the following steps:
#' \itemize{
#'   \item Renames columns to more descriptive names.
#'   \item Ensures the data is in a consistent format for further analysis.
#' }
#' @examples
#' \dontrun{
#'   raw_data <- read_file("data/raw/OLO_data.csv")
#'   cleaned_data <- clean_olo(raw_data, "scapisstudynr", "scapis_spectrum")
#' }
clean_olo <- function(data, identifier, study = "scapis_spectrum") {
# Check if the study argument is either "mind" or "spectrum"
  if (!study %in% c("mind", "scapis_spectrum")) {
    stop("The study argument must be either 'mind' or 'scapis_spectrum'.")
  }
# Remove tests
data <- data %>%
  filter(!grepl("test", sample_id, ignore.case = TRUE))

# Remove identical rows
data <- data %>%
  distinct()

# Remove reject_reason contain not NA
data <- data %>%
  filter(is.na(reject_reason))

# Filter on wrong scan_time formatting
data <- data %>%
  filter(grepl("^\\d{2}:\\d{2}:\\d{2}$", scan_time))

# Convert to correct types
data <- type_convert(data)

# Function to count decimal places in a number
count_decimals <- function(x) {
  if (is.na(x) || !is.numeric(x)) return(0)
  x_str <- as.character(x)
  if (grepl("\\.", x_str)) {
    return(nchar(strsplit(x_str, "\\.")[[1]][2]))
  } else {
    return(0)
  }
}

processed_data <- data %>%
  group_by(sample_id) %>%
  mutate(
    decimal_count = sapply(`mch [pg]`, count_decimals),
    flag_present = !is.na(flags)
  ) %>%
  arrange(desc(flag_present), desc(decimal_count)) %>%
  filter(row_number() == 1) %>%
  select(-decimal_count, -flag_present) %>%
  ungroup()

colnames(processed_data) <- colnames(processed_data) %>%
  gsub("%", "_percent", .) %>%
  gsub("#", "_number", .)

processed_data <- processed_data %>%
  select(-patient_id, -patient_name, -patient_date_of_birth, -sex, -age)

processed_data <- processed_data %>%
  mutate(prover_complete = 1)

  # Filter based on study type
  if (study == "scapis_spectrum") {
    processed_data <- processed_data %>%
      filter(!grepl("MD", sample_id, ignore.case = TRUE))
  } else if (study == "mind") {
    processed_data <- processed_data %>%
      filter(grepl("MD", sample_id, ignore.case = TRUE))
  }

processed_data <- processed_data %>%
  rename(!!identifier := sample_id)

# Change the names of every variable to redcap format
new_colnames <- c(
  "sample_type", "slide_id", "kit_id", "wbc_109l", "wbc_flagged",
  "rbc_1012l", "rbc_flagged", "plt_109l", "plt_flagged", "hgb_gl",
  "hgb_flagged", "hct_ll", "hct_flagged", "mcv_fl", "mcv_flagged",
  "rdw__percent", "rdw_flagged", "mch_pg", "mch_flagged", "mchc_gl",
  "mchc_flagged", "neut_percent__percent", "neut_percent_flagged",
  "neut_number_109l", "neut_number_flagged", "lymph_percent__percent",
  "lymph_percent_flagged", "lymph_number_109l", "lymph_number_flagged",
  "mono_percent__percent", "mono_percent_flagged", "mono_number_109l",
  "mono_number_flagged", "eos_percent__percent", "eos_percent_flagged",
  "eos_number_109l", "eos_number_flagged", "baso_percent__percent",
  "baso_percent_flagged", "baso_number_109l", "baso_number_flagged",
  "flags", "reject_reason", "scan_date", "scan_time", "sample_mode",
  "instrument_id", "scan_rev", "scan_tag", "export_rev", "config_rev",
  "config_tag", "operator_id", "operator_name", "demographic", "qc_status",
  "prover_complete"
)
colnames(processed_data)[2:length(colnames(processed_data))] <- new_colnames

return(processed_data)
}

#' Match OLO Data to REDCap Data
#'
#' This function matches the cleaned OLO data to the REDCap data based on a specified identifier usually "mind" or "scapisstudynr".
#' It ensures that the study argument is either "mind" or "scapis_spectrum" and performs a left join to merge the data.
#'
#' @param data_olo A data frame containing the cleaned OLO data.
#' @param identifier A character string specifying the identifier column name.
#' @param study A character string specifying the study name. Must be either "mind" or "scapis_spectrum". Default is "scapis_spectrum".
#' @return A data frame with the OLO data matched to the REDCap data.
#' @details This function performs the following steps:
#' \itemize{
#'   \item Checks if the study argument is valid.
#'   \item Exports the REDCap data.
#'   \item Performs a left join to merge the OLO data with the REDCap data based on the identifier.
#' }
#' @examples
#' \dontrun{
#'   cleaned_data <- clean_olo(raw_data, "scapisstudynr", "scapis_spectrum")
#'   matched_data <- match_to_redcap(cleaned_data, "scapisstudynr", "scapis_spectrum")
#' }
match_to_redcap <- function(data_olo, identifier, study = "scapis_spectrum") {
  # Check if the study argument is either "mind" or "scapis_spectrum"
  if (!study %in% c("mind", "scapis_spectrum")) {
    stop("The study argument must be either 'mind' or 'scapis_spectrum'.")
  }

  data_redcap <- export_redcap_data()

  data_ammended <- data_olo %>%
    left_join(select(data_redcap, "scapisstudynr", scapis_spectrum), by = "scapisstudynr")

  return(data_ammended)
}

#' Write Data to CSV
#'
#' This function writes the amended OLO data to a CSV file with NAs represented as empty strings. Ready for REDcap import.
#'
#' @param data_ammended A data frame containing the amended OLO data.
#' @return None. The function writes the data to a CSV file.
#' @details This function uses the \code{write_csv} function from the \code{readr} package to write the data to a CSV file.
#' @examples
#' \dontrun{
#'   write_to_csv(matched_data)
#' }
write_to_csv <- function(data_ammended) {
  write_csv(data_ammended, "data/processed/data_olo_ammended.csv", na = "")
}
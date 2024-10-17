#' Convert Units
#'
#' This function checks OLO raw output and converts if necessary.
#'
#' @param df A data frame containing OLO_data
#' @return A data frame with the conversion
#' @details This function uses the following packages:
#' \itemize{
#'   \item \code{dplyr} for data manipulation.
#' }
#' @examples
#' \dontrun{
#'   df <- convert_units(df)
#' }
convert_units <- function(df) {
  if ("hgb [mmol/L]" %in% colnames(df)) {
    df <- df %>%
      mutate(`hgb [mmol/L]` = as.numeric(`hgb [mmol/L]`))
    colnames(df)[colnames(df) == "hgb [mmol/L]"] <- "hgb [g/L]"
  }
  # Convert "hgb [g/dL]" to "hgb [g/L]" by multiplying by 10
  if ("hgb [g/dL]" %in% colnames(df)) {
    df <- df %>%
      mutate(`hgb [g/dL]` = as.numeric(`hgb [g/dL]`) * 10)
    colnames(df)[colnames(df) == "hgb [g/dL]"] <- "hgb [g/L]"
  }
  # Some variables have bad naming, convert based on range.
  # Convert "hgb [g/L]" less than 10 to itself * 16
  if ("hgb [g/L]" %in% colnames(df)) {
    df <- df %>%
      mutate(`hgb [g/L]` = ifelse(`hgb [g/L]` < 20, `hgb [g/L]` * 16, `hgb [g/L]`))
  }
  if ("mchc [mmol/L]" %in% colnames(df)) {
    df <- df %>%
      mutate(`mchc [mmol/L]` = as.numeric(`mchc [mmol/L]`))
    colnames(df)[colnames(df) == "mchc [mmol/L]"] <- "mchc [g/L]"
  }
  if ("mchc [g/dL]" %in% colnames(df)) {
    df <- df %>%
      mutate(`mchc [g/dL]` = as.numeric(`mchc [g/dL]`) * 10)
    colnames(df)[colnames(df) == "mchc [g/dL]"] <- "mchc [g/L]"
  }
  # Range direction conversion
  if ("mchc [g/L]" %in% colnames(df)) {
    df <- df %>%
      mutate(`mchc [g/L]` = ifelse(`mchc [g/L]` < 150, `mchc [g/L]` * 16, `mchc [g/L]`))
  }
  # Convert amol to pg
  if ("mch [amol]" %in% colnames(df)) {
    df <- df %>%
      mutate(`mch [amol]` = as.numeric(`mch [amol]`))
    colnames(df)[colnames(df) == "mch [amol]"] <- "mch [pg]"
  }
  if ("mch [pg]" %in% colnames(df)) {
    df <- df %>%
      mutate(`mch [pg]` = ifelse(`mch [pg]` > 100, `mch [pg]` / 64.5, `mch [pg]`))
  }
  # Convert WBC from 10^3/uL to 10^9/L
  if ("wbc [10^3/uL]" %in% colnames(df)) {
    df <- df %>%
      mutate(`wbc [10^3/uL]` = as.numeric(`wbc [10^3/uL]`))
    colnames(df)[colnames(df) == "wbc [10^3/uL]"] <- "wbc [10^9/L]"
  }
  # Convert RBC from 10^6/uL to 10^12/L
  if ("rbc [10^6/uL]" %in% colnames(df)) {
    df <- df %>%
      mutate(`rbc [10^6/uL]` = as.numeric(`rbc [10^6/uL]`))
    colnames(df)[colnames(df) == "rbc [10^6/uL]"] <- "rbc [10^12/L]"
  }

  # Convert PLT from 10^3/uL to 10^9/L
  if ("plt [10^3/uL]" %in% colnames(df)) {
    df <- df %>%
      mutate(`plt [10^3/uL]` = as.numeric(`plt [10^3/uL]`))
    colnames(df)[colnames(df) == "plt [10^3/uL]"] <- "plt [10^9/L]"
  }

  # Convert HCT from % to L/L
  if ("hct [%]" %in% colnames(df)) {
    df <- df %>%
      mutate(`hct [%]` = as.numeric(`hct [%]`) / 100)
    colnames(df)[colnames(df) == "hct [%]"] <- "hct [L/L]"
  }

  # Conversions for Neutrophils, Lymphocytes, Monocytes, Eosinophils, and Basophils
  leukocyte_types <- c("neut# ", "lymph# ", "mono# ", "eos# ", "baso# ")
  for (leukocyte in leukocyte_types) {
    full_colname <- paste(leukocyte, "[10^3/uL]", sep = "")
    if (full_colname %in% colnames(df)) {
      df <- df %>%
        mutate(!!sym(full_colname) := as.numeric(!!sym(full_colname)))
      colnames(df)[colnames(df) == full_colname] <- paste(leukocyte, "[10^9/L]", sep = "")
    }
  }
  return(df)
}

#' Read File
#'
#' This function reads a file and returns its content as a data frame.
#' It supports both CSV and Excel file formats.
#'
#' @param file A character string specifying the path to the file to be read.
#' @return A data frame containing the content of the file.
#' @details This function uses the following packages:
#' \itemize{
#'   \item \code{readr} for reading CSV files.
#'   \item \code{readxl} for reading Excel files.
#' }
#' @examples
#' \dontrun{
#'   df <- read_file("data/sample.csv")
#'   df <- read_file("data/sample.xlsx")
#' }
read_file <- function(file) {
  if (grepl("\\.csv$", file)) {
    df <- read_csv(file, show_col_types = FALSE)  # Use read_csv for csv files
  } else if (grepl("\\.xlsx$", file)) {
    df <- read_excel(file)  # Use read_excel for xlsx files
  } else {
    stop("Unsupported file format")
  }
  return(df)
}

#' Import and Clean OLO Data
#'
#' This function imports OLO data from a specified directory, converts units,
#' checks for consistent column names, and combines the data into a single data frame.
#'
#' @param olo_path A character string specifying the path to the directory containing OLO data files.
#' @return A data frame containing the combined and cleaned OLO data.
#' @details This function depends on the following packages:
#' \itemize{
#'   \item \code{readr} for reading CSV files.
#'   \item \code{readxl} for reading Excel files.
#'   \item \code{dplyr} for data manipulation.
#'   \item \code{progress} for displaying a progress bar.
#' }
#' @examples
#' \dontrun{
#'   olo_path <- "data/raw/OLO_data"
#'   combined_data <- import_olo(olo_path)
#'   print(combined_data)
#' }
import_olo <- function(olo_path) {
  file_list <- list.files(path = olo_path, pattern = "\\.(csv|xlsx)$", full.names = TRUE)
  data_list <- list()
  differing_columns <- list()
  first_df <- read_file(file_list[1])
  first_df <- convert_units(first_df)
  colnames_check <- colnames(first_df)

  for (file in file_list) {
    df <- read_file(file)
    df <- convert_units(df)
    differing_cols <- setdiff(colnames(df), colnames_check)
    if (length(differing_cols) > 0) {
      differing_columns[[file]] <- differing_cols
    }
    data_list <- append(data_list, list(df))
  }

  if (length(differing_columns) > 0) {
    log_file <- file("logs/differing_columns_log.txt", open = "wt")
    for (file in names(differing_columns)) {
      writeLines(sprintf("File: %s", file), log_file)
      writeLines(sprintf("Differing columns: %s\n", paste(differing_columns[[file]], collapse = ", ")), log_file)
    }
    close(log_file)
    stop("Column names differ across files. See differing_columns_log.txt for details.")
  }

  data_list <- lapply(data_list, function(df) {
    df[] <- lapply(df, as.character)

    return(df)
  })
  concatenated_data <- bind_rows(data_list)
  return(as_tibble(concatenated_data))
}
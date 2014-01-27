# Assignment - Rank hospitals in all states

rankall <- function(outcome, num = "best") {
	## Read outcome data
	source("rankhospital.R")
	data <- read.csv("ProgAssignment3-data/outcome-of-care-measures.csv", colClasses = "character")
	results <- character()
	
	## Check that outcome is valid
	possible_states <-  as.vector(as.data.frame(table(data[,7]))$Var1)
	possible_outcome <- c("heart attack", "heart failure", 'pneumonia')
	
	if(outcome %in% possible_outcome == FALSE) {
		stop("invalid outcome")
		} else if(outcome == "heart attack") {
			column_num = 2
			} else if(outcome == "heart failure") {
				column_num = 3
				} else if(outcome == "pneumonia") {
					column_num = 4
				}
	
	## For each state, find the hospital of the given rank
	# Subset to data that will be tested
	rank_data <- subset(data[, c(2, 11, 17, 23)])
		
	# Order by outcome
	rank_data <- rank_data[with(rank_data, order(as.numeric(rank_data[,column_num]), Hospital.Name)), ]
	
	# For loop time!
	for(state in possible_states) {
		hospital <- rankhospital(state, outcome, num)
		results <- append(results, hospital[1])
	}
	
	## Return a data frame with the hospital names and the (abbreviated) state name
	final <- data.frame(
		"hospital" = results,
		"state" = possible_states
		)
		
}

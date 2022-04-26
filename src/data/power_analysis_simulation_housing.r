conduct_one_trial <- function(num_in_block = c(100, 200, 300)) { 
  require(data.table)
  
  ## three blocks 
  ## each has a normal distribution, with a mean-shift between them. 
  ## - for example, city-wide median income. 
  
  income_block_a <- rnorm(n=num_in_block[1], mean = 100000, sd = 10000) 
  income_block_b <- rnorm(n=num_in_block[2], mean = 900000, sd = 10000) 
  income_block_c <- rnorm(n=num_in_block[3], mean = 400000, sd = 20000)
  
  block <- sample(c(rep('a', num_in_block[1]), rep('b', num_in_block[2]), rep('c', num_in_block[3])))
  
  ## treatment is a racial/ethnic signal of the person who is asking for an 
  ## appraisal 
  
  baseline_effect    <- -5000
  additional_block_a <- 5000
  additional_block_b <- 0
  additional_block_c <- -1000
  
  ## sf 
  min_sf <- 700 
  max_sf <- 3000
  ## bedrooms 
  min_bedroom <- 0
  max_bedroom <- 4
  ## lot size 
  min_lot <- 1000
  max_lot <- 43000
  ## 
  ## other "stuff" leftover. 
  unmodeled_estimates_low  <- -100000
  unmodeled_estimates_high <- 100000

  bedrooms           <- sort(sample(seq(from=min_bedroom, to=max_bedroom), prob = c(.1, .1, .3, .3, .2), replace = TRUE))  
  sqfootage          <- sort(runif(n=sum(num_in_block), min=min_sf, max=max_sf))
  lot_size           <- sort(runif(n=sum(num_in_block), min=min_lot, max=max_lot))
  racial_composition <- sample(0:1, size = sum(num_in_block), replace = TRUE)
  
  true_price <- 0 + 10000 * bedrooms + 200 * sqfootage + 1 * lot_size + 
    racial_composition * baseline_effect + 
    racial_composition * additional_block_a * I(block == 'a') + 
    racial_composition * additional_block_b * I(block == 'b') + 
    racial_composition * additional_block_c * I(block == 'c') + 
      runif(sum(num_in_block, min = unmodeled_estimates_low, max = unmodeled_estimates_high)) 
    
  
  d <- data.table(
    block, bedrooms, sqfootage, lot_size, racial_composition, true_price
    )
  
  d[block == 'a', true_price := true_price + income_block_a]
  d[block == 'b', true_price := true_price + income_block_b]
  d[block == 'c', true_price := true_price + income_block_c]
    
  return(d)
} 

estimate_model_no_interaction <- function(data) { 
  require(data.table)
  model <- data[ , lm(true_price ~ bedrooms + factor(block) + sqfootage + lot_size + racial_composition)]
  }

estimate_model_with_interaction <- function(data) { 
  require(data.table)
  model <- data[ , lm(
    true_price ~ bedrooms + factor(block) + sqfootage + lot_size + racial_composition + 
      racial_composition * factor(block))]
}

rm(p_values)
p_values <- replicate(n = 100, expr = 
  summary(
    estimate_model_no_interaction(
      data = conduct_one_trial(
        num_in_block = c(200, 200, 200)
        )
      )
    )$coefficients[7, 4]
)
mean(p_values < 0.05)

p_values_by_block <- replicate(n=100, expr = 
  summary(
    estimate_model_with_interaction(
      data = conduct_one_trial(
        num_in_block = c(20, 30, 40)
      )
    )
  )$coefficients[7:9, 4]
  )






mean(p_values < 0.05)

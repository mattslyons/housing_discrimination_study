rental\_power\_analysis
================

``` r
make_cities <- function(city_n) {

  cities <- data.table(
    city = c('chicago',
          'dallas',
          'houston',
          'washingtondc',
          'philadelphia',
          'miami',
          'atlanta',
          'boston',
          'phoenix',
          'sfbay',
          'inlandempire',
          'detroit',
          'seattle',
          'losangeles',
          'minneapolis',
          'newyork',
          'sandiego',
          'tampa',
          'denver',
          'baltimore'),
    n = rep(300,20),
    # median_price = c(1000, 862, 700),
    # sd_city = c(200, 150, 150),
    female_subj_ratio = rep(.5,20),
    black_subj_ratio = rep(.5,20),
    
    # predicted response ratios by group
    # racial estimates from Wave 1 of https://doi.org/10.1177%2F2378023120972287
    # Males offset taken from https://doi.org/10.1016/j.regsciurbeco.2018.10.003
    # using the "single" category of Murchie
    
    rr_white_female = runif(20,.519,.635),
    rr_white_male = runif(20,.519 - .0255,.635 - .0255),
    
    rr_black_female = runif(20,.343,.422),
    rr_black_male = runif(20,.343 + .0694,.422 + .0694)

  )

  return(cities)
}

cities <- make_cities(num_in_city)
cities
```

    ##             city   n female_subj_ratio black_subj_ratio rr_white_female
    ##  1:      chicago 300               0.5              0.5       0.5193453
    ##  2:       dallas 300               0.5              0.5       0.5268525
    ##  3:      houston 300               0.5              0.5       0.6167419
    ##  4: washingtondc 300               0.5              0.5       0.5269259
    ##  5: philadelphia 300               0.5              0.5       0.5489402
    ##  6:        miami 300               0.5              0.5       0.6327773
    ##  7:      atlanta 300               0.5              0.5       0.6290428
    ##  8:       boston 300               0.5              0.5       0.6302388
    ##  9:      phoenix 300               0.5              0.5       0.5742236
    ## 10:        sfbay 300               0.5              0.5       0.5953256
    ## 11: inlandempire 300               0.5              0.5       0.5368796
    ## 12:      detroit 300               0.5              0.5       0.5962927
    ## 13:      seattle 300               0.5              0.5       0.5630931
    ## 14:   losangeles 300               0.5              0.5       0.5534859
    ## 15:  minneapolis 300               0.5              0.5       0.5255554
    ## 16:      newyork 300               0.5              0.5       0.5879232
    ## 17:     sandiego 300               0.5              0.5       0.5599740
    ## 18:        tampa 300               0.5              0.5       0.6260889
    ## 19:       denver 300               0.5              0.5       0.5753591
    ## 20:    baltimore 300               0.5              0.5       0.5969023
    ##     rr_white_male rr_black_female rr_black_male
    ##  1:     0.5425316       0.3541630     0.4804735
    ##  2:     0.5701410       0.4199520     0.4659707
    ##  3:     0.5555375       0.3906991     0.4581293
    ##  4:     0.5634193       0.3726660     0.4866527
    ##  5:     0.4960902       0.3961773     0.4167167
    ##  6:     0.5716445       0.3893058     0.4619426
    ##  7:     0.5354261       0.3786442     0.4640325
    ##  8:     0.5635176       0.3448058     0.4377787
    ##  9:     0.5970016       0.3920328     0.4323499
    ## 10:     0.5440139       0.3462192     0.4821131
    ## 11:     0.5119983       0.3461441     0.4519458
    ## 12:     0.5241475       0.3751181     0.4863308
    ## 13:     0.5058015       0.3931673     0.4507563
    ## 14:     0.5466036       0.3880871     0.4202147
    ## 15:     0.5191349       0.3969304     0.4738688
    ## 16:     0.5893123       0.4062804     0.4148193
    ## 17:     0.5402259       0.3698604     0.4646696
    ## 18:     0.5558862       0.3575392     0.4307089
    ## 19:     0.5183085       0.4156747     0.4497076
    ## 20:     0.4977501       0.4009894     0.4815873

``` r
make_city_data <- function(city = cities[1,]){
  n = city[,n]
  
  subj_female = trunc(city[,female_subj_ratio] * n)
  subj_black = trunc(city[,black_subj_ratio] * n)
  
  city_data <- data.table(
    city = rep(city[,city],city[,n]),
    #list_price = rnorm(n=n,mean=city[,median_price],sd=city[,sd_city]),
    
    # randomly apply subjects to treatments
    female = sample(rep(0:1,c(n-subj_female, subj_female))),
    black = sample(rep(0:1,c(n-subj_black, subj_black)))
  )
  
  # apply predicted response rate to each group
  rr_white_male <- c(city[,rr_white_male],1-city[,rr_white_male])
  city_data[I(!female) & I(!black), response := sample(
    1:0,
    size = .N,
    replace = TRUE,
    prob = rr_white_male)]
  
  rr_white_female <- c(city[,rr_white_female],1-city[,rr_white_female])
  city_data[I(female) & I(!black), response := sample(
    1:0,
    size = .N,
    replace = TRUE,
    prob = rr_white_female)]
  
  rr_black_male <- c(city[,rr_black_male],1-city[,rr_black_male])
  city_data[I(!female) & I(black), response := sample(
    1:0,
    size = .N,
    replace = TRUE,
    prob = rr_black_male)]
  
  rr_black_female <- c(city[,rr_black_female],1-city[,rr_black_female])
  city_data[I(female) & I(black), response := sample(
    1:0,
    size = .N,
    replace = TRUE,
    prob = rr_black_female)]
  
  return(city_data)
  
}
```

``` r
# function to calculate power in lapply
calcpow <- function(col) {return(mean(col<.05))}
```

``` r
make_multi_city_data <- function(cities = cities) {

  multi_city_data <- data.table()
  
  for (i in 1:cities[,.N]) {
    multi_city_data <- rbind(multi_city_data,make_city_data(city = cities[i,]))
  }
  
  return(multi_city_data)
}

multi_city_data <- make_multi_city_data(cities)
```

``` r
multi_city_data[,mean(response), by = .(female,black)]
```

    ##    female black        V1
    ## 1:      1     0 0.5897611
    ## 2:      0     0 0.5472313
    ## 3:      0     1 0.4300341
    ## 4:      1     1 0.3589577

``` r
# m_boston <- multi_city_data[city == 'Boston',lm(response ~ female * black)]
# m_chicago <- multi_city_data[city == 'Chicago',lm(response ~ female * black)]
# m_phili <- multi_city_data[city == 'Philadelphia',lm(response ~ female * black)]
m_multi_city_simple <- multi_city_data[,lm(response ~ female * black)]
m_multi_city_FE <- multi_city_data[,lm(response ~ female * black + city)]

stargazer(m_multi_city_simple, m_multi_city_FE,
          column.labels = c('simple', 'cityFE'),
           type = 'text')
```

    ## 
    ## ======================================================================
    ##                                    Dependent variable:                
    ##                     --------------------------------------------------
    ##                                          response                     
    ##                              simple                   cityFE          
    ##                               (1)                       (2)           
    ## ----------------------------------------------------------------------
    ## female                      0.043**                   0.044**         
    ##                             (0.018)                   (0.018)         
    ##                                                                       
    ## black                      -0.117***                 -0.116***        
    ##                             (0.018)                   (0.018)         
    ##                                                                       
    ## citybaltimore                                        -0.102**         
    ##                                                       (0.040)         
    ##                                                                       
    ## cityboston                                           -0.080**         
    ##                                                       (0.040)         
    ##                                                                       
    ## citychicago                                          -0.113***        
    ##                                                       (0.040)         
    ##                                                                       
    ## citydallas                                           -0.124***        
    ##                                                       (0.040)         
    ##                                                                       
    ## citydenver                                            -0.056          
    ##                                                       (0.040)         
    ##                                                                       
    ## citydetroit                                          -0.107***        
    ##                                                       (0.040)         
    ##                                                                       
    ## cityhouston                                          -0.106***        
    ##                                                       (0.040)         
    ##                                                                       
    ## cityinlandempire                                     -0.109***        
    ##                                                       (0.040)         
    ##                                                                       
    ## citylosangeles                                       -0.131***        
    ##                                                       (0.040)         
    ##                                                                       
    ## citymiami                                             -0.026          
    ##                                                       (0.040)         
    ##                                                                       
    ## cityminneapolis                                      -0.147***        
    ##                                                       (0.040)         
    ##                                                                       
    ## citynewyork                                           -0.038          
    ##                                                       (0.040)         
    ##                                                                       
    ## cityphiladelphia                                     -0.157***        
    ##                                                       (0.040)         
    ##                                                                       
    ## cityphoenix                                          -0.099**         
    ##                                                       (0.040)         
    ##                                                                       
    ## citysandiego                                          -0.068*         
    ##                                                       (0.040)         
    ##                                                                       
    ## cityseattle                                          -0.084**         
    ##                                                       (0.040)         
    ##                                                                       
    ## citysfbay                                            -0.116***        
    ##                                                       (0.040)         
    ##                                                                       
    ## citytampa                                            -0.087**         
    ##                                                       (0.040)         
    ##                                                                       
    ## citywashingtondc                                      -0.065          
    ##                                                       (0.040)         
    ##                                                                       
    ## female:black               -0.114***                 -0.116***        
    ##                             (0.025)                   (0.025)         
    ##                                                                       
    ## Constant                    0.547***                 0.637***         
    ##                             (0.013)                   (0.030)         
    ##                                                                       
    ## ----------------------------------------------------------------------
    ## Observations                 6,000                     6,000          
    ## R2                           0.034                     0.040          
    ## Adjusted R2                  0.033                     0.036          
    ## Residual Std. Error    0.491 (df = 5996)         0.490 (df = 5977)    
    ## F Statistic         70.069*** (df = 3; 5996) 11.296*** (df = 22; 5977)
    ## ======================================================================
    ## Note:                                      *p<0.1; **p<0.05; ***p<0.01

# `{r} # sim_multi_city_simple_pv <- function(multi_city_data = multi_city_data) { #    #   n_subj = sum(cities[,n]) #    #   #create model #   mod_multi_city <- multi_city_data[,lm(response ~ female * black)] #    #   # extract p-values #   return(summary(mod_multi_city)$coefficients[,4]) #  # } #  # multi_city_simple_pv <- future_replicate( #   1000, #   expr = sim_multi_city_simple_pv(make_multi_city_data(cities)) # ) #  # multi_city_simple_pv <- as.data.table(t(multi_city_simple_pv)) #  # multi_city_simple_power <- multi_city_simple_pv[,future_lapply(.SD,calcpow)] #  # multi_city_simple_power #`

``` r
sim_multi_city_FE_pv <- function(multi_city_data = multi_city_data) {
  
  n_subj = sum(cities[,n])
  
  #create model
  mod_multi_city <- multi_city_data[,lm(response ~ female * black + city)]
  
  # extract p-values
  return(summary(mod_multi_city)$coefficients[,4])

}

multi_city_FE_pv <- future_replicate(
  1000,
  expr = sim_multi_city_FE_pv(make_multi_city_data(cities))
)

multi_city_FE_pv <- as.data.table(t(multi_city_FE_pv))

multi_city_FE_power <- multi_city_FE_pv[,future_lapply(.SD,calcpow)]

multi_city_FE_power
```

    ##    (Intercept) female black citybaltimore cityboston citychicago citydallas
    ## 1:           1  0.461 0.999         0.055      0.056       0.095      0.053
    ##    citydenver citydetroit cityhouston cityinlandempire citylosangeles citymiami
    ## 1:      0.057       0.057       0.045            0.158          0.105     0.056
    ##    cityminneapolis citynewyork cityphiladelphia cityphoenix citysandiego
    ## 1:           0.088       0.054            0.147       0.056         0.08
    ##    cityseattle citysfbay citytampa citywashingtondc female:black
    ## 1:       0.106     0.059     0.061            0.053        0.987

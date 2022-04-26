# Team MTLS w241 final project
Team MTLS research project - W241 section 6 Fall 2021 <br>
Tilman Bayer, Matt Lyons, Sam Stephens, Luke Verdi

Are racial/ethnic minorities in the US subject to bias when seeking housing? Does such bias vary by gender? Such discrimination has been outlawed for more than half a century by the Fair Housing Act and other legislation. But previous research has found evidence that it has persisted into the 2010s among Craigslist advertisements, in the case of "roommate wanted" ads (Gaddis and Ghoshal 2020) and general rental ads by property owners or other agents (Murchie and Pang 2018).

We plan to explore this question in a correspondence audit study, contacting Craigslist advertisers seeking roommates from 20 urban areas in the US via up to 12,000 emails with randomized signifiers for race/ethnicity and gender.

![Cities and Craigslist Screencap](./data/cities_rooms.png?raw=true)

We hypothesize that having Black signifiers will cause a lower response rate than having White signifiers. Further, we expect that this effect will be moderated by gender such that we see a larger difference between response rates for men by race than for women. Additionally, we expect that the extent of local residential segregation will moderate the race effect, with more-segregated areas seeing a greater difference in response rate by race than areas with less segregation.

By varying applicant gender, we also plan to examine to what extent applicant gender affects the response rate. Based on previous studies, we expect the baseline response rate to be lower for male applicants than for female applicants. By including both male and female applicants, we expect we will see a statistically significant difference in racial bias by gender.

Our approach largely follows the methods of Gaddis and Ghoshal (2020); however, we believe that our study will add value e.g. by examining newer data (Gaddis and Ghoshal collected data in 2013 and 2014), across a larger number of regions (20, compared to 3 in Gaddis and Ghoshal) and compared to earlier audit studies, will be able to take advantage of more careful race/ethnicity signaling approaches developed in the literature more recently (Gaddis 2017).

Specifically, we have chosen 16 first and last name combinations which are perceived as congruently signalling race to a 90% degree or greater. Further, each first name is drawn from the middle 50th percentile of mother's education level (Gaddis 2017), and none of the search results on the first page have any defamatory or contrary race/gender signals.

| Category Signal | Name 1          | Name 2          | Name 3           | Name 4        |
|:---------------:|-----------------|-----------------|------------------|---------------|
| Black Female    | Shanice Thomas  | Tionna Wilson   | Ebony Williams   | Tyra Booker   |
| Black Male      | Jamal Jefferson | DeAndre Jackson | Terell Robinson  | Jayvon Carter |
| White Female    | Hilary Roberts  | Amy Morgan      | Stephanie Nelson | Kristen Hall  |
| White Male      | Brad Anderson   | Steven Smith    | Luke Mitchell    | Brian Bailey  |

We will use a Python script to continuously scrape the Craigslist "rooms and shares" section in these 20 areas. The script will record the city, time scraped, and the email address to a CSV file (Craigslist masks the email addresses, replacing them with a random string of characters @craigslist.org). Once an hour, a separate Python script will send emails to each of the new scraped advertisements during the previous hour, signaling race and gender according to our block randomization and recording the details of the signal (within each city, we will use each name and each slight variation of email body text an equal number of times). This is to avoid any effects associated the delay between the advertisement's posting and the time of the response.

![Email example](./data/email_screencap.png?raw=true)

After seven days have passed since the last sent emails, a third Python script will check through the email inbox, making note of which emails received responses in the CSV file. To those responses, it will send another email indicating that we are no longer interested in the space to close the loop and ensure no renters are waiting for a response.

![Data flow diagram](./data/dataflow_diagram.png?raw=true)

We will analyze the collected response rates by using models built in R. We'll primarily be regressing Response Rate on Race, Gender and Race * Gender to answer the primary questions around whether racial/ethnic minorities in the US subject to bias when seeking housing. We'll also be including several models attempting to account for city fixed effects or city segregation levels and potentially for name fixed effects. The data on city segregation levels would come from residential segregation data from UC Berkeley's Othering & Belonging Institute. An example of what this model will look like is shown in the image below, with the main terms for Race, Gender and Race * Gender. Significant terms (like those shown) for these variables would inform answers to our hypotheses. For a model which includes city fixed effects, 19 city variables would be included (1 is shown to illustrate). For a model including name fixed effects, 12 name variables would included (1 is shown to illustrate).

![Regression example](./data/regression.png?raw=true)

By revealing that racial bias persists in the housing market and the extent to which these biases continue to influence discriminatory behaviors, as well as how they interact with gender, this research aims to provide evidence in support of policy change/legislation to combat this discrimination and to contribute to the ongoing conversation on this topic within the academic community.

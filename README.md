# Personalized Search Engine for Airbnb
Particularly, the project attempts to develop a need-orientated search engine. In this sense, the reviews of past guests are used to select best search results or to adapt them to factor. 
All the data are from Airbnb.com. We crawled the data by Python. Python Code is attached. 
(1) Data Preprocessing
Actually, we crawled many information related to each property from Airbnb, but those information like price, location and so on are currently unnecessary, so we decide to remove those one and keep only URLs, ids and reviews of properties to make the application run more quickly.
(2) Running Process
When the application gets the keywords input by users, it will extract each word from keywords as each term. Based on all the docs, which one property’s id, url and reviews made make up one doc, each term’s IDF will be calculated. 
Next, we need our users to tell us how many candidates they would like to have a look, because we will generate a temporary container to store the top N documents based on the number they input, so that we do not need to store all the data and to reduce memory usage.
The application can get the TFIDF of each document in which have any terms, based on the IDF got just now. And only the N candidates will be stored ranked by the TFIDF scores.
However, in order to adjust the ranking list so that we could present a more attractive-related ranking list instead of only TFIDF-based list, we would conduct a sentiment analysis for each review in each document in top N list, and calculate average sentiment score(ASC) in one document to get product of ASC and TFIDF. The ASC is range of -1 to 1, so it will be a good adjust index for ranking. The positive score means the most visitors have positive attitude for the property. And the negative scores mean negative ones on the contrary.
Eventually, we can get the final ranking list including N candidates and return it to users. If user think they would like to have a look at each property in Airbnb official website, it will popup the web page from URL stored locally in user’s web browser's.

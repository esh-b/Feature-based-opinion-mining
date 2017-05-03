# Feature-based-opinion-mining

### Need for this kind of project: ###
*	Since the evolution of social networks, people have started to express their opinions in the form of the blogs or facebook posts or tweets starting from the products people buy to the presidential candidate they support.
*	When searched for a particular product on the web, the current day search engines show the list of websites which gives the features of the product and their prices. But, the users can be given much more info about the product using the reviews about the searched product.
*	Thus, a new type of search engine can be designed which will not only retrieve facts, but will also enable the retrieval of opinions of the users about the product.

### Use cases: ###
*   A search engine is created which, when searched for a product, gives the highlighted features of the product and some of the helpful reviews (instead of the user scrolling through all the reviews to know about the product).
*   Consider the scenario when the **product sellers** want to know which of their product features stood it in the market or which of their product features were not liked by majority of their users, this kind of analysis is very helpful.

### About the authors: ###
>***Magdalini Eirinaki, Shamita Pisal, Japinder Singh*** (Computer Engineering Department, San Jose State University, One Washington Square, San Jose, CA 95192, United States)

### Steps to run the code:
*   All the codes are written in ***Python 3.5.2***.
*   The sample review files is uploaded in the repository. All the review files to be analyzed are assumed to be in this format although the python code (*main.py*) can be modified to read the review file according to its format.
*   All the requirements are installed before running the code by running the command in the terminal: `pip3 install -r requirements.txt`.
*   To run the algorithms on the sample review file, just type the following command in the terminal: `python3 main.py CanonG3.txt`. 
*   Running the above command creates 3 files:
    * *featureScore.txt* which contains all the potential features about the product and their scores.
    * *positiveReviews.txt* which contains all the positive reviews as classified by the algorithm such that a positive review at line i expresses much positive opinion than a review at line j (j > i).
    * *negativeReviews.txt* which contains all the negative reviews such that a negative review at line i expresses much negative opinion than a review at line j (j > i).

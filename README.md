# Matching Wikipedia Articles in a Category via Latent Semantic Analysis

Here we implement a method for finding pages within a category most related to a given page or search query. 
We use Natural Language Processing techniques, specifically the Latent Semantic Analysis technique, in order to perform our matches. 
We use Wikipedia's publicly available API for the collection of document content. 
Our system is portable, built upon a series of Docker containers:

1. a Python container `joshuacook/miniconda` based upon the `busybox` and `miniconda` images.
2. a Mongo DB container from the latest public `mongo` image
3. a data container for Mongo DB from `tianon/true`

![](https://dl.dropboxusercontent.com/u/407587/img/system.png)

## Installation

Usage of this repository requires the installation of Docker. Please [refer](https://docs.docker.com/engine/installation/) to the Docker documentation for installation on your system.

Once Docker has been installed, properly configured and launched, no additional work is necessary. 



## API

We provide a basic API to this functionality via the following command line arguments:

- `./bin/categories #CATEGORY#`
	- will display a category and its associated sub-categories
- `./bin/download`
	- uses Wikipedia's publicly accessible [API](https://en.wikipedia.org/w/api.php) to download pages associated with a given category. 
	  These pages are stored in Mongo DB. Will return an error if the category is misspelled. 
	- It is not necessary to put cateogies in quotes. 
	- Alternatively, a yaml file can be passed. [See Below](#category_yaml)
- `./bin/notebook`
    - launches an interactive notebook 
    - allows the user to manage categories, pages, and queries
    - provides easy access to an IPython shell to the database and object models
- `./bin/page #PAGE#`
	- will display the content of a particular page
- `./bin/pages #CATEGORY#`
	- will display the titles of pages associated with a given category
- `./bin/search #CATEGORY# #N_OF_MATCHES# #QUERY_STRING#`
	- will display `N` articles in a `#CATEGORY# that are most similar to a passed query string
	- the query string may or may not be a stored page
- `./bin/start_db`
	- starts the `mongo` and `mongodata` containers
	- necessary to run the system 

## Document Collection

```Bash
$ ./bin/download #CATEGORY#
```

We use Wikipedia's publicly available  This process is a fairly straight-forward API call. 

Note that it is also possible to pass a yaml file containing a list of categories in the following format:

<a href="category_yaml"></a>
```
categories:
  - Machine learning
  - Game theory
  - Algorithms
  - Linear algebra
```

```Bash
$ ./bin/download data/these_categories.yml
```


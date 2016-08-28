from  lib.helpers.application_helper import wikimedia_page_format
from                        requests import get
from                    urllib.parse import quote
from                           numpy import arange, array, asarray, asmatrix, column_stack
from           sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from                sklearn.pipeline import make_pipeline
from           sklearn.preprocessing import Normalizer

base_url = "https://en.wikipedia.org/w/api.php"

def identify_similar_pages(document_to_match_index, similarity_matrix):
    
    dim_sim_matrx          = len(similarity_matrix)
    
    sim_mat_w_indices      = column_stack((similarity_matrix,arange(dim_sim_matrx)))    
    sim_mat_w_i_sorted     = sim_mat_w_indices[sim_mat_w_indices[:, document_to_match_index].argsort()[::-1]]
    
    sim_page_indices    = sim_mat_w_i_sorted[:,dim_sim_matrx].astype(int)

    return sim_page_indices


def mediawiki_get_category_pageid(category):
    action                 = "?action=query"
    parameters             = "&format=json&prop=extracts&explaintext&exlimit=maxl"
    page                   = "&titles=Category:"+quote(category)
        
    response               = get(base_url+action+parameters+page)
    category_pageid        = [int(key) for key in response.json()['query']['pages']][0]
    
    return category_pageid
    
def mediawiki_get_page_headings(title):
    action                 = "?action=mobileview"
    parameters             = "&format=json&prop=sections&sections=all"
    page                   = "&page="+quote(title)
    
    response               = get(base_url+action+parameters+page)
    headings               = response.json()['mobileview']['sections']
    headings               = [head['line'] for head in headings if 'line' in head] 
    
    return headings

def mediawiki_get_page_text(title,pageid):
    action                 = "?action=query"
    parameters             = "&format=json&prop=extracts&explaintext&exlimit=max"
    page                   = "&titles="+quote(title)
    
    response               = get(base_url+action+parameters+page)
    
    return response.json()['query']['pages'][str(pageid)]['extract']

def mediawiki_get_pages_for_category(category):
    action                 = "?action=query"
    parameters             = "&format=json&list=categorymembers&cmlimit=max"
    category_param         = "&cmtitle=Category:"+wikimedia_page_format(category)
    
    response               = get(base_url+action+parameters+category_param)
    
    return response.json()['query']['categorymembers']

def prepare_document_term_matrix(text_list):
    vectorizer             = CountVectorizer(min_df = 1, stop_words='english')
    document_term_matrix   = vectorizer.fit_transform(text_list)

    return document_term_matrix
    
def prepare_similarity_matrix(latent_semantic_analysis):
    similarity_matrix      = asarray(asmatrix(latent_semantic_analysis) * \
                             asmatrix(latent_semantic_analysis).T)
                         
    return similarity_matrix
    
def prepare_singular_value_decomposition(document_term_matrix):
    singular_value_decomposition = TruncatedSVD(100, algorithm= 'randomized')
    normalizer                   = Normalizer(copy=False)
    pipeline                      = make_pipeline(singular_value_decomposition, normalizer)

    latent_semantic_analysis     = pipeline.fit_transform(document_term_matrix)
    
    return latent_semantic_analysis
    

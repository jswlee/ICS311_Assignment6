Readme for socialmediagraphs.py and social-media-example-usage.ipynb
Authors: Jonathan Lee and Gregor Umhoefer

The Jupyter Notebook can be used to run the graph functions, as it builds a graph of users, comments, and posts. User instructions are as follows.

For Task 1: Important Post Display

Call the display_important_posts() function, arguments: display_important_posts(graph, filter, views_importance, n)
* graph: the DiGraph created by the notebook, called G
* filter: the criteria that determines post importance, only accepts the following
    * "views"
    * "comments"
    * "mixed"
* views_importance: used if "mixed" is chosen, applies a weight between 0 and 1 to the number of views, and 1 - weight to the number of comments, when determining importance.
* n: the number of top results to display. This displays them in descending order of importance.
    * E.g. if n = 1 it displays the most important, n = 2 displays the top 2


For Task 3: Wordcloud

Call the filter_posts_by_graph() function.
Args: filter_posts_by_graph(graph, include_keywords, user_filter)
  * graph: the DiGraph, G, generated by the notebook
  * include_keywords: a list of words required for a post to be included in the wordcloud
  * user_filter: a dictionary to include posts by author attributes, usage {"attribute": "type"}
    * E.g. {"gender": "male"} includes only posts by male authors

For any questions or problems with the code, please contact gregoru@hawaii.edu

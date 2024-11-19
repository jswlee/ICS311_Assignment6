import networkx as nx
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def build_social_graph(users, posts, comments):
    """
    Builds a social media graph from users, posts, and comments.

    Args:
        users (dict): Dictionary of user data.
        posts (dict): Dictionary of post data.
        comments (dict): Dictionary of comment data.

    Returns:
        nx.DiGraph: The constructed directed graph.
        post_list: A list of tuples containing post_id, number of comments, and number of views.
    """
    G = nx.DiGraph()

    # Add users as nodes
    for user_id, user_data in users.items():
        G.add_node(
            user_id,
            type="user",
            username=user_data["username"],
            age=user_data["attributes"]["age"],
            gender=user_data["attributes"]["gender"],
            location=user_data["attributes"]["location"],
            posts=user_data["posts"],
            comments=user_data["comments"],
            posts_read=user_data["posts_read"],
            color = "green"
        )


    # Add posts as nodes and connect them to their authors
    for post_id, post_data in posts.items():
        G.add_node(
            post_id,
            type="post",
            author=post_data["author"],
            content=post_data["content"],
            creation_time=post_data["creation_time"],
            comments=post_data["comments"],
            viewed_by=post_data["viewed_by"],
            color = "blue"
        )

        # Connect post to author
        G.add_edge(post_data["author"], post_id, connection_type="authored")

        # Connect viewers to the post
        for viewer in post_data["viewed_by"]:
            G.add_edge(viewer, post_id, connection_type="viewed")

    # Add comments as nodes and connect them to their posts and authors
    for comment_id, comment_data in comments.items():
        G.add_node(
            comment_id,
            type="comment",
            author=comment_data["author"],
            post_id=comment_data["post_id"],
            content=comment_data["content"],
            creation_time=comment_data["creation_time"],
            color = "magenta"
        )

        # Connect comment to author
        G.add_edge(comment_data["author"], comment_id, connection_type="authored")

        # Connect comment to post
        G.add_edge(comment_id, comment_data["post_id"], connection_type="commented_on")

    return G


def filter_posts_by_graph(graph, include_keywords=None, user_filter=None):
    """
    Filters posts based on the graph structure, user attributes, and post content keywords.
    
    Args:
        graph (nx.DiGraph): The graph representing the social network.
        include_keywords (list): List of keywords to include in the post content.
        user_filter (dict): Dictionary of user attributes to filter authors.
    
    Returns:
        list: Filtered post contents that match the criteria.
    """
    filtered_posts = []

    # Iterate through graph nodes
    for node, attributes in graph.nodes(data=True):
        # Skip non-post nodes
        if attributes.get("type") != "post":
            continue
        
        # Get post author and content
        post_author = attributes.get("author")
        post_content = attributes.get("content")

        # Check if the post author matches the user_filter
        author_attributes = graph.nodes[post_author] if post_author in graph.nodes else {}
        if user_filter and not all(author_attributes.get(k) == v for k, v in user_filter.items()):
            continue

        # Check if the post content matches include_keywords
        if include_keywords and not any(keyword.lower() in post_content.lower() for keyword in include_keywords):
            continue

        # Add post content to the result
        filtered_posts.append(post_content)
    
    return filtered_posts

# Generate a word cloud for posts filtered by user attributes
def generate_word_cloud(posts):
    text = " ".join(posts)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def display_graph(graph, important_posts = [], filter = None):
    """
    Displays the social media graph.
    
    Args:
        graph (nx.DiGraph): The graph to display.
        important_posts (list): List of important post IDs to highlight.
        filter (str): The filter used to select important posts.
    """

    plt.figure(figsize = (10, 10))
    pos = nx.spring_layout(graph, seed = 42, k = 2)
    edge_labels = nx.get_edge_attributes(graph, 'connection_type')

    title = "Social Media Graph"
    if important_posts:
        for i, node in enumerate(important_posts):
            pos[node] = ((.2 * i) - (.1 * len(important_posts)), 2)
        title += f": {len(important_posts)} Important Posts at the Top Sorted by {filter.capitalize()}"

    node_colors = [attributes.get("color") for _, attributes in graph.nodes(data = True)]
    nx.draw(graph, pos, with_labels=True, node_color = node_colors, node_size = 1000, font_size = 14)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size = 10)

    legend = [plt.Line2D([], [], marker = 'o', color = 'w', label = 'User', markerfacecolor='green', markersize = 12),
              plt.Line2D([], [], marker = 'o', color = 'w', label = 'Post', markerfacecolor='blue', markersize = 12),
              plt.Line2D([], [], marker = 'o', color = 'w', label = 'Comment', markerfacecolor='magenta', markersize = 12)]
    
    plt.legend(handles=legend, loc='lower left', title = "Nodes")
    plt.title(title)
    plt.show()

def display_important_posts(graph, filter = "mixed", views_importance = .5 ,n = 1):

    comments_importance = 1 - views_importance

    if filter == "mixed":
        post_list = [(node, (comments_importance * len(attributes.get("comments", [])) + 
                 views_importance * len(attributes.get("viewed_by", []))))
                 for node, attributes in graph.nodes(data=True) 
                 if attributes.get("type") == "post"]
    
    elif filter == "views":
        post_list = [(node, len(attributes.get("viewed_by", [])))
                 for node, attributes in graph.nodes(data=True) 
                 if attributes.get("type") == "post"]
        
    elif filter == "comments":
        post_list = [(node, len(attributes.get("comments", [])))
                 for node, attributes in graph.nodes(data=True) 
                 if attributes.get("type") == "post"]

    post_list = sorted(post_list, key = lambda x: x[1], reverse = True)[:n]
    important_posts = [post_id for post_id, _ in post_list]

    display_graph(graph, important_posts, filter)
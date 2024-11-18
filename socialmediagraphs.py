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
            posts_read=user_data["posts_read"]
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
            viewed_by=post_data["viewed_by"]
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
            creation_time=comment_data["creation_time"]
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
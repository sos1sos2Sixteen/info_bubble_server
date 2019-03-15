
from .models import Bubble, Tag, Account, Comment

def tag_serializer(tag):
    data = {
        "id" : tag.pk,
        "name" : tag.name,
        "a_rstrct" : tag.access_restriction,
        "p_rstrct" : tag.publish_restriction
    }

    return (data)

def publisher_serializer(account):
    data = {
        "id" : account.pk,
        "alias" : account.alias
    }

    return (data)

def bubble_abstract_serializer(bubble):
    data = {
        "id" : bubble.pk,
        "title" : bubble.title,
        "source" : bubble.source,
        "source_url" : bubble.source_url,
        "commit_time" : bubble.commit_stamp.__str__(),
        "likes" : bubble.likes,
        "abstract" : bubble.abstract,
        "tags" : tag_serializer(bubble.tags.all()[0]),
        "publisher" : publisher_serializer(bubble.publisher)
    }
    return (data)


def bubble_rect_serializer(bubble):
    if bubble == None:
        data = {
            "success" : 1,
            "content" : None
        }
    else:
        data = {
            "success" : 0,
            "content" : bubble.content
        }
    return (data)

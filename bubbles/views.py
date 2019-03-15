from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .codec import success,failure,userAuthentication,USER_LOGGED_IN,NO_SUCH_USER,FORMAT_ERROR
from .models import Tag, Comment, Account, Bubble
from bubbles import serializer
from .authentication import gen_auth,validate_auth
from django.utils import timezone
# Create your views here.
LIST_LENGTH = 3

@csrf_exempt
def bubble_list_handle(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        res = userAuthentication(req)

        if FORMAT_ERROR == res:
            return JsonResponse(failure(None))
        else:
            try:
                offset = req['offset'];

                if USER_LOGGED_IN == res:
                    res_set = Bubble.objects.order_by("-commit_stamp")[offset:offset + LIST_LENGTH]
                else:
                    res_set = Bubble.objects.filter(tags__access_restriction = False).order_by("-commit_stamp")[offset:offset + LIST_LENGTH]

                length = len(res_set)

                reply = {
                    "n" : length,
                    "exhaust" : not (length == LIST_LENGTH),
                    "bubbles" : []
                }

                for bub in res_set:
                    reply["bubbles"].append(
                        serializer.bubble_abstract_serializer(bub)
                    )
                
                return JsonResponse(reply)
            except KeyError:
                return JsonResponse(failure(None))
    else:
        return JsonResponse(failure(None))

@csrf_exempt
def bubble_detail_handle(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        res = userAuthentication(req);

        try:
            rids = req['requests']
            reply = {}
            for rid in rids:
                try:
                    bub = Bubble.objects.get(pk = rid)
                    bub.view_count = bub.view_count + 1
                    bub.save()

                    reply[rid] = serializer.bubble_rect_serializer(bub);
                except Bubble.DoesNotExist:
                    reply[rid] = serializer.bubble_rect_serializer(None);
        
            return JsonResponse(reply)
        except KeyError:
            return JsonResponse(failure(None))

    else:
        return JsonResponse(failure(None))

@csrf_exempt
def login_handle(request):
    if request.method == 'POST':
        req = json.loads(request.body)

        reply = {
                    "success" : 1,
                    "data" : None
                }

        try:
            user = req["user"]
            pas  = req["pass"]

            try:
                acc = Account.objects.get(account_num = user)
                # if account does exist
                if acc.password_plain == pas :
                    # pass word match
                    reply["success"] = 0
                    reply["data"] = {
                        "user" : user,
                        "auth" : gen_auth(acc)
                    }
                    return JsonResponse(reply)
                else:
                    return JsonResponse(reply)
            except Account.DoesNotExist:
                # account does not exist
                
                return JsonResponse(reply)

        except KeyError:
            # mal-formatted request
            return JsonResponse(reply)
    else:
        # wrong type of request
        return JsonResponse(reply)

@csrf_exempt
def bubble_upload_handle(request):
    if request.method == 'POST':

        req = json.loads(request.body)
        reply = {
            "success" : 1,
            "data" : {}
        }

        try:
            user = req["user"]
            auth = req["auth"]
            title = req["title"]
            content = req["content"]
            tag_id = req["tag"]

            # first check user authentication
            acct = Account.objects.get(account_num = user)
            v1 = validate_auth(acct,auth)
            # then check tag availability
            tag = Tag.objects.get(pk=tag_id)
            v2 = (tag.publish_restriction == False)

            if v1 and v2:
                # ok to publish
                # alter database
                bub = Bubble(
                    title = title,
                    source = "用户投稿",
                    source_url = "n/a",
                    commit_stamp = timezone.now(),
                    likes = 0,
                    view_count = 0,
                    content = content,
                    abstract = content[:20],
                    publisher = acct,
                )
                bub.save()
                bub.tags.set([tag])
                bub.save()
                
                reply["success"] = 0
                reply["data"] = {
                    "id" : bub.pk
                }

            return JsonResponse(reply)

        except KeyError:
            reply["data"] = {
                "error" : "keyerror"
            }
            return JsonResponse(reply)
        except Account.DoesNotExist:
            eply["data"] = {
                "error" : "account not exist"
            }
            return JsonResponse(reply)
        except Tag.DoesNotExist:
            eply["data"] = {
                "error" : "tag not exist"
            }
            return JsonResponse(reply)


    else:
        # wrong request type
        return JsonResponse(failure(None))
from django.db import models
from ..LandR.models import User

# Managers

# Thread manager, not sure yet if needed
class ThreadManager(models.Manager):
    def validator(self):
        return {}
    

# To add the posibility of multiple users in a thread I need to change:
class MessageManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if "threadId" not in postData:
            # The next line only looks at if the postData["email"] is one email, not varius, have to split to look at varius
            if not User.objects.filter(email = postData["nm_email"]):
                errors["email"] = "Receiver email doesn't exist"
        if len(postData["nm_title"].strip()) < 1:
            errors["title"] = "Title can't be blank"
        elif len(postData["nm_title"]) > 255:
            errors["title"] = "Title can't be more than 255 characters"
        if len(postData["nm_text"]) > 2000:
            errors["nm_text"] = "Message text can only have up to 2000 characters"
        return errors
    
    def creator(self, postData, sId):
        errors = self.validator(postData)
        if not errors:
            sender = User.objects.get(sessionId=sId)
            title = postData["nm_title"]
            text = postData["nm_text"]
            if "threadId" not in postData:
                tempThread = Thread.objects.create(title = title)
                tempThread.users.add(sender)
                # This is only good for conversations between two users, the next line has to change to include multiple emails
                tempThread.users.add(User.objects.get(email=postData["nm_email"]))
                tempThread.newFor.add(*(tempThread.users.all()))
            else:
                #Check if the user sending is in the thread
                tempThread = Thread.objects.get(id=postData["threadId"])
                if not Thread.objects.filter(id=postData["threadId"]).filter(users__in=User.objects.filter(sessionId=sId)):
                    return {"problem":"You're not a part of this conversation"}
                tempThread.newFor.add(*(tempThread.users.all()))
            newMessage = Message.objects.create(sender = sender, thread = tempThread, title = title, text = text)
            tempThread.save()
            return {"success":newMessage}
        return errors

# Models
class Thread(models.Model):
    title = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="threads")
    newFor = models.ManyToManyField(User, related_name="new_threads")
    latest_message = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ThreadManager()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="messages")
    thread = models.ForeignKey(Thread, related_name="messages")
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()
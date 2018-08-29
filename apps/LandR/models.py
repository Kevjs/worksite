from django.db import models
import bcrypt

# Managers
class TitleManager(models.Manager):
    def Title_Validator(self, postData):
        errors = {}
        if len(postData["title_title"].strip()) < 1:
            errors["title_title"]="Title's title is blank"
        elif len(postData["title_title"]) > 255:
            errors["title_title"]="Title's title is too long (max 255 chars)"
        elif Title.objects.filter(title = postData["title_title"]):
            errors["title_title"] = "Title's title already exists"
        if len(postData["title_description"].strip()) < 1:
            errors["title_description"]="Title's description is blank"
        elif len(postData["title_description"]) > 255:
            errors["title_description"]="Title's description is too long (max 255 chars)"
        return errors

    def Title_Creator(self, sId, postData):
        user = User.objects.filter(sessionId = sId)
        if not user:
            return {"wrong_login_info":"No User with that sessionId"}
        errors = self.Title_Validator(postData)
        if errors:
            return errors
        user = user.first()
        if user.website_power.level >= 500:
            return {"success":Title.objects.create(title=postData["title_title"], description=postData["title_description"])}
        return {"error":"A non-admin tried to create a title"}

class LevelManager(models.Manager):
    def Level_Validator(self, postData):
        errors = {}
        if len(postData["website_power_level"].strip()) < 1:
            errors["website_power_level"]="Power level is blank"
        elif len(postData["website_power_level"]) > 255:
            errors["website_power_level"]="Power level is too long (max 255 chars)"
        if len(postData["website_power_title"].strip()) < 1:
            errors["website_power_title"]="Power level title is blank"
        elif len(postData["website_power_title"]) > 255:
            errors["website_power_title"]="Power level title is too long (max 255 chars)"
        elif Level.objects.filter(title=postData["website_power_level"]):
            errors["website_power_title"] = "Power level title already exists"
        return errors

    def Level_Creator(self, sId, postData):
        user = User.objects.filter(sessionId = sId)
        if not user:
            return {"wrong_login_info":"No User with that sessionId"}
        errors = self.Level_Validator(postData)
        if errors:
            return errors
        user = user.first()
        if user.website_power.level >= 500:
            if user.website_power.level >= int(postData["website_power_level"]):
                return {"success": Level.objects.create(title=postData["website_power_title"], level=postData["website_power_level"])}
            else:
                return {"error":"Tried to create a level power over their own power"}
        return {"error":"A non-admin tried to create a level power"}

class UserManager(models.Manager):
    def User_Validator(self, postData):
        # Add regex restrictions and/or any type of restriction on the creation of users here
        errors = {}
        if len(postData["first_name"].strip()) < 1:
            errors["first_name"]="First name can't be blank"
        elif len(postData["first_name"]) > 255:
            errors["first_name"]="First name is too long (max 255 chars)"
        if len(postData["last_name"].strip()) < 1:
            errors["last_name"]="Last name can't be blank"
        elif len(postData["last_name"]) > 255:
            errors["last_name"]="Last name is too long (max 255 chars)"
        if len(postData["email"].strip()) < 1:
            errors["email"]="Email can't be blank"
        elif len(postData["email"]) > 255:
            errors["email"]="Email is too long (max 255 chars)"
        elif User.objects.filter(email=postData["email"]):
            errors["email"]="Email already exists"
        if "password" in postData:
            if len(postData["password"].strip()) < 1:
                errors["password"]="Password can't be blank"
            elif len(postData["password"]) > 30:
                errors["password"]="Password is too long (max 30 chars)"
            # Add whatever restrictions we want on password
        return errors
    
    def logger(self, postData):
        if User.objects.filter(email=postData["email"]):
            if bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData["email"]).password.encode()):
                return {"success": User.objects.get(email=postData["email"])}
        return {"error":"Email or password doesn't match"}
    
    def creator(self, sId, postData):
        # Check if all the input is correct before creating to avoid duplicates
        errors = self.User_Validator(postData = postData)
        if postData["select_title"] == "new":
            titleErrors = Title.objects.Title_Validator(postData)
            errors.update(titleErrors)
        if postData["select_level"] == "new":
            levelErrors = Level.objects.Level_Validator(postData)
            errors.update(levelErrors)
        if errors:
            return errors

        # Since all checks came back positive proceed to create titles/levels as needed
        if postData["select_title"] == "new":
            t = Title.objects.Title_Creator(sId, postData)
            t = t["success"]
        else:
            t = Title.objects.get(title=postData["select_title"])
        
        if postData["select_level"] == "new":
            l = Level.objects.Level_Creator(sId, postData)
            l = l["success"]
        else:
            l = Level.objects.get(title=postData["select_level"])
        
        # Now that we have everything create and return the new user
        user = {"success" : User.objects.create(first_name=postData["first_name"], last_name = postData["last_name"], email = postData["email"], password = bcrypt.hashpw("123".encode(), bcrypt.gensalt()), sessionId = bcrypt.hashpw(postData["email"].encode(), bcrypt.gensalt()), phone_number = postData["phone_number"],title=t,website_power=l)}
        return user
    
    def first(self, postData):
        errors = self.User_Validator(postData)
        if errors:
            return errors
        t = Title.objects.create(title = postData["title_title"], description = postData["title_description"])
        l = Level.objects.create(title = postData["title_title"], level = 1000)
        user = {"success" : User.objects.create(first_name=postData["first_name"], last_name = postData["last_name"], email = postData["email"], password = bcrypt.hashpw("123".encode(), bcrypt.gensalt()), sessionId = bcrypt.hashpw(postData["email"].encode(), bcrypt.gensalt()), phone_number = postData["phone_number"],title=t,website_power=l)}
        return user
        
# Models

# User Job function
class Title(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TitleManager()

# Level Class is used to store different user classification for the webpage. Giving
# the opportunity to create limited site functionality to higher up workers and vice-versa
class Level(models.Model):
    title = models.CharField(max_length=255)
    level = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LevelManager()

# Base User Model
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    status = models.TextField()
    phone_number = models.CharField(max_length=25)
    password = models.CharField(max_length=255)
    sessionId = models.CharField(max_length=255)
    title = models.ForeignKey(Title, related_name="workers")
    website_power = models.ForeignKey(Level, related_name="workers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
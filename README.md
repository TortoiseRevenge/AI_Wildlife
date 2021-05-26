# AI_Wildlife
This project was originally designed to: <br>
&ensp;&ensp;&ensp;    1. Receive an image from a trail camera <br>
&ensp;&ensp;&ensp;    2. Send that image to Microsoft's AI for Earth and get back the species, family, etc. <br>
&ensp;&ensp;&ensp;    3. Post that Image to Twitter with Data<br>
&ensp;&ensp;&ensp;    4. Store the Image and data received into a database<br>
    <br>
While this "Phase 1" system is still here, our final product now also includes the ability to do everything the same, but step 1 is:<br>
    &ensp;&ensp;&ensp;1. Receive an image from Twitter<br>
&ensp;and 3:<br>
    &ensp;&ensp;&ensp;3. Reply to the image with Data<br>
    <br>
This file will go over how exactly we were able to get this done using Azure and the functions in this repository.<br>
# Phase 1

Requirements for Phase 1: <br>
&ensp;&ensp;&ensp;    1. An Azure Account <br>
&ensp;&ensp;&ensp;    2. An API key from AI for Earth, accessible at https://www.microsoft.com/en-us/ai/ai-for-earth-tech-resources#primaryR7 <br>
&ensp;&ensp;&ensp;    3. A Twitter Account to post to <br>
&ensp;&ensp;&ensp;    4. An Email Account to get Emails to (Unless there is another way for you to automatically get the images from a trail cam) <br>
&ensp;&ensp;&ensp;    5. An Onedrive Account (You can easily get this for free by simply using the Email Account you got in step 4) <br>
    <br>
You'll want to begin this process by creating a Logic App on Azure, with the trigger "When a New Email Arrives". The exact one you use depends on your email account provider. In my case, I had it sent to an outlook account, and so I used the Outlook Conncetor's trigger.
![image](https://user-images.githubusercontent.com/56144316/119371481-19380380-bc7c-11eb-8073-da6b20db1af6.png)
Turn the "Only with Attachments" and "Include Attachments" to On. This allows us to get the attachments that the emails are sent with, as well as to make sure we aren't sending an email not related to the project (assumming you don't get attachments commonly). Make sure to actually connect the email to the connector.


<br><br> Next Up we are going to create a for each loop. This for each loop will go over each attachment. this is useful in case the email contains multiple emails (and Azure makes the for loop here mandatory). 

<br><br> The first action we will do inside will be a create file, in the onedrive connector. 
![image](https://user-images.githubusercontent.com/56144316/119372756-4c2ec700-bc7d-11eb-9ea3-d9d728c98387.png)
Follow the Above Configuration, although you can change the Folder Path to whatever folder you would like to store the images in. Make sure to also connect your Onedrive account in this step.
<br><br>
Directly after this create a "Get File Content Using Path".
![image](https://user-images.githubusercontent.com/56144316/119374123-d297d880-bc7e-11eb-86ef-0543eec8d176.png)
The "Path" is from the "Create File" you  had done before.
<br>
This next task is redundant, so you don't have to do it. First, create a Storage Account in Azure, and then inside of it create a container, with whatever name you would like. 
<br>
Once you are done, go back to your logic app.
Add a "Create Blob" Action. Make sure to connect it to the storage account, and then follow the rest of these inputs (unless you have changed your folder path). ![image](https://user-images.githubusercontent.com/56144316/119375390-5e5e3480-bc80-11eb-8799-6214bd5b4261.png)
<br>
We are now going to create an HTTP Trigger which will actually get the AI results from Microsoft. The First result for Actions under "HTTP Trigger" should be the one to choose. Once you have the action, input the following
![image](https://user-images.githubusercontent.com/56144316/119686467-f9374a00-be0b-11eb-8a30-af21f684c171.png)<br>
&ensp;&ensp;&ensp;URI - The Actual HTTP URL / I to Microsoft. In this case, we are using the latest version, https://aiforearth.azure-api.net/species-classification/v2.0/predict <br>
&ensp;&ensp;&ensp; Content-Type - Dynamic Content from your for each action, specifically the "Attachments Content-Type" <br>
&ensp;&ensp;&ensp; Ocp-Apim-Subscription-Key - Input the API key from AI For Earth <br>
&ensp;&ensp;&ensp; Body - This sends the actual image for the AI to go through,, so in this case you send the file content from your Onedrive file creation
<br><br>
Next Up we'll have to actually parse the data we just got from AI for Earth, which was sent in JSON. So to do this we'll use the "Parse JSON" Action. For Content input the "Body" element from the HTTP Trigger, and then input the following code into the Schema:
```
{
    "properties": {
        "bboxes": {
            "items": {
                "properties": {
                    "confidence": {
                        "type": "number"
                    },
                    "x_max": {
                        "type": "number"
                    },
                    "x_min": {
                        "type": "number"
                    },
                    "y_max": {
                        "type": "number"
                    },
                    "y_min": {
                        "type": "number"
                    }
                },
                "required": [
                    "confidence",
                    "x_max",
                    "x_min",
                    "y_max",
                    "y_min"
                ],
                "type": "object"
            },
            "type": "array"
        },
        "predictions": {
            "items": {
                "properties": {
                    "class": {
                        "type": "string"
                    },
                    "class_common": {
                        "type": "string"
                    },
                    "confidence": {
                        "type": "number"
                    },
                    "family": {
                        "type": "string"
                    },
                    "family_common": {
                        "type": "string"
                    },
                    "genus": {
                        "type": "string"
                    },
                    "genus_common": {
                        "type": "string"
                    },
                    "kingdom": {
                        "type": "string"
                    },
                    "kingdom_common": {
                        "type": "string"
                    },
                    "order": {
                        "type": "string"
                    },
                    "order_common": {
                        "type": "string"
                    },
                    "phylum": {
                        "type": "string"
                    },
                    "phylum_common": {
                        "type": "string"
                    },
                    "species": {
                        "type": "string"
                    },
                    "species_common": {
                        "type": "string"
                    },
                    "subphylum": {
                        "type": "string"
                    },
                    "subphylum_common": {
                        "type": "string"
                    },
                    "subspecies": {
                        "type": "string"
                    },
                    "subspecies_common": {
                        "type": "string"
                    }
                },
                "type": "object"
            },
            "type": "array"
        }
    },
    "type": "object"
}
```

<br><br>

Now that we have the data, we can actively  use it. First, we'll post it to Twitter.
<br>
Unlike what you might do in the second logic app, Logic App thankfully has an integrated wy to post a main tweet to Twitter, directly integrated with it. You won't even have to get an API key from twitter to do this, just an account.
<br>
All you have to do is use the "Post A Tweet" action from the Twitter Connector, connect your account, and input the info. In my case I wanted the post to include the species, species' family name, and the confidence, so I put in the  "Tweet Text" Section the following:
![image](https://user-images.githubusercontent.com/56144316/119689299-592ef000-be0e-11eb-893e-85ca1b4ac038.png)
<br> You won't have to implement those For each loops yourself, as they are automatically added when you input the dynamic variables. Also make sure to add your "file content" (the image) to the media section, so the image will be included with the text.
<br>
Our last action in this Logic App is to save the information to a database for further analytics. For this, we are using a Cosmos DB, although you can choose SQL or whatever other DB type you like, albeit with some modification to the following steps. In our case, we simply used the Cosmos DB "Create or update document", specifically Version 2. In the case of Cosmos our action looked like this:
![image](https://user-images.githubusercontent.com/56144316/119689959-e7a37180-be0e-11eb-956b-e130fde38a89.png)
If you want to copy that exactly, you can use this code: ```{
  "blob_etag": "@{body('Create_blob_2')?['ETag']}",
  "blob_filelocator": "@{body('Create_blob_2')?['FileLocator']}",
  "blob_name": "@{body('Create_blob_2')?['Name']}",
  "blob_path": "@{body('Create_blob_2')?['Path']}",
  "class": "@{items('For_each')?['class']}",
  "class_common": "@{items('For_each')?['class_common']}",
  "confidence": "@{items('For_each')?['confidence']}",
  "family": "@{items('For_each')?['family']}",
  "family_common": "@{items('For_each')?['family_common']}",
  "genus": "@{items('For_each')?['genus']}",
  "genus_common": "@{items('For_each')?['genus_common']}",
  "id": "@{triggerBody()?['Id']}",
  "image_id": "@{body('Create_file')?['Id']}",
  "image_link": "@{body('Create_file')?['Path']}",
  "kingdom": "@{items('For_each')?['kingdom']}",
  "kingdom_common": "@{items('For_each')?['kingdom_common']}",
  "order": "@{items('For_each')?['order']}",
  "order_common": "@{items('For_each')?['order_common']}",
  "phylum": "@{items('For_each')?['phylum']}",
  "phylum_common": "@{items('For_each')?['phylum_common']}",
  "species_common": "@{items('For_each')?['species_common']}"
}```<br>(although you can change it as you wish)
<br><br>
That is all for this initial DB, which should allow you to send images to it either from a trail camera or simply manually and have the image and classification tweeted out with it. The following logic app will then be what I'm calling "Phase 2", that being direct capture of images from Twitter and classification in a reply.

# Phase 2

You'll need all the things from Part 1, but you wil also need one more thing. **A Twitter API Key**. Be advised that your API Key for this may be banned while testing, so be careful and follow all the rules advised. To get the key itself, you can go to https://developer.twitter.com/en. Follow the instructions in the "apply" section.
<br>
The general makeup of this phase is pretty similar to the first. Instead of using an email trigger, we instead used a twitter connecter. This is designed to do the same task however, effectively checking if anything has been updated. ![image](https://user-images.githubusercontent.com/56144316/119693251-b8daca80-be11-11eb-90cf-962e1177c4d3.png)
<br>
In our case, we simply looked whenever somebody would "@" our Twitter account. <br>
After the connector we go back to similar fields as phase 1. The biggest thing that changes is the main for each loop goes is focused on the media urls of the tweet, not the email's attachments. This for each loop also serves as a protection from if the account is "@ed" with text, since if the tweet does not contain the image media url the loop will just be skipped, and if a tweet contains multiple images, each one can be searched.
<br>
![image](https://user-images.githubusercontent.com/56144316/119694087-85e50680-be12-11eb-8fb4-2ff5ad93fc27.png)<br>
Most of the changes are simply to change the dynamic variables from the Outlook ones to Twitter, although there is also another big change. Intstead of a "create file" action, we instead use the "upload file from URL action". This allows the actual image from twitter to be downloaded, with the source url taken being the "current item" of the for loop. The only big change here is the "Content-Type" in the HTTP trigger. We have no variables for the content type here, so instead we just send "application/octet-stream". <br><br>
![image](https://user-images.githubusercontent.com/56144316/119695984-5800c180-be14-11eb-8367-c376b877401a.png)
<br>
The Parse JSON also uses the exact same info as in phase 1. <br>
Now with the data, we are going to reply to the tweet that sent the image. You can use nearly the same code for the adding to database, albeit with some of the changes to accouunt for the input being from Twitter, not an email.
<br><br>
The big change however is with the reply. For whatever reason the Twitter Connector does not have the ability for replys. At best you can quote tweet someone, although that is hard for the end user to actaully see it, and especially hard for anyone to actually see that your account is doing anything. For this, we will instead be using an Azure Function.

TO BE COUNTINUED

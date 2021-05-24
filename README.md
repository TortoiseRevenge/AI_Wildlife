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
We are now going to create an HTTP Trigger 

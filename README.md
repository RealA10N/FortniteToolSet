# FortniteToolSet
A Tool-Set for my personal use.
Accesses different fortnite api's and generates info and images from them.
used mostly in my [instagram page](https://www.instagram.com/reala10n/).

## "News" script
- First version: [FortniteNewsToStoryImageGenerator.py](FortniteNewsToStoryImageGenerator.py)
- Second version **(Recommended):** [v2_FortniteNewsToStoryImageGenerator.py](v2_NewsToStoryImage.py)
- _Assets folder:_ [/NewsGeneratorAssets](/NewsGeneratorAssets)

#### What does it do?
1. The script will download the current Fortnite news info from an api.
2. The script will let the user select one news item from the 3 of the api.
3. The script will import the needed assets from the [assets folder](/NewsGeneratorAssets).
4. The script will create a image from the news info.

#### Visual Example
![News Example Image](<https://i.imgur.com/jUAlydC.png>)  

## "ItemShop" script
- First version: [Fortnite Item Shop To Story Image.py](Fortnite Item Shop To Story Image.py)
- Second version: [v2_Fortnite Item Shop To Story Image.py](v2ItemShopToStoryImage.py)
- Third version **(recommended)**: [v3_FortniteItemShopToStoryImage.py](v3_ItemShopToStoryImage.py)
- _Assets folder:_ [/ItemsAssets](/ItemsAssets)

#### What does it do?
1. The script will download the current Fortnite item shop info from an api.
2. It will run an algorithm to check how many featured and non-featured items there are in the shop (version 3+ only).
3. The script will create icons for every item, and place them in order on a background image.
4. If needed, more then one image will be created and saved (version 3+ only).

#### Visual example
![ItemShop visual example](<https://i.imgur.com/2FsR71e.png>)  

## "Featured" script
- The script: [FortniteFeaturedSkinToStory.py](FortniteFeaturedSkinToStory.py)
- _Assets folder:_ [/FeaturedSkinToStoryAssets](/FeaturedSkinToStoryAssets)

#### What does it do?
1. The script will download the current Fortnite item shop info from an api.
2. From all the items in the shop, it will search for featured skins only.
3. After it found the featured skins, it will let the user choose only one skin.
4. The script will generate an image with matching background and save it.

#### Visual example
![Featured visual example](<https://i.imgur.com/jUAlydC.png>)    

## "Routine" script
- The script: [AllScriptsRoutine.py](AllScriptsRoutine.py)

#### What does it do?
1. This script will import the [ItemShop](#itemshop-script), [News](#news-script) and [Featured](#featured-script) scripts, and will run them all together.

2. All the images generated from the imported scripts will be saved in a new folder named "RoutineFinalImages"

3. The script will send all the files in the "RoutineFinalImages" folder to the email given in the [ToolSetSettings.json](ToolSetSettings.json) file ([_read more here_](#"ToolSetSettings.json"-file)).

#### Visual example
![Routine visual example](<https://i.imgur.com/zeucYmj.png>)    

## "Email" Script
- The script: [SendEmail.py](SendEmail.py)

#### What does it do?
This script is for import only. by using the `SendEmail()` class, you will be able to send emails easily!

#### Class functions
- `.login(your_gmail, your_password)`  
Will login you to gmail servers.
- `.add_recipient_address('recipient@mail.com')`  
Adds recipient email.
- `.clear_recipients()`  
Will clear all recipients from the list. you can still add new ones!
- `set_subject('my title!')`  
Will set the the title of the email.
- `.add_body('this is the text in the mail')`  
Will add text to the email's body.
- `.add_file('file_path')`  
Will add file to the attachments list.
- `.clear_files()`  
Will clear all files from attachments list. you can still add new ones!
- `.send_mail()`  
Will push all the info to the server, and send the email!

#### Example

Running:  
```python
from SendEmail import SendEmail

mail = SendEmail()
mail.add_recipient_address('daniel@gmail.com')
mail.add_recipient_address('bob@gmail.com')
mail.set_subject('this is my title!')
mail.add_body('this is my body (:')
mail.login('your_mail@gmail.com', 'PasswordToMail')
mail.send_mail()
mail.server_quit()
```

Result should be something like this:  
![Email script result](https://i.imgur.com/fSbBoWG.png)  

## "ToolSetSettings.json" file
* The file: [ToolSetSettings.json](ToolSetSettings.json)

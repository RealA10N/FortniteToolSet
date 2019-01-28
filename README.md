# **FortniteToolSet**
A Tool-Set for my personal use.
Accesses different fortnite api's and generates info and images from them.
used mostly in my [instagram page](https://www.instagram.com/reala10n/).

## **"News"** script
- First version: [_FortniteNewsToStoryImageGenerator.py_](FortniteNewsToStoryImageGenerator.py)
- Second version **(Recommended):** [_v2_FortniteNewsToStoryImageGenerator.py_](v2_NewsToStoryImage.py)
- _Assets folder:_ [_/NewsGeneratorAssets_](/NewsGeneratorAssets)

#### What does it do?
1. The script will download the current Fortnite news info from an api.
2. The script will let the user select one news item from the 3 of the api. 
3. The script will import the needed assets from the [_assets folder_](/NewsGeneratorAssets).
4. The script will create a image from the news info.

#### Example
- The script will download all the info from the api:<br />
![Fortnite in game news](https://i.imgur.com/rA5KOOw.png)
- It will then go to the [_assets folder_](/NewsGeneratorAssets) and import all the needed assets:<br />
![News assets](https://i.imgur.com/MPprH8P.png)
- Finally, the script will put all the images together and save the result:<br />
![News script result](https://i.imgur.com/p3EZqw7.png) 

## **"ItemShop"** script
- First version: [_Fortnite Item Shop To Story Image.py_](Fortnite Item Shop To Story Image.py)
- Second version **(recommended)**: [_v2_Fortnite Item Shop To Story Image.py_](v2_ItemShopToStoryImage.py)
- Third version **(Still in development)**: [_v3_FortniteItemShopToStoryImage.py_](v3_ItemShopToStoryImage.py)
- _Assets folder:_ [_/ItemsAssets_](/ItemsAssets)

#### What does it do?
The script is the complicated one from the three.
1. The script will download the current Fortnite item shop info from an api.
2. It will run an algorithm to check how many featured and non-featured items there are in the shop (version 3+ only).
3. The script will create icons of every item, and place them in order on a background image.

#### Example
- The script will download all the info from the api:<br />
![Fortnite Item Shop](https://i.imgur.com/Yt0YR4R.png)
- It will then go to the [_assets folder_](/ItemsAssets) and import all the needed images:<br />
![Item shop assets image](https://i.imgur.com/f80DOoa.png)
- Finally, the script will put all the items on the background image:<br />
![Item shop assets image](https://i.imgur.com/nDCEHNE.png)


## **"Featured"** script
- The script: [_FortniteFeaturedSkinToStory.py_](FortniteFeaturedSkinToStory.py)
- _Assets folder:_ [_/FeaturedSkinToStoryAssets_](/FeaturedSkinToStoryAssets)

#### What does it do?
1. The script will download the current Fortnite item shop info from an api.
2. From all the items in the shop, it will search for featured skins only.
3. After it found the featured skins, it will let the user choose only one skin.
4. The script will generate an image with matching background and save it.

#### Example
- The script will download and get this image from the api:<br />
![Skin image](https://i.imgur.com/vwa2uqi.png)
- It will then go to the [_assets folder_](/FeaturedSkinToStoryAssets) and get the matching assets:<br />
![Assets image](https://i.imgur.com/bU0WgNa.png)
- The script will put the skin image on the background image, with the overlay image on top:<br />
![Final result](https://i.imgur.com/X9HN6RX.png)



## The Future
**This is what i'm planning on developing and upgrading next in this project!**
- [x] Create a better looking and more detailed "readme" file! :blush:
- [x] Improve the "ItemShop" script, and create a third version of it. (In progress)
  - [x] Create an algorithm that will choose a way to display the items in the final image. (Done in update 3.0)
  - [ ] Create a new 4on5 grid to display more then 12 items (3on4 grid) like now.
  - [ ] Create a feature that determines if an item is making the first appearance in the item shop, and display it differently.
- [ ] Create an "Morning routine" script, that will run "News", "ItemShop" and "Featured" scripts automaticlly.
  - [ ] Make all the scripts compatible with importing them.
    - [x] [_v2_ItemShopToStoryImage.py_](v2_ItemShopToStoryImage.py)
    - [ ] [_v2_FortniteNewsToStoryImageGenerator.py_](v2_NewsToStoryImage.py)
    - [ ] [_FortniteFeaturedSkinToStory.py_](FortniteFeaturedSkinToStory.py)
- [ ] Automate all the scripts, to work automatically and detect updates when needed.
- [ ] Add a "BeforeYouStart.md" file to repo. it will explaine how to install all the needed liberies, and more!
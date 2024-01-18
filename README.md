# DnD-Simple-Engine

Sometimes you want to set up an RPG game or campaign in which the scenarios are shown through a screen, to give more immersion music is added to those images, but it can be clumsy to do it separately, one by one, when the game should be dynamic, also, the solutions that are out there often require too much preparation time or are very complex.

The idea of the project is to provide a simple story generation engine, in which you simply want to show an image with a particular music or sound, in a fast and dynamic way, without many problems.

**NOTE:** The project is still in its alpha phase, so there may be bugs or missing features that will be added later.

**VERSION NOTE:** The current version is 0.1.x, so the generation of scenes for the game must be defined manually in a json file, until we can implement a solution within the engine. The steps are listed below.

## 🔧 Setup:

1. In the engine folder, go to the `assets/images/personalized` folder and create a folder with the name of your campaign, for example: `my-campaign`.

2. Put the images you want to use in the folder you just created.

3. Then, go to the `assets/audio/personalized` folder and create a folder with the name of your campaign again, for example: `my-campaign`.

4. Put the audios you want to use in the folder you just created.

5. Define your campaign. Go to the `docs/save_data` folder and edit the `000.json` file, put your configuration, in `character` leave it as it is since it has not yet been implemented, in the `scenes` section, add the scenes you want to use. Example:

```json
{
    "id": "000",
    "name": "The Pharos Cult",
    "description": "",
    "characters": {
        "Name": {
            "player": "",
            "race": "",
            "subrace": "",
            "background": "",
            "class": "",
            "level": "",
            "description": ""
        }
    },
    "scenes": {
        "Taverna": {
            "image_path": "./assets/images/personalized/El culto a Pharos/scenes/tavern.webp",
            "audio_path": "./assets/audio/personalized/El culto a Pharos/Tavern.mp3",
            "description": ""
        },
        "Travel path": {
            "image_path": "./assets/images/personalized/El culto a Pharos/scenes/travel_path.webp",
            "audio_path": "./assets/audio/personalized/El culto a Pharos/travel_path.mp3",
            "description": ""
        }
    }
}
```

6. All done, now you can run the engine through the `Simple-Dnd-Engine.exe` file in the root folder.

## ⚡Requirements

- CPU: 1.6 GHz or higher processor
- RAM: 1 GB 
- Hard Disk: 200 MB
- OS: Windows 10 or higher

## 🖊️ Author

- Agustín Montaña - [GitHub](https://github.com/Agustinm28)
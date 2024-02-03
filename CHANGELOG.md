## [0.2.0] - 2024-01-28

### Added
- Added a CHANGELOG.md file
- Added a "Repository" of assests in engine to load and optimize image or audio assets and be used in different campaigns
- Added a "New campaign" screen to create a new campaign with name, description, images and asociated audio
- Added an audio and image repository folder
- Added icon to program
- Added classes to handle the creation of a new campaign
- Added pygame_gui support with a theme.json file for themed elements
- In scene battle music added with the key a pressed
- Added an option to edit or delete a campaign

### Changes
- Save data now is defined in a json file inside the engine
- Resolution menu is now a dropdown in options
- Fullscreen button changed

### Fixes
- Bugs fixed
- Fixed a bug that caused the font to not scale with the resolution

## [0.1.3] - 2024-01-21

### Added
- Added a new module to handle the game state
- Added a new module to handle the game loop
- Added a new module to handle the game events
- Added a new module to handle the game input
- Added a "Loading" screen
- Added a "Campaigns" screen to select the campaign to load

### Changes
- Refactor of code to make it more readable
- Added comments to code
- Added more documentation to README.md

### Fixes
- Multiple bugs fixed and code optimized

## [0.1.2] - 2024-01-15

### Added
- Image enhancement module, wich optimice image format and scales it to the desired size
- Audio enhancement module, wich optimice audio format
- Engine buffer module, wich allows to load and unload assets from memory
- Scenes buffer module, wich allows to load and unload scenes from memory
- Engine json, wich have all the engine configuration
- Options menu with resolutions and fullscreen options

### Changes
- Refactor of code to make it more readable
- Added comments to code
- Added more documentation to README.md
- Long audio is now streamed instead of loaded into memory
- Music now loops and fades in and out

### Fixes
- Fixed a bug that caused the program to crash when the image was not found
- Fixed a bug that caused the program to crash when the audio was not found
- Fixed a bug in buttons that make them not work properly
- Fixed a bug in buttons that make them stash themselves
- Fixed a bug in buttons that make them not appear when they should
- Memory leak fixed
- Memory use reduced sustantially (from 2.5GB to 70MB)
- Fixed resolution now can be changed without restarting the program
- Fixed a bug where the program crashed if a campaign was not found or not defined correctly

## [0.1.1] - 2024-01-12

### Changes
- Refactor of code to make it more readable
- Added comments to code
- Added more documentation to README.md
- Assets load has been optimized
- Image and audio loading has been optimized


## [0.1.0] - 2024-01-09

### Added
- Initial release
- README.md
- Show basic image and audio functionality
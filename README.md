# CrewHelp
Tool designed to help crewmates expose imposters in Among Us.
This script would not exist without the excellent work of Ben from Learn Code By Gaming. Go [check him out !](https://www.youtube.com/c/LearnCodeByGaming)

## What does this tool do ?
The purpose of this tool is to display a map giving the last positions of the players encountered at each meeting. By running the main script while Among Us is opened, a map will be displayed during each meeting. On this map, encountered players and their timings are shown so you can spot liars and debunk impostors !

## WIP
Color recognition is not 100% accurate but can track most of the crewmates with little to no skin (hat/pants). __The script only works on the map The Skeld !__ Here are some screenshots of the program :
![demo_medbay.png](https://github.com/dorian-bucaille/CrewHelp/blob/main/illustration/demo_medbay.png?raw=true)
![demo_nav.png](https://github.com/dorian-bucaille/CrewHelp/blob/main/illustration/demo_nav.png?raw=true)

## Done
- [x] Basic player detection
- [x] Retrieve players' positions and timings
- [x] Display a map with players' positions and timings
- [x] Show up the map when meetings occur
- [x] Clean code up
- [x] Display map using QT

## To improve...
- [ ] Overall program ergonomics like map fonts, marker positions, etc.
- [ ] Create an executable
- [ ] Publish a first release
- [ ] Advanced player detection with ML

## Other
I'm fully aware that image recognition is absolutely not the best way to track players in Among Us. This project is mainly a way for me to learn new techniques and technologies in Python.

__I do not encourage people to cheat in online games and am not responsible for any abuse. Do not use this script in online games__.

```
\\             //    ooo        ooooo   .oooooo.    ooooooooooooo ooooooooooooo
 \\\' ,      / //    `88.       .888'  d8P'  `Y8b   8'   888   `8 8'   888   `8
  \\\//,   _/ //,     888b     d'888  888      888       888           888
   \_-//' /  //<,     8 Y88. .P  888  888      888       888           888
     \ ///  <//`      8  `888'   888  888      888       888           888
    /  >>  \\\`__/_   8    Y     888  `88b    d88b       888           888
   /,)-^>> _\` \\\   o8o        o888o  `Y8bood8P'Ybd'   o888o         o888o
   (/   \\ //\\
       // _//\\\\o   ooooo       .o.  oooooo   oooooo     oooo oooo    oooo
      ((` (( `888'   `888'      .888.  `888.    `888.     .8'  `888   .8P'
              888     888      .8"888.  `888.   .8888.   .8'    888  d8'
              888ooooo888     .8' `888.  `888  .8'`888. .8'     88888[
              888     888    .88ooo8888.  `888.8'  `888.8'      888`88b.
              888     888   .8'     `888.  `888'    `888'       888  `88b.
             o888o   o888o o88o     o8888o  `8'      `8'       o888o  o888o
```
*MQTT Hawk* is a Python application, which subscribes to MQTT topics and is able to perform actions based on MQTT messages.

Very similar to [jpmens/mqttwarn](https://github.com/jpmens/mqttwarn), but with less features.

MQTT Hawk supports:
- Python 3.6+
- YAML config inspired by [Home Assistant](https://github.com/home-assistant/home-assistant)
- pluggable components


### Installation
```
$ git clone https://github.com/romanpeters/mqtt-hawk
$ cd mqtt-hawk/
$ pip install -r requirements.txt
```
Edit `config.yaml.example` and rename it to `config.yaml`.
Install the dependencies for the components you're using.
```
$ python3 mqtthawk
```

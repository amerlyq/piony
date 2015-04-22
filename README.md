piony
======

Radial menu for Wacom / mouse
---------------------
Layered radial menu with multiple levels, designed with Wacom stylus in mind.

I'm not saying «use this», it's rather «use best».

What left is to make the best this one.

Description
-----------


Usage
-----
Press and release chosen button on Wacom (I personally recommend ring central Button 1).
Radial menu will appear. You can press on any sector to generate action.

(Hold button, draw line to petal, release!)


Depends
-------
 * [Python3](https://www.python.org/) -- main language
 * [xdotool](http://www.semicomplete.com/projects/xdotool) -- keys emulation
 * [xbindkeys](http://www.nongnu.org/xbindkeys/xbindkeys.html) -- binds Wacom to menu

Script ```deploy``` will notify you about all missing dependencies.

Install
-------
Setup one of Wacom button to unusable key (like ```<F28>```)
```
  xsetwacom "$WPAD" Button 1 "key f28"
```

Bind launching of script on this keys in xbindkeys
```
  printf "\"piony\"\n    F28\n" > ~/.wacom_xbindkeys
  xbindkeys -f ~/.wacom_xbindkeys
```

Now when pressing Wacom button binded to ```<F28>```, menu will be launched.

There is already written ```deploy``` script, which will set all that by itself.

Custom Environment
-------------------
 * Make window floating for i3wm: {```~/.i3/config```}
```
  for_window [class="^piony.py"] floating enable
```
 * Disable shadow in compton: {```~/.config/compton.conf```}
```
  shadow-exclude = [ "class_g = 'piony.py'" ];
```


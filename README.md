piony
======

[![Join the chat at https://gitter.im/amerlyq/piony](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/amerlyq/piony?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/amerlyq/piony.svg)](https://travis-ci.org/amerlyq/piony)
[![Coverage Status](https://coveralls.io/repos/amerlyq/piony/badge.svg?branch=master&service=github)](https://coveralls.io/github/amerlyq/piony?branch=master)
[![Stories in Ready](https://badge.waffle.io/amerlyq/piony.png?label=ready&title=Ready)](https://waffle.io/amerlyq/piony)


Radial menu for Wacom / mouse
---------------------
Layered radial menu with multiple levels, designed with Wacom stylus in mind.

I'm not saying «use this», it's rather «use best».

What left is to make the best this one.


Description
-----------
Nonintrusive fast-emerging cascade menu.


Usage
-----
Press and release chosen button on Wacom (I personally recommend ring central Button 1).
Radial menu will appear. You can press on any sector to generate action.

(Hold button, draw line to petal, release!)


Depends
-------
 * [Python3](https://www.python.org/) -- main language
 * [Qt5](https://www.qt.io/) -- main framework
 * [yaml](http://yaml.org/) -- interface configs format
 * [xdotool](http://www.semicomplete.com/projects/xdotool) -- keys emulation
 * [xbindkeys](http://www.nongnu.org/xbindkeys/xbindkeys.html) -- binds Wacom to menu

Script ```deploy``` will notify you about all missing dependencies.


# Note #
Firstly, I thought about using C++11 to create something fast and efficient.
But chance to find any of C++ developers amongst artists and designers is much-much lower
then several ones with python knowledge to contribute their better ideas.
Of course this decision greatly affected the program architecture overall.


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

Bugs
----
 * For i3wm in dual monitor mode will create window _only_ on active monitor.
   Even if mouse is hovering on another monitor now.

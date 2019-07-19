#!/usr/bin/env bash
package_name=com.nonoapp

adb shell monkey -p $package_name \
                 --throttle 100 \
                 --pct-touch 20 \
                 --pct-motion 5 \
                 --pct-trackball 20 \
                 --pct-majornav 19 \
                 --pct-syskeys 1  \
                 --pct-nav 2 \
                 --pct-appswitch 32 \
                 --pct-anyevent 1 \
                 -v -v -v 50000 \
                 1> monkey.log  2>error.log

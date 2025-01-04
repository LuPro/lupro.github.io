---
title: My last 6 months in KDE/Plasma Mobile
description: Learning experiences all around
date: 2025-01-04T21:00:00
preview: Random updates from yours truly
tags:
    - KDE
    - Plasma Mobile
---

Uh. Has it really been almost half a year already? Whoops.

Unfortunately even with this many months I didn't get quite as much done in KDE-land as I hoped, for two main reasons:
- I've been bouncing back and forth between quite big tasks (for my current level of experience in the KDE stack), leading to a lot of time spent with few results. I've learned a lot, but there's not much to show for it yet.
- A good amount of time was taken by preparations for the 2024 European Rocketry Challenge (EuRoC) in Portugal - this was my second time there with the TU Wien Space Team and while it was an absolute blast, prepping a student-build bi-liquid propelled rocket for launch is on the more time consuming side of things. Who'd have thought! Maybe I'll write a dedicated post for this some time in the future, we'll see.

Back to KDE though: It wasn't all just learning - my phone also broke! Well. Kind of. Probably a loose contact in the SIM reader leading to it dropping connection to my SIM card a bit more often than I'd like.
However this did push me to put said SIM into my old OnePlus 6T which just so happened to be running postmarketOS edge making me an official Linux Mobile daily-driver.

And I'm happy to report it mostly just worked. Sure, there's a few apps I'd like to have that aren't available on Linux Mobile (yet?), but what's there works and it's enough for me to use it.

Though there are certainly a number of more-than-a-bit-annoying bugs to be ironed out - so iron them out I will. For now my SIM card is back in my spotty Android phone until I fix a bug which sometimes duplicates incoming calls making them continue ringing while you've already picked up (less than ideal), but after that I think I'll stay on my 6T with Plasma Mobile for a longer while.

Now before I write another novel, let's get to the stuff I did actually finish in the last few months.

# Merged Changes

## Mobile Taskswitcher

- Fixed an issue with the animation opening the taskswitcher from homescreen
- Fixed the icon list during task scrub mode sometimes being off center
- Reintroduced maximizing the selected window when not in docked mode. Technically it shouldn't be necessary since our KWin configuration should force windows to be fullscreen already, but some apps managed to break out of that (mostly GTK based apps), so back in it goes.
- Disable blue border on touch gestures in mobile environment - it's nice as an indicator for mouse based gestures, but unnecessary here.
- Add double tap on navbar task switcher button to switch between the 2 most recent apps.

## Misc

- Disabled session restore on mobile (at least until a bug with dialer launching ontop of login screen soft-locking the phone is fixed)
- This is not a change by me, but I wanted to mention it because it's great and I mentioned in my last post that I tried (and failed) working on that before: Micah Stanley did a marvelous job at new mobile friendly notifications!
- I've also done my first MR reviews which was exciting and a lot more work than I anticipated. At this point I want to thank all the people who have spent time on my MRs already!

# Unfinished

I still haven't managed to get back to my touch corner gesture MR for KWin due to all the stuff that came in between like:
- Fixing that the navigation gestures are still active while the navbar is enabled. Unfortunately this requires a change in how our setting system works and... CMake broke me here. I got pretty close to fixing this but had to leave it be for now for my own sanity's sake. I hope to get back to this soon since this is quite annoying.
- Improving plasma-dialer's lockscreen behavior. Right now with session restore it restores above the initial login screen on mobile essentially soft-locking the phone if it happened to be running when the phone was shut down. A similar thing happens when a call is received during the lockscreen - I'm currently figuring out how to best fix that.


Well, that's all from me now. Hopefully I manage to do the next post in a more timely manner, but we'll see for how long my current bigger ticket items will keep me occupied for.

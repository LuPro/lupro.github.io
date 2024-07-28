---
title: What I did in KDE/Plasma Mobile land in July-ish
description: Miscellaneous improvements
date: 2024-07-28
preview: Random updates from yours truly
tags:
    - KDE
    - Plasma Mobile
---

After my gargantuan post around the overhauled navigation gestures (and a still-in-progress one about KWin corner touch gesture support I'll hopefully have ready soon:tm:) let's tackle a few more smaller things. I'll try to make these somewhat regular (dare I say maybe even monthly?), but let's see how that shakes out, probably more like every 2-3 months if at all.

As an exciting update, near the end of June (the 25th to be exact) I got accepted to the KDE dev team. This means I now have the ability to properly manage submitted issues on GitLab and, only slightly terrifyingly, I'm now allowed to push code changes to the main repositories and review MRs. Let's see when, if ever, this feeling of trepidation over having to make quadruple sure I don't accidentally do stupid stuff subsides. Should it even subside or is being very extra super duper careful a good thing. I'll keep you posted whenever I find an answer to that :D

Anyways, let's get to code changes:

# Merged Changes

## Task Switcher/Gesture Navigation

- I sat down and overhauled some of the animations around the navigation gestures of the mobile task switcher: The diagonal quick switch should now look smoother and not be nearly-instantaneous and the flick to homescreen is now a tad smoother and actually makes the task preview smaller while animating instead of looking like it's opening the selected task before suddenly vanishing.
- Fixed minor logic bug around task switcher quick switch gesture. It should now correctly open the task switcher when you're trying to quick switch towards the end of a list - if there's nothing to quick switch to, it's better to open the full task switcher instead of just returning to the app you were in before.
- I added a task icon list to the task scrub gesture in the switcher to make it visually more distinct to the "normal" task switcher and provide more useful info about the open apps you can switch to. In case you didn't know: In gesture-only mode w (I'll admit this one is a bit older, but this is the first installment of this kind of post so I'm not tooooo strict on the "in July" part): ![](taskswitcher_scrub_icon_list.png) I'm still tracking an issue with this where when the task list becomes too long it's not properly centered anymore, but that should be a fairly simple fix once I get to it.
- The main task switcher opening gesture now stops tracking the finger 1:1 in the vertical direction once it's moved a bit past its "fully activated" point. This is a bit awkward to explain, but basically it makes it "more reluctant" to follow the finger infinitely far up. If that still doesn't make sense, here's a video: ![](taskswitcher_tracking_reluctance.mp4)
- The task switcher gestures now have a haptic feedback in some places: When the conditions are met for the task switcher to open (eg: gesture progress is far enough and finger movement speed is slow enough) and when the task scrub mode starts there'll now be a bit of haptic feedback.

## Misc

I've done some bug triaging and reproduction here and there, as well as tried to keep up to date on merge requests in the Plasma Mobile world. I still haven't really done a proper review and merge, but I'm trying to look through all of the other ones to hopefully learn how good reviews look like so at some point I'll be able to do them.

# Unfinished

- I tried my hand at fixing the task switcher navigation gestures being always active instead of just when the gesture navigation mode is actually turned on. To do this properly we probably need to refactor the `mobileshellsettings` plugin to be accessible via C++ (it's just a QML plugin currently), so let's see how that goes.
- I started work on more mobile friendly notification popups. The new design uses a swipe-to-dismiss interaction instead of having a close button. While technically "working" from a functionality perspective, the visuals are kind of broken still. I hope to have this complete by 6.2, but there's still some open questions. I'll probably have to get in touch with more experienced Plasma devs to brainstorm why this is going wrong so badly, but I've not quite given up at bashing my head against this myself. Oh and before I forget: this also affects Plasma Desktop when in Touch/Tablet Mode. ![This was my first try, which was smooth but left behind the window shadow](mobile_notifications_fail_1.mp4) ![And this my second try which is more technically correct and properly moves the window, but... I mean, you can see it yourself](mobile_notifications_fail_2.webm)

# Upcoming

For the next month I wanna try and finish up my work on KWin touch corner gestures (and get another oversized blog post out about those) and then implement them into Plasma Mobile. Once that is done I want to do more bug fixing, triaging and looking at knocking out some tickets for planned bigger picture improvements for 6.2. Let's see next month if a) I get any of this done or b) I even manage to make a blog post since I'll not be home for a while.

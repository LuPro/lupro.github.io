---
title: Search Postmortem Part 1
description: A deeper dive into TaleSpire's new search
date: 2026-07-29T18:01:00
preview: An introduction to our search & tag system and the challenges we had to solve
tags:
    - TaleSpire
    - Search
---

# Tags

So, what are tags and why do we need them? In short, tags are "some text" that describes a thing or properties of a thing. Usually that’s a single word, where in our case the "the thing" is minis^[0]. For example, a tag for a mini might be "human", and for a tile it could be "wood".

Technically, all of the information of tags could be contained in the name, but that would quickly become unwieldy - "Armed Dragonborn Warrior with Bow and Sword" or "Half-Elf Blacksmith" aren't great names.
These aren't good for a few reasons: Names get super long, search algorithms have a hard time actually finding things, and people tend not to always agree on how exactly to call things. The Half-Elf Blacksmith is especially interesting, but I’ll leave that for a future post.

Tags solve that.

# What does "solve" mean

No two people will always agree on how to name things, how to describe them, and especially not how to categorize them. No tag system will ever truly "solve" that problem, because there are no true correct answers.

We can, at best, make useful tools that allow most people to have a better experience than without them. So when I say "Tags solve that", what I really mean is "Tags solve some of the aforementioned problems to varying degrees of success and bring a bunch of their own issues and idiosyncrasies, but we’d on average be worse off without them."

# We cannot ship our memories

Unfortunately, there are many perfectly valid ways to tag things - there is no "objectively correct" way. For example: Let's pretend we want to learn about worms. First, we'll check the Wikipedia article on worms: "Worms are many different distantly related bilateral animals[...]".

Wait what.

We got half a sentence in, and suddenly worms are different, *distantly* related animals? And that sentence doesn't even let on just how distant "distantly" is, believe me, it's wild^[1].

But maybe we can at least be perfectly objective with tiles? Also, no, because all we can do in TaleSpire is look at things to describe them, we have no way of reliably distinguishing between brass and gold just by looking at it - and we don't even want to! A big part of building in TaleSpire is using and even more so "mis"using assets; It's not up to us (Bouncyrock) whether an asset is a telescope or a mortar tube, that's up to you (the players) when using them!

So if objective isn't an option, subjective tags it is - unfortunately, that means different people will have different ideas on how that should be done and we need to pick one way. But, as the section heading already said: we cannot ship our memories and knowledge about how our decisions for the tag system work. So we need some way for TaleSpire to (intuitively) show you all how our tags work, which ones we have, and when to use them.


How we tackled all that is what I'll get into the next part of this series, this one is already getting long enough.
See you then!




[0]: Everything is already set up for tiles and props to use the new tag system, but we have not finalized the actual list of new tags for them, which is a significant part of the work.

[1]: The only taxonomic classification^[2] that Nematodes (wormy-looking things that account for 80% of all living animals in the world) and Earthworms have in common is that they're animals. That's it. There's no more taxonomic common ground between the two. They are pretty much as distant from each other as they are from humans. (And yes, I know Nematode is a Phylum and Earthworm a Suborder, which is a whole different story that a biologist should get into, not a software developer) Of course, when all is said and done, we require words that adequately describe the visuals of assets, so the "worm" tag does in fact exist, and it is useful - this was only to illustrate the impossibility of being "factual and objective". Also, don't even get me started on fish.

[2]: I didn't want to use recursive footnotes, yet here we are. I want to add at this point, while we're talking about "objective" classifiers, that as much as taxonomy is rooted in verifiable science, it is also still a bunch of subjective, human-made words trying to classify the unclassifiable reality into more-or-less neat boxes, because that’s what our human brains have evolved to prefer. In the end, as much as taxonomy is a science (and it is!), it is also an imprecise, subjective tool for humans to try to wrap their brains around the impossible complexity of life. Also, it often isn't all that useful for classifying things "based on looks" which we need for TaleSpire, as we've long since moved away from "look based taxonomy" like that.

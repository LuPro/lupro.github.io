---
title: Search Postmortem Part 5
description: A deeper dive into TaleSpire's new search
date: 2026-10-14T16:28:00
preview: Random anecdotes about all the headaches search brought us
tags:
    - TaleSpire
    - Search
---

Hi!

This is the fifth and final part of the deep(er) dive into the new tag and search system 

Instead of "engineering" problems, in this devlog, I want to get into a few examples of why the heck all of this took so long. The actual "writing code" part of this journey was (while substantial) not the real issue. Most of the time was spent sitting and brooding about which tags to include, how to relate them to each other, and going back and forth on decisions for many valid reasons.

So, to share some of our struggles, I'm just going to illuminate a few of the oddities and tricky decisions we encountered along the way. But do know: Those are by far not the only ones.

# Cats and Dogs

We really wanted to keep tags reasonably consistent across the board and decided early on that we won't have tags for every single possible species - we just couldn't possibly have a tag for every single animal, real and fantastical. This (and a few other) considerations led to the concept of searching for asset names: if we don't have tags for mouse, weasel, lemur, rabbit, ... we still need a way to find those animals, so we added asset-name search.

However, while we don't have a "Black-footed Ferret" asset, we only have a "Ferret"; we *do* have a "German Shepherd" instead of just "Dog" - the nature of our relationship with our beloved furry companions makes us care more about the smaller details and differences. So try as we might, we can't just have "canine" as the only tag for dogs, the same way we only have "mustelid" for ferrets and weasels, even if that would be "more consistent". No problem, let's just add the dog and cat tag.

But there's another problem. In part 3, I talked about one goal of the new tag system we aimed for: tag sets being somewhat consistent across different people tagging the same mini. For dogs, this was fine: A Labrador is tagged dog, a Gray Wolf is tagged wolf.
But what about cats? Sure, a Maine Coone gets the "cat" tag, no problem - but what about a Lion? Leopard? Lynx? Many people consider these felines to be "big cats"^[0], so it's not unlikely they'd also use the "cat" tag for those. Once even just a few do that, there’s no consistent way to distinguish between a cuddly Siamese cat and a decidedly less cuddly tiger.
To solve this, we got rid of the "cat" tag and instead made it an example_of relation pointing to "feline"^[1].

# Art Style and Games

Another frequent cause of trouble is the freedom assets can be used in and how "interpretable" our art style is: There's nothing visually distinguishable between an elf and a half-elf. Both look vaguely human with pointy ears (even worse if they're wearing something with a hood!), but that's about it^[2]. A similar story for demons and half-demons. For these "half" tags, we mostly rely on tag relations solving inconsistency, so all of those are findable under "elf", "demon", ... and if the artist making the asset feels like "but that is actually a half-something for real!" they can additionally tag them as said half-something.

A more interesting problem is tagging assets that are entirely up to interpretation. This happens less with creatures, but we also started working on tags for tiles and props, which encountered this a lot: For example, who's to say whether a white/yellow-ish grainy substance in a sack of grains is actually grains? It could just as well be sand, flour, small pebbles, or some futuristic composite material.

Job tags had similar problems - we want them so you can easily find a blacksmith to put in your smithy or a scientist for your evil corporation laboratory. But we noticed that, especially in modern and sci-fi settings, people who do a certain job don't really "look" like that job. An accountant has no special features to distinguish them from any other office worker - this is less of an issue for more "physical" jobs (eg: a blacksmith carrying a hammer and wearing heavy duty apron and gloves), but even then, if a barkeep doesn't happen to carry a glass but instead just a towel for cleaning the bar it might as well be a janitor.

So which ones are visually distinct and important enough to add, and which ones aren't?

# Not everyone is a biologist

While we ended up with a fairly in-depth taxonomic tree, getting there was challenging: first, how do made-up fantasy creatures fit into real-world taxonomy, and second, not everyone is a biologist.

Let's look at the latter some more. While we could reasonably assume that most people know what canine and feline mean, the same isn't true for mustelid (eg: weasels, ferrets, badgers), cetacean (eg: whales, dolphins), or whatever the fresh hell "procyonidae" (eg: raccoons) are. However, to find relevant stand-ins^[3] we do need these grouping tags. It was incredibly difficult to draw the line between "this is too obscure (looking at you, procyonidae)" and "this is reasonable (equine, bovine, mustelid, ...)". But even those "reasonable" ones still need to be learnable and discoverable for people who don't know them.

In some cases, we could also use the more commonly known word instead of the "scientifically correct" one: For example, as far as "animals that most people can name and care about in a TTRPG" go, Procyonidae pretty much only contain raccoons, so we skipped this horrible word and just added a "raccoon" tag instead. Similarly, for bears, we could have added "ursine"^[4], but all the ursines we care about are just "something bear", so we went with just adding a "bear" tag instead.

# Synonym Kinds

While fleshing out the tag list we came across another language oddity - not only do different terms for the same thing exist, but also the same term can have different (mutually exclusive) meanings depending on context. For example, a "dragonfolk" person will always be well described by "dragon" and "humanoid" - however "exoskeleton" can relate to insects, or robots/mechs with people inside, but crucially not both at the same time.
This difference between some synonyms that point to more than one tag implying all of those tags and some implying only one of those made them incompatible with each other with regards to the search UI tooling. Luckily, all of the cases we encountered where only one of the pointed tags could be true at a time were quite niche and unimportant terms, so for the time being we just removed them instead of having to work around (and intuitively show) this difference for just two very rare uses.

# Ordering

Tag relations make it easy to group tags and synonyms together while keeping duplicates in check, but what remained tricky was choosing which one becomes the "main" one - should fighter point to warrior or warrior to fighter? Turtles and tortoises are different, but not really (visually) different enough to warrant two separate tags. But which of the two should we keep and which should only be a "synonym" of the other?
This was a frequent source of discussion, followed by researching word usage frequency and definitions, followed by discussion, followed by...

# Ambiguity

Originally, we intended for minis to be categorized between "Alive", "Undead", and "Animated", where the latter would be some sort of made-to-move-through-magic-or-technology - so things like golems, floating armors, and robots.
But we quickly realized that whether a floating armor is magically floating (enchanted), or possessed by a ghost (undead), and whether undead is even different from animated or still counts as "magic" or not, was extremely subjective and depended on the particular world and setting you looked at.
However, we still wanted to be able to search for undead as enemies, while also having the distinction to be able to populate an evil wizard tower with appropriate magical workers/guards.
In the end, we went for Alive/Undead/Enchanted, where "Alive" is the "default assumption" (any mini that's not undead or enchanted), "Undead" is the default "fuzzy" definition of undead, so your typical zombies, ghouls, skeletons, and company, while "Enchanted" refers to inanimate objects that were compelled to move by magic. The "robot" use case is handled separately through the "machine" tag instead.

And with this we have reached the end of this deep dive series into (some parts of) the new search and tag system! I hope you've enjoyed this slightly different kind of devlog, but now it's back to coding for me. See you in the next log!

[0]: I'm a bit annoyed at that term in English - while German does also have "Großkatze" (which literally translates to "big cat"), we also have "Raubkatze" which roughly translates to something akin to "cat of prey" (like bird of prey), or more literally "Preying Cat" which - in my opinion - does a better job at distinguishing domesticated/"pet" cats from wild cats (and especially the big ones), even though I know our fuzzy little house friends are also vicious hunters in their own right.

[1]: We also added a "house cat" example_of which points to both feline and domestic to be able to find specifically just pet cats quicker.

[2]: I've already touched on this a bit in part 2 about tag relations - it might of course be that there is a more pronounced visual difference in whatever fantasy world you are playing in, but since TaleSpire strives to be as system- and world-agnostic as reasonably possible, we can't really account for that. In most worlds, the differences are minor to non-existent, especially with our "zoomed out miniature" style.

[3]: "Stand-ins" as in, "Oh, I wanted to have a hawk, but that asset doesn't exist, let's instead see birds for the next best/closest thing".

[4]: *Technically* Ursid or Ursidae, "ursine" is the accompanying adjective roughly meaning "resembling an Ursidae (bear)". The same goes for Canidae, Felidae, ... but in normal language use, the terms are often used interchangeably, and from what we could gather, the -ne adjectives were more common.

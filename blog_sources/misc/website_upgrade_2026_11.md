---
title: Webdev without JS
description: Making a website without JS in 2026? In this economy?
date: 2026-11-06T20:35:00
preview: I'll ramble a bit about my trial and tribulations upgrading this website
tags:
    - Misc
---

While finishing up my last round of improvements on this here website I thought it might be interesting enough to warrant a blog post.

I've recently had a bit of inspiration looking at some other smaller blogs and personal websites that were more in the style of the "olden web" with more playful and... "maximalist" designs for the lack of a better term.
While I didn't want to go all that way into early 2000s web design, I did want to copy some of that playfulness and character and try and combine it somewhat with the modern minimalist aesthetic. The result of that is the still quite boring, but a *touch* more playful [projects](/static/html/projects.html) page - I do wanna tweak the default style to have a bit more character (more like, any character at all), but I am quite happy about how the style switching has turned out when going to the individual sections and some of the flourishes in those.

What I am not happy about is the actual implementation though, and I want to talk about that. That page in particular, but the whole website really is built with as little JavaScript as possible - as of right now "as little as possible" means none.
I don't actually have something against JS per se and I'm quite confident using it due to my work on the [Mission Control web interface](https://github.com/SpaceTeam/web_ecui_houbolt) for the TU Wien Space Team's [bi-liquid rockets](/static/html/projects/tust_liquids.html), but I like the idea of keeping this website small and lightweight and I kind of wanted to challenge myself how far I could go with just using HTML and CSS^[0].

# Not far it seems

When I imagined what such a project page could look like I immediately envisioned something like a conversation selection you would find in a CRPG with a handful of "conversation options" that lead to some response^[1] - so the requirements are clear: A list of options and a container next to (or under) those that shows some more info depending on the selected item.

But, how the hell do I do this without JS? Using just HTML and CSS it's not that easy to make something conditionally appear or disappear.

# Or is it?

CSS selectors have gotten quite powerful over the years, so it ended up not actually being that hard:

```
#container:has(button.one:focus) #one-content
```

Using this handy selector^[2] I could apply a style to the content container of a given button with said button has focus. Now the default style just need to move it out of the way and make it invisible, while the focus style undoes that and we're off to the races.

# Keeping focus

However, this doesn't work if you have more stuff to interact with inside that content, since as soon as the main "selection button" loses focus, the content disappears. That is luckily also fixed quite quickly by adding the following:

```
#container:has(button.one:focus, #one-content:focus-within) #one-content
```

This isn't *perfect*, since this will only work when you click on something that is actually focusable, so clicking on random text would still hide the content, but this is good enough for what I need it for, at least for now.

# Keyboard Navigation

Initially I was quite happy with the styling which hides the unfocused content. It was just `translate`ing the containers off-screen - which looked quite smart when animating in and out.
However, I do try to keep everything I do as accessible as possible, so I tested keyboard navigation by tabbing through and oh boy did things fall apart. Turns out when you move things off screen and set opacity to 0, but don't `display: none` it, the browser will still happily scroll to it while tabbing - even if overflow is disabled.

Well, no biggie, instead of moving it off screen, move it only slightly and scale it, this gives almost the same effect while keeping all elements on screen^[3].

# Apple

With all that solved I had a nicely working projects page that - after a decent chunk of work - even looked and behaved well on mobile! All was good and everyone lived happily ever after, that is, until I wanted to show my new projects page to my brother on his iPhone.

## :focus

Now, I don't want to entirely shit on Apple here, I kind of understand some of their reasoning behind this, but: Safari, both on macOS and iOS, does not give out :focus so willy-nilly. Importantly, they don't give focus on click of a button (apparently only text inputs get focused with a click?). Now, if we recall the sections from above, I kind of require focus on my elements for my trick to make this kind of site work without JS.

And here's where I became unhappy with the implementation: I couldn't find a way to do it. I had to settle. I had to use JS.

It is almost nothing, just a single `onclick="focus()"` on each input element so Safari actually focuses the damn thing, but technically it is now not a JS free website anymore.
However, it will still work perfectly on all browsers but Safari without JS, since that `focus()` call is redundant on them, so I say it's close enough - especially considering I don't have an Apple device accessible to test on, so I can't really do proper development iterations.

## :focus 2 Electric Boogaloo

But this is not the end of the story, because Apple, in their infinite wisdom is even stingier with allowing :focus - apparently, they don't allow it at all for `a` elements, which makes links impossible to click when they're in the content containers since they make the main button lose focus which immediately hides the content.

So I had to add the most awful of hacks and put a button (which is focusable) inside of the `a` tag just so Safari would finally be happy.

# Wrapping up

Knowing what I know now, would I recommend doing this to someone else? I'm not sure, I enjoyed it and the end result is nice enough, but I would be lying if I said it didn't take significantly longer than just using even small amounts of JS.
Also, since I had to do a lot more esoteric CSS work it's probably not as maintainable and definitely not as easily extendible with new content as a few lines of straightforward JS are, but to hell with it, I still like it!

And that's where I'll leave it be for now, thanks for reading and until the next one!

[0]: Part of that mindset was also inspired by the insanity that is [CSS Clicker](https://lyra.horse/css-clicker/). I still have not the slightest clue how such a thing is even remotely possible.

[1]: The design didn't end up going that way, but it might still in the future. I wanted to get the content and basic setup done and out first before I spend days tweaking a design I might not end up liking.

[2]: For brevity's sake I've renamed the IDs since the real ones are a decent bit longer.

[3]: Just keep in mind to also set the z-index of the currently active element to be higher than the hidden stuff, otherwise you can't interace with it. Oops.

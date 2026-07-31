---
id: shell/packages
title: Packages
part: Software
section: Packages
order: 2
summary: Every app is a bundle of code, most of that code is free, and the shell is how you reach it
keywords: [package, open source, install, homebrew, pandoc, tesseract, git, diff, licence]
---

# Packages

*v0.2.0*

A **package** is a small, self-contained piece of code that does one
job and can be dropped into anything that needs that job done. The last
article's wrapper is built out of them.

## Most packages are free

Not free as in a trial. Free as in published, openly licensed, and
maintained in the open by the people who needed it to exist. The same
libraries sit underneath commercial products and free ones.

This is not a fringe world. The tool that reads text out of scanned
pages was built at HP and is now maintained by Google. The tool that
converts between document formats was written by a professor of
philosophy and is used by publishers. These are not cut-price
imitations of paid apps — they are frequently the thing the paid app is
wrapped around.

## The shell is how you reach them

A package has no window and no icon, so a mouse cannot find it. That is
the whole reason this world stays invisible to most people, and the
whole reason a shell changes what is available to you.

One line installs one:

```
brew install pandoc
```

That is the shape of it. No account, no download page, no licence key,
no salesperson. And once installed, the package is a command like any
other — so it composes with everything else you have seen, and Claude
Code can drive it for you.

## What that replaces, in this line of work

| Instead of | The package |
|---|---|
| Word tracked changes | `diff`, `git diff` |
| Drive version history | `git` |
| Acrobat text extraction | `tesseract`, `pdftotext` |
| Acrobat merge and split | `qpdf`, `pdftk` |
| Converting to Word or PDF | `pandoc` |
| Renaming exhibits in bulk | the shell itself |
| Searching a folder at once | `ripgrep`, `grep` |
| Making scans searchable | `ocrmypdf` |
| Shrinking a PDF to email | `ghostscript` |
| Stripping file metadata | `exiftool` |

The first row is the one worth pausing on. `diff` compares two
documents and shows exactly what moved, and it does it between any two
files, in any format, without either party having to have had tracking
switched on. It predates Word by a decade.

The second is nearly as good. `git` keeps every version of every file,
with a note on why it changed, and can show you any two of them side by
side — for a folder of drafts, not only one document. It gets a section
of its own later in the course.

> None of this asks you to abandon what you use. It changes what you
> reach for when the paid tool cannot do the thing: three hundred
> scanned exhibits to make searchable, a hundred filenames to
> normalise, two versions of an agreement from opposing counsel who did
> not track changes.

## Where this is going

You are one sentence away from all of it. The reason to know packages
exist is that you can now ask for the outcome — *"pull the text out of
these scans"* — and let Claude Code pick the package, install it, and
run it.

It cannot do that from nowhere, though. Something has to find the
package, fetch it, and keep it working when its dependencies change.
That something is next.

Press `n`.

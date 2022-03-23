# agregore-mobile
Mobile version of the Agregore browser for Android, based on Chromium and Bromite

**WORK IN PROGRESS**

## Development

This codebase is based on [Chromium Android](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/android_build_instructions.md) and [Bromite](https://github.com/bromite/bromite).

How it works:

- You'll need 40 or 50 GB of space on your machine since chromium is so huge.
- Run `./setup.py` to do the initial folder setup.
  - The build scripts use Python 3, so you'll need to have it installed on your system.
	- Chromium build tools are set up in `./depot_tools`
	- A Chromium source tree is set up in `./chromium` (this takes huge amounts of space)
	- A `Bromite` source tree is set up in `./bromite` (this doesn't take much space)
- Run `./patch_with_bromite.py` to checkout the correct version of Chromium and to apply the bromite patches to it
  - Run this whenever bromite gets updated
- TODO: Run `./patch_with_agregore.py` to apply Agregore patches to the Chromium tree
- Run `./prebuild.py` to sync dependencies needed to perform a build.
	- This can be skipped if you're just adding changes, dependenices can take an extra 30 GB of space
- Run `./build.py` to trigger a new build of the browser
  - You'll need to be running Ubuntu 18 in order to do a successful build.
  Automated builds via a [build server](https://build.mauve.moe) are a work in progress.
- The `patches` folder contains Agregore-specific patches on top of Chromium
- TODO: Run `./gen-patch.py` To generate a new patch based on the latest Commit inside `Chromium/src`
	- Then you'll want to commit the patches and use `apply_agregore_patches.py` to apply them on the build server

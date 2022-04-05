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
  - Run this whenever bromite gets updated, it will auto-run at setup
- Run `./apply_agregore_patches.py` to apply Agregore patches to the Chromium tree
  - Run this whenever there are new Agregore patches to apply. It will auto-run at setup
- Run `./prebuild.py` to sync dependencies needed to perform a build.
	- This can be skipped if you're just adding changes, dependenices can take an extra 30 GB of space
- Run `./build.py` to trigger a new build of the browser
  - You'll need to be running Ubuntu 18 in order to do a successful build.
  Automated builds via a [build server](https://build.mauve.moe) are a work in progress.
- The `patches` folder contains Agregore-specific patches on top of Chromium
- Run `./generate_patch.py` To generate a new patch based on the latest Commit inside `Chromium/src`
	- You can specify `--n` for the number of commits to include in the patch if you want something other than the latest one.
	- Generally, if you did several commits as part of your change, you'll want to squash them with `git rebase -i HEAD~<n>` where `n` is the number of commits you want to squash.
	- Then you'll want to commit the patches and use `apply_agregore_patches.py` to apply them on the build server

### Flow for making patches

- Checkout a new branch for your patch
- Make changes in `chromium/src`
- `git add -A` to track newly added files
- `git commit -am "some message"` to commit your changes
	- For the message, try to start with `AG ` since this will be the patch name
- `cd ../../` back to the root of agregore-mobile
- `./generate_patch.py` to generate a new patch
- `git add -A` to track the new patch
- `git commit -am "Added patch for bla bla bla"` to commit your patch to the main repo
- `git push`

### Adding changes to an existing patch

- Make your changes in `chromium/src`
- (If you have new or deleted files) `git add -A` to track the new files or remove deleted ones.
- `git commit -am "some message"` to commit your changes
	- Note the message doesn't matter because we'll be deleting it in favor of the message in the patch
- `git rebase HEAD~2` to start rebasing the commit history (with the goal of sqashing your previous commit into your patch commit)
	- Note `2` means "the latest commit, and the one before that", if you have more commits that you want to squash, increase this number
- When your editor opens, Squash all the commits other than the one for the patch (which should be left as "pick")
- Then once it prompts you to edit the new commit message, delete the squashed commit messages and just keep the original message
- Now your history should have the latest commit
- `cd ../../` to go back to the agregore-mobile directory
- `./generate_patch.py` to re-generate the patch content
- `git commit -am "the actual commit message for you change"` to commit changes to your patch
- `git push` to push the latest version of your patch out

### Applying new versions of a patch

- `git pull` to get the latest chnages
- `./undo_last_patch.py` to undo the latest version of the patch
- `./apply_agregore_patches.py` to re-apply the latest versions of the patches.

### Flow for building with the build server

- Checkout a new branch to start
- Make changes inside chromium/src and commit
- Run `./generate_patch.py` to generate a pach
- Commit your changes to your branch
- Push them to github
- Checkout the branch on the build server `ssh root@build.mauve.moe`
- Apply the patches using `./apply_agregore_patches.py`
- Run `./build.py`

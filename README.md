# My local functions

Here are a list of functions and programs that I have made, that are not available to the general public (mostly just because I am to lazy to set up the repos in pip etc).

I plan to make several functions here and you may or may not want all of them.
For those that want them all, the `install.sh` script should work.
Otherwise you can follow the example below for how to install individual functions.

## Installing Individual Functions/Packages

First up you need to update your path, so you can run the functions regardless of where you are on your computer.
Below are a few commands to make a `~/.local/bin` folder and add that to your `PATH` for the current session as well as adding it to your `~/.zshrc` file so that it permanently gets added to your path.
Bash users should change `~/.zshrc` to `~/.bashrc`.

```bash
mkdir ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

Next, you will need to move over the relevant functions into your `~/.local/bin/` folder.
This can be done with `mv` or preferrably a symbolic link, that way you can have access to any updates I make in the future.
Below is an an example of using a symbolic link.

```bash
ln -s ~/git_repos/local_functions/shell/change_wallpaper.sh ~/.local/bin
```

Alternatively, for python packages specifically, they can be installed through `pip`.
Below is the basic structure for installing a package.
(Note, you still need to update your path for python packages as well).

```bash
python -m pip install -e PACKAGENAME
```


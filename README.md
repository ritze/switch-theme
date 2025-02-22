# switch-theme

Set the themes for generic applications and frameworks.


## Config

Themes and the way how the themes are changed are defined in the config file
`~/.config/switch-theme/switch-theme.toml`.
There are three major categories:
1. Aliases
2. Themes
3. Apps

An example can be found in `example/switch-theme.toml`.


### Aliases

It's possible to set an alias to a specific theme. E.g. this can be used to
define the standard dark and light theme:

```
[aliases]
light        = "onehalf-light"
dark         = "ayu-dark"
dimmed-dark  = "onehalf-dark"
```

### Themes

A theme defines the theme name used for each application:

```
[themes.onehalf-dark]
fallback  = "dark"
alacritty = "onehalf-dark"
bat       = "OneHalfDark"
gtk       = "Adwaita-dark"
```

In the example there are three applications defined, which behavior is defined
under
* `[apps.alacritty]`
* `[apps.bat]`
* `[apps.gtk]`

A special option is `fallback`, which references to another theme. In the
example the fallback theme is defined under `themes.dark`. The `fallback` option
is not recursive and only followed once.

A theme together with its fallback must define themes for all applications
defined.


### Apps

For each application there are two different modi:
* Search and replace
* Executing a command

#### Search and replace

The script will replace the value of `pattern` with the value of `replace` in
the file defined under `file`. Thereby `{}` of the field `replace` will be
replaced by the string defined under the theme.

```
[apps.bat]
file    = "~/.config/fish/functions/bat.fish"
pattern = ' --theme=.* '
replace = ' --theme="{}" '
```

If switching the theme to *onehalf-dark* the pattern ` --theme=.* ` is replaced
in `~/.config/fish/functions/bat.fish` will be replaced with
`--theme="OneHalfDark"`.


#### Command

A command will execute the provided string with the theme name appended.

```
[apps.gtk]
command = "gsettings set org.gnome.desktop.interface gtk-theme"
```

If switching the theme to *onehalf-dark* the command
`gsettings set org.gnome.desktop.interface gtk-theme Adwaita-dark` is executed.


## State files

For each application the set theme will be written into a state file while the
file has the application name.

The state directory is `$XDG_STATE_HOME/switch-theme`. If the environment
variable `XDG_STATE_HOME`` is not set, the default path `$HOME/.local/state`
for `XDG_STATE_HOME` will be used.

For example if switching the theme *onehalf-dark* and the application bat is
configured with

```
[themes.onehalf-dark]
bat       = "OneHalfDark"
```

the file `$XDG_STATE_HOME/switch-theme/bat` will be overwritten with the text
`OneHalfDark`.


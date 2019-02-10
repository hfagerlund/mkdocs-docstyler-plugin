# mkdocs-docstyler-plugin

**docstyler** is a plugin for [MkDocs](https://github.com/mkdocs/mkdocs/) that enables users to add (persistent, preferred and/or alternate) external stylesheets to custom themes using the `mkdocs.yml` configuration file. ([Why 'docstyler' instead of 'extra_css'?](https://github.com/hfagerlund/mkdocs-docstyler-plugin#which-config-to-use-docstyler-or-extra_css))

## Requirements

* [Python](https://www.python.org/) >= v3.6.4
* [MkDocs](https://github.com/mkdocs/mkdocs/) >= v1.0.4
* a [**custom/third-party** MkDocs theme](https://www.mkdocs.org/user-guide/styling-your-docs/#using-the-theme-custom_dir):
  * [docSkimmer](https://github.com/hfagerlund/mkdocs-docskimmer) (**recommended**)

> **Note:** This plugin does **not** work for [built-in themes](https://www.mkdocs.org/user-guide/styling-your-docs/#built-in-themes) (ie. `mkdocs` and `readthedocs`).

## Quick Start
### Installation

* Manually:

```
$ git clone https://github.com/hfagerlund/mkdocs-docstyler-plugin.git
$ cd mkdocs-docstyler-plugin
$ python3 ./setup.py install
```

(Not on PyPi yet.)

* Add `docstyler` to `mkdocs.yml` and set its [configuration options](https://github.com/hfagerlund/mkdocs-docstyler-plugin#configuration).
* Add custom `.css` files to the `docs` directory (or in a subdirectory under `/docs`).

* Build and preview the site:
```
$ mkdocs build --clean
$ mkdocs serve
```
- - -
## Features
### Which config to use: 'docstyler' or 'extra_css'?

Although `extra_css` and `docstyler` **can both be used together** in `mkdocs.yml`, there are some important [differences](https://github.com/hfagerlund/mkdocs-docstyler-plugin#differences).

> **Note**: If both config options are combined, (persistent) stylesheets added using `docstyler` can be used to **override** stylesheets added in the `extra_css` section of `mkdocs.yml`.

### Differences
* Stylesheet types
  * `extra_css` adds only **persistent** stylesheet links.
  * `docstyler` enables the addition of three types of external stylesheet links: **persistent, preferred and/or alternate**.

* Theme types
  * `extra_css` can be used with [built-in themes](https://www.mkdocs.org/user-guide/styling-your-docs/#built-in-themes) or [custom/third-party themes](https://www.mkdocs.org/user-guide/styling-your-docs/#using-the-theme-custom_dir).
  * `docstyler` is only compatible with [custom/third-party themes](https://www.mkdocs.org/user-guide/styling-your-docs/#using-the-theme-custom_dir).

### Similarities
* Custom `.css` files should be placed in the `docs` directory (or in a subdirectory under `/docs`) when using either `extra_css` or `docstyler`.

### Additional Features
* docstyler also enables customization of stylesheet `<link>` elements with (multiple) **media types**.
- - -
## Configuration

### Example:
```yaml
# excerpt from mkdocs.yml:

plugins:
  - search
  - docstyler:
      alternate_styles:
        - path: reverse-contrast.css # file in /docs dir
          title_attr: Reverse contrast
        - path: ./custom_css/large-text.css # file in /docs/custom_css subdir
          media_attr: screen # optional
          title_attr: Large text # displayed in browsers that support 'View' > 'Page Style' menu or equivalent

      persistent_styles: # do not add 'title_attr'
        - path: base.css
          media_attr: all # optional

      preferred_styles:
        # stylesheets with same 'title_attr' are combined (by the browser)
        - {path: 'custom-theme-base.css', media_attr: 'screen', title_attr: 'Theme styles'}
        - {path: 'custom-theme-menus.css', media_attr: 'screen', title_attr: 'Theme styles'}

        - path: ./custom_css/custom-basic.css
          media_attr: all # optional; single media type
          title_attr: Universal (custom)

        - path: mobile.css
          title_attr: Mobile styles
          media_attr: 'screen and (max-width: 600px)' # media query (single or double quotes required)

        - path: ./custom_css/custom-style.css
          media_attr: print, screen # list
          title_attr: Printable
```

**Note:** 'search' must be added under the `plugins` section of `mkdocs.yml` in order to [enable it for use with other plugins](https://www.mkdocs.org/user-guide/configuration/#plugins) including docstyler.

### Result:
Automatically adds the following to the output of the theme's **'styles' block**:

```html
<link href="base.css" rel="stylesheet" media="all">
<link href="custom-theme-base.css" title="Theme styles" rel="stylesheet" media="screen">
<link href="custom-theme-menus.css" title="Theme styles" rel="stylesheet" media="screen">
<link href="./custom_css/custom-basic.css" title="Universal (custom)" rel="stylesheet" media="all">
<link href="mobile.css" title="Mobile styles" rel="stylesheet" media="screen and (max-width: 600px)">
<link href="./custom_css/custom-style.css" title="Printable" rel="stylesheet" media="print, screen">
<link href="reverse-contrast.css" title="Reverse contrast" rel="alternate stylesheet">
<link href="./custom_css/large-text.css" title="Large text" rel="alternate stylesheet" media="screen">
```
> **Note**: Other existing styles in `{% block styles %}` not added using docstyler are **preserved** (not overwritten or modified).

- - -
## Changelog
* v0.1.0 (2019-02-10) - Initial release.

> **Note**:
> * Dates shown in YYYY-MM-DD format 
> * Versioning using [SemVer](http://semver.org/)
- - -
## License
Copyright (c) 2019 Heini Fagerlund. Licensed under the [BSD-3-Clause license](https://github.com/hfagerlund/mkdocs-docstyler-plugin/blob/master/LICENSE).

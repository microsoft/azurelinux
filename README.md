# Structure

This website is based on the [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme, which is released under the MIT license. This theme is implemented as a remote theme for ease of maintenance. For significant changes, please consult their documentation.

## Usage

To run a local copy of the website before publishing, please use the included docker compose file. This will allow you to test and validate your changes before pushing them to the git repository.

### Starting the container

From the commandline `docker compose up` will build the website and launch a small webserver from which to view it locally at `http://0.0.0.0:4000/CBL-Mariner`.

### Stopping the container

From the commandline, use `ctrl-c` to exit the process, and run `docker compose stop` to tear down the containers.

## Pages and Blog post

If you add a page or blog post, please create them in the _posts or _pages directories, named appropriately. 
appropriate header material is required for files. example header data is below:

```
---
layout: single
header:
  overlay_image: /assets/images/conor-sexton-hRemch0ZDwI-unsplash.jpg
title: your page title here
---
```
If you wish to add an author profile to either a page or a blog post, please add an entry to `_data/authors.yml` and include a profile picture in `assets/images/profile/` Once that is complete you can add a line to the header material of the page referencing the author entry. It should look similar to the example below

```
---
layout: single
author: jperrin
header:
  overlay_image: /assets/images/conor-sexton-hRemch0ZDwI-unsplash.jpg
title: your page title here
---
```
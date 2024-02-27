# Mariner Image Customizer API

The Mariner image customizer (imgcustomizer) will be released as a standalone tool and
will provide strong backwards compatibility guarantees (after the first official
release).
This is contrast to the Mariner toolkit's new image config, which isn't officially
released and doesn't provide any backwards compatibility guarantees.

While currently the new image config and imgcustomizer config are very similar, in the
future there is the possibility they will diverge.

## Known differences

- For the new image config, `AdditionalFiles`' source files are relative to the working
  directory.
  Whereas, for imgcustomizer, the source files are relative to the config file.

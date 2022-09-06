# Contribution Guidelines

## Data contribution

The primary way to store the content of this project is on the [data/](data/) folder.
This means that if you want to propose new or an edit **for content**,
very likely the edit will be on that folder.

## Language localization contribution

The translations are stored at [i18n/](i18n/).

## Code internals contribution

1. Give a look at our code. It mostly python, bash script and GitHub Action.
2. We use Shopify Liquid template engine (same features as GitHub pages with Jekyll)
   with common documentation at https://shopify.github.io/liquid/.
   1. The _specific_ implementation is python-liquid maintaned coordinated by @jg-rp.
      Check <https://jg-rp.github.io/liquid/>. `python -m pip install python-liquid`
   2. We also use some extra filters `python -m pip install -U python-liquid-extra`

## Other non techincal aspects

### Code of Conduct
Please note that this project is released with a [Contributor Code of Conduct](.github/CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.

## License
By contributing to this project you agree that all contributions for this project,
both code and data, are explicitly public domain dedication as far as laws allow it.

> TL;DR: **Unlicense** and **BSD0** are good examples of public domain for code.
> But for content, **CC0** mostly explicitly does not grant rights to trademarks.
> As rule of thumb,
> "public domain" does not allow to impersonate the the creators of the resources cited on the list,
> but it does allow derived works of this project itself both for different
> proposes or (if someone thinks we're not fair with our curation of items)
> create a fork of the project to replace us.


<!--
@TODO maybe comment these
      - Testing https://github.com/panoply/vscode-liquid
-->
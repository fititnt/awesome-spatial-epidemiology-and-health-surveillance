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
> @TODO explain a bit more
-->


<!--
## Adding an awesome list

Please ensure your pull request adheres to the [list guidelines](pull_request_template.md).

## Creating your own awesome list

To create your own list, check out the [instructions](create-list.md).

## Adding something to an awesome list

If you have something awesome to contribute to an awesome list, this is how you do it.

You'll need a [GitHub account](https://github.com/join)!

1. Access the awesome list's GitHub page. For example: https://github.com/sindresorhus/awesome
2. Click on the `readme.md` file: ![Step 2 Click on Readme.md](https://cloud.githubusercontent.com/assets/170270/9402920/53a7e3ea-480c-11e5-9d81-aecf64be55eb.png)
3. Now click on the edit icon. ![Step 3 - Click on Edit](https://cloud.githubusercontent.com/assets/170270/9402927/6506af22-480c-11e5-8c18-7ea823530099.png)
4. You can start editing the text of the file in the in-browser editor. Make sure you follow guidelines above. You can use [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown/). ![Step 4 - Edit the file](https://cloud.githubusercontent.com/assets/170270/9402932/7301c3a0-480c-11e5-81f5-7e343b71674f.png)
5. Say why you're proposing the changes, and then click on "Propose file change". ![Step 5 - Propose Changes](https://cloud.githubusercontent.com/assets/170270/9402937/7dd0652a-480c-11e5-9138-bd14244593d5.png)
6. Submit the [pull request](https://help.github.com/articles/using-pull-requests/)!

## Updating your Pull Request

Sometimes, a maintainer of an awesome list will ask you to edit your Pull Request before it is included. This is normally due to spelling errors or because your PR didn't match the awesome-* list guidelines.

[Here](https://github.com/RichardLitt/knowledge/blob/master/github/amending-a-commit-guide.md) is a write up on how to change a Pull Request, and the different ways you can do that.

-->
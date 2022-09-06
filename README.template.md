# {{ 'project_title' | t }}
[![Frictionless](https://github.com/fititnt/awesome-spatial-epidemiology-and-public-health-surveillance/actions/workflows/frictionless.yml/badge.svg)](https://repository.frictionlessdata.io/pages/dashboard.html?user=fititnt&repo=awesome-spatial-epidemiology-and-public-health-surveillance&flow=frictionless)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

<!--
![{{ 'project_title' | t }} Banner](partials/awesome-spatial-epidemiology.jpg)
-->

**{{ 'project_summary' | t }}**


## {{ 'section_github_topics_title' | t }}
> **Resoning behind 3 tiers**: Tier 1 is directly related to main topic of our list of recommendations.
> Tier 2 is is related to the scientific area (but not strictly the tooling).
> Tier 3 are related to the tooling (but not restricted to the scientific application).

- **Tier 1**:
{% include_relative partials/github-topics_1.md %}
- **Tier 2**:
{% include_relative partials/github-topics_2.md %}
- **Tier 3**:
{% include_relative partials/github-topics_3.md %}

<!--

{% for item in site.i18n.mul.featured_compilations %}
  {{ item | json }}
  {{ item.name | t }}
  {% for item2 in item.resources %}
    {{ item2.name | t }}
  {% endfor %}
{% endfor %}

{{ datapackage.name }}
{{ datapackage.resource.biosafety_levels }}


-->


## License

[![Public Domain](partials/public-domain.png)](UNLICENSE)

To the extent possible under law, [Emerson Rocha](https://github.com/fititnt)
has waived all copyright and related or neighboring rights to this work to
[Public Domain](UNLICENSE).

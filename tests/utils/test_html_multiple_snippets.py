import pytest

from altair.utils.html import spec_to_html


@pytest.mark.parametrize("requirejs", [True, False])
def test_standard_template_targets_adjacent_output_div(requirejs):
    spec = {
        "data": {"url": "data.json"},
        "mark": {"type": "point"},
        "encoding": {
            "x": {"field": "x", "type": "quantitative"},
            "y": {"field": "y", "type": "quantitative"},
        },
    }
    html = spec_to_html(
        spec,
        mode="vega-lite",
        requirejs=requirejs,
        fullhtml=False,
        vegalite_version="6.0",
        vegaembed_version="7",
        vega_version="6",
    )

    # Each snippet should resolve its own adjacent output div rather than the
    # first matching ID in the document. This allows multiple snippets that use
    # the default output_div="vis" to coexist on the same page.
    assert "let outputDiv = document.currentScript.previousElementSibling;" in html
    assert "vegaEmbed(outputDiv, spec, embedOpt)" in html
    assert 'vegaEmbed("#vis", spec, embedOpt)' not in html

    combined = html + html
    assert combined.count("document.currentScript.previousElementSibling") == 2

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPARE = ROOT / "compare.html"
INDEX = ROOT / "index.html"


def test_compare_page_exists_and_loads_tracker_catalog():
    html = COMPARE.read_text()

    assert "Sprite Compare" in html
    assert "loadCatalog" in html
    assert 'fetch("index.html")' in html
    assert "spriteAssets" in html
    assert "const catalogMatch = trackerHtml.match" in html
    assert "new Function" in html


def test_compare_page_accepts_two_tracker_exports():
    html = COMPARE.read_text()

    assert 'id="leftJson"' in html
    assert 'id="rightJson"' in html
    assert "parseTrackerState" in html
    assert "JSON.parse" in html
    assert "Boolean(value.collected) || mastered" in html
    assert "compareMode" in html
    assert 'data-mode="collected"' in html
    assert 'data-mode="mastered"' in html


def test_compare_page_accepts_short_codes_and_json_exports():
    html = COMPARE.read_text()

    assert 'const CODE_PREFIX = "spr1."' in html
    assert "decodeStateCode" in html
    assert "parseStateInput" in html
    assert "fromUrlBase64" in html
    assert "if (text.startsWith(CODE_PREFIX))" in html
    assert "parseTrackerState" in html
    assert "JSON.parse(text)" in html


def test_compare_page_renders_missing_and_overlap_states():
    html = COMPARE.read_text()

    assert "renderCompare" in html
    assert "only-left" in html
    assert "only-right" in html
    assert "both" in html
    assert "neither" in html
    assert "needs-left" in html
    assert "needs-right" in html
    assert "leftHas && !rightHas" in html
    assert "rightHas && !leftHas" in html
    assert "sprite.released" in html
    assert 'location.pathname.startsWith("/sprites/")' in html
    assert 'src="${assetPrefix}${sprite.image}"' in html


def test_tracker_links_to_compare_page():
    html = INDEX.read_text()

    assert 'href="/sprites/compare"' in html
    assert "Compare" in html

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SPRITE_ASSETS = ROOT / "assets" / "sprites"
REFERENCE_ASSET = ROOT / "assets" / "reference" / "sprite-tracker-reference.jpeg"
FNASSIST_V4110_ASSET = ROOT / "assets" / "reference" / "fnassist-v4110-sprites.jpg"


def test_tracker_page_exists():
    assert INDEX.exists()


def test_tracker_has_collected_and_mastered_controls():
    html = INDEX.read_text()

    assert "collected" in html
    assert "mastered" in html
    assert "localStorage" in html
    assert "spriteTrackerState" in html


def test_tracker_renders_visible_reference_count():
    html = INDEX.read_text()

    assert "SPRITE_TOTAL = visibleSpriteAssets.length" in html
    assert "70 sprite variants" in html


def test_tracker_has_progress_and_filtering():
    html = INDEX.read_text()

    assert "collectedCount" in html
    assert "masteredCount" in html
    assert "data-filter" in html
    assert 'data-filter="hide-mastered"' in html
    assert "FILTER_KEY" in html
    assert "spriteTrackerActiveFilter" in html
    assert "setActiveFilter" in html
    assert "localStorage.setItem(FILTER_KEY" in html
    assert "localStorage.getItem(FILTER_KEY)" in html
    assert "exportData" in html


def test_tracker_uses_real_sprite_asset_urls():
    html = INDEX.read_text()

    assert 'assetBase = "assets/sprites"' in html
    assert '"Mat1", "Water Sprite"' in html
    assert "fortnite-api.com/images/cosmetics/br/backpack_coldtrophy" not in html
    assert "Water Sprite" in html
    assert "Quack Zero Point Sprite" in html


def test_tracker_excludes_mastery_pod_and_groups_rows():
    html = INDEX.read_text()

    assert "Sprite Mastery Pod" not in html
    assert "renderGroup" in html
    assert "sprite-row" in html
    assert "Water Sprite" in html
    assert "Fire Sprite" in html


def test_tracker_temporarily_hides_unavailable_variants():
    html = INDEX.read_text()

    assert 'const unavailableVariantPrefixes = ["Gem", "Holofoil", "Cube"]' in html
    assert "const visibleSpriteAssets = spriteAssets.filter" in html
    assert "unavailableVariantPrefixes.some" in html
    assert "visibleSpriteAssets.map" in html


def test_tracker_uses_requested_sprite_row_order():
    html = INDEX.read_text()

    assert "const groupOrder" in html
    group_order_block = html.split("const groupOrder = [", 1)[1].split("];", 1)[0]
    expected_order = [
        '"Water Sprite",',
        '"Earth Sprite",',
        '"Fire Sprite",',
        '"Duck Sprite",',
        '"Ghost Sprite",',
        '"Dream Sprite",',
        '"Demon Sprite",',
        '"Punk Sprite",',
        '"King Sprite",',
        '"TheBurntPeanut Sprite",',
        '"Fishy Sprite",',
        '"Soccer Striker Sprite",',
        '"Aura Sprite",',
        '"Boss Sprite",',
    ]
    positions = [group_order_block.index(item) for item in expected_order]
    assert positions == sorted(positions)


def test_tracker_downloads_sprite_assets_locally():
    assert (SPRITE_ASSETS / "mat1.png").exists()
    assert (SPRITE_ASSETS / "mat55.png").exists()
    assert not (SPRITE_ASSETS / "mat0.png").exists()


def test_tracker_uses_local_reference_image():
    html = INDEX.read_text()

    assert "assets/reference/sprite-tracker-reference.jpeg" in html
    assert "i.redd.it/x3bgjvo3mf9h1.jpeg" not in html
    assert REFERENCE_ASSET.exists()


def test_tracker_has_collapsible_sidebar_and_file_sync():
    html = INDEX.read_text()

    assert "toggleSidebar" in html
    assert "side-collapsed" in html
    assert "panel-control" in html
    assert "panel-toggle" in html
    assert 'id="toggleSidebar" type="button" class="panel-toggle"' in html
    assert "SERVER_STATE_URL" in html
    assert "/api/state" in html
    assert "persistServerState" in html


def test_tracker_includes_verified_v4110_sprites():
    html = INDEX.read_text()

    assert "Boxx Sprite" not in html
    assert "Auta Sprite" not in html
    assert "Grim Reaper Sprite" in html
    assert "Soccer Striker Sprite" in html
    assert "Fishy Sprite" in html
    assert "Aura Sprite" in html
    assert "Boss Sprite" in html
    assert "Seven Sprite" in html
    assert "Air Sprite" in html
    assert "assets/reference/fnassist-v4110-sprites.jpg" in html
    assert "FNAssist v41.10" in html
    assert FNASSIST_V4110_ASSET.exists()


def test_verified_sprite_crops_are_explicit_and_fitted():
    html = INDEX.read_text()

    assert "const V4110_CROPS" in html
    assert "const V4110_COLUMN_X" in html
    assert "const V4110_ROW_Y" in html
    assert "const V4110_CELL_SIZE = 512" in html
    assert "const V4110_CROP_INSET = 72" in html
    assert "makeV4110Crop" in html
    assert "cropViewBox" in html
    assert "centeredCrop" not in html
    assert "preserveAspectRatio=\"xMidYMid meet\"" in html
    assert 'viewBox="${cropBox}"' in html
    assert "sprite-crop" in html
    assert "sprite-canvas" not in html
    assert "getImageData" not in html


def test_sprite_art_cannot_cover_controls():
    html = INDEX.read_text()

    assert "isolation: isolate" in html
    assert "z-index: 0" in html
    assert "z-index: 1" in html
    assert "pointer-events: none" in html


def test_compact_buttons_do_not_overflow_cards():
    html = INDEX.read_text()

    assert 'aria-label="Toggle collected' in html
    assert 'aria-label="Toggle mastered' in html
    assert ">Have</button>" in html
    assert ">Master</button>" in html


def test_sprite_cards_constrain_text_and_controls():
    html = INDEX.read_text()

    assert "grid-template-columns: repeat(auto-fill, minmax(9.25rem, 1fr))" in html
    assert "overflow: hidden" in html
    assert "grid-template-columns: minmax(0, 1fr) auto" in html
    assert "max-width: 100%" in html


def test_sprite_cards_show_verified_player_skills_only():
    html = INDEX.read_text()

    assert "spriteSkills" in html
    assert "row-skill" in html
    assert "Water shield regen" in html
    assert "Rare chest boost" in html
    assert "Overdrive on move" in html
    assert "${groupSkill ? `<span class=\"row-skill\" title=\"${groupSkill}\">${groupSkill}</span>` : \"\"}" in html
    assert "${sprite.skill ? `<div class=\"skill-strip\"" not in html
    assert "Aqua pulse" not in html
    assert "Gold sheen" not in html
    assert "variantEffects" not in html

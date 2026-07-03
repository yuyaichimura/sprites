from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SPRITE_ASSETS = ROOT / "assets" / "sprites"
REFERENCE_ASSET = ROOT / "assets" / "reference" / "sprite-tracker-reference.jpeg"


def test_tracker_page_exists():
    assert INDEX.exists()


def test_tracker_has_collected_and_mastered_controls():
    html = INDEX.read_text()

    assert "collected" in html
    assert "mastered" in html
    assert "localStorage" in html
    assert "spriteTrackerState" in html
    assert "const next = { ...source }" in html
    assert "state = normalizeState(imported)" in html


def test_tracker_renders_visible_reference_count():
    html = INDEX.read_text()

    assert "SPRITE_TOTAL = spriteAssets.filter((sprite) => sprite.released).length" in html
    assert "spriteTotalLabel.textContent = SPRITE_TOTAL" in html
    assert 'id="spriteTotalLabel">61</span> sprite variants' in html


def test_tracker_has_progress_and_filtering():
    html = INDEX.read_text()

    assert "toolbar-progress" in html
    assert "progress-pill" in html
    assert "font-size: 1.32rem" in html
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


def test_tracker_uses_fortnitegg_sprite_asset_urls():
    html = INDEX.read_text()

    assert "assets/sprites/mat1.webp" in html
    assert '{ id: "mat1", name: "Water Sprite"' in html
    assert "fortnite-api.com/images/cosmetics/br/backpack_coldtrophy" not in html
    assert "Water Sprite" in html
    assert "Quack Zero Point Sprite" not in html


def test_tracker_excludes_mastery_pod_and_groups_rows():
    html = INDEX.read_text()

    assert "Sprite Mastery Pod" not in html
    assert "renderGroup" in html
    assert "sprite-row" in html
    assert "Water Sprite" in html
    assert "Fire Sprite" in html


def test_tracker_marks_and_hides_unreleased_by_default():
    html = INDEX.read_text()

    assert "UNRELEASED_KEY" in html
    assert "spriteTrackerShowUnreleased" in html
    assert 'showUnreleased = localStorage.getItem(UNRELEASED_KEY) === "true"' in html
    assert "toggleUnreleased" in html
    assert 'released: false' in html
    assert 'card.dataset.released = sprite.released ? "true" : "false"' in html
    assert 'const matchesRelease = showUnreleased || card.dataset.released === "true"' in html
    assert "setShowUnreleased(showUnreleased, false)" in html


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
        '"Burnt Peanut",',
        '"Fishy Sprite",',
        '"Striker Sprite",',
        '"Aura Sprite",',
        '"Boss Sprite",',
        '"Grim Sprite",',
        '"Air Sprite",',
        '"Seven Sprite",',
    ]
    positions = [group_order_block.index(item) for item in expected_order]
    assert positions == sorted(positions)


def test_tracker_downloads_sprite_assets_locally():
    assert (SPRITE_ASSETS / "mat1.webp").exists()
    assert (SPRITE_ASSETS / "v4110-soccer-striker.webp").exists()
    assert len(list(SPRITE_ASSETS.glob("*.webp"))) == 82
    assert not (SPRITE_ASSETS / "fortnitegg").exists()
    assert not (SPRITE_ASSETS / "mat0.webp").exists()


def test_tracker_removes_reference_tracker_image_from_ui():
    html = INDEX.read_text()

    assert "assets/reference/sprite-tracker-reference.jpeg" not in html
    assert "Original Fortnite Runners sprite tracker reference" not in html
    assert "i.redd.it/x3bgjvo3mf9h1.jpeg" not in html


def test_tracker_has_collapsible_sidebar_and_file_sync():
    html = INDEX.read_text()

    assert "toggleSidebar" in html
    assert "side-collapsed" in html
    assert "panel-control" in html
    assert "panel-toggle" in html
    assert "menu-bars" in html
    assert "storedSidebar" in html
    assert "defaultSidebarCollapsed" in html
    assert 'window.matchMedia("(max-width: 880px)").matches' in html
    assert "toggleControls" in html
    assert "controls-open" in html
    assert "toolbar-menu" in html
    assert "mobile-controls" in html
    assert "cog-icon" in html
    assert 'aria-label="Show filters"' in html
    assert 'aria-label="Hide panel"' in html
    assert 'toggleSidebar.setAttribute("aria-label"' in html
    assert "SERVER_STATE_URL" in html
    assert "/api/state" in html
    assert "persistServerState" in html


def test_tracker_includes_fortnitegg_sprite_assets():
    html = INDEX.read_text()

    assert "Boxx Sprite" not in html
    assert "Auta Sprite" not in html
    assert "Grim Sprite" in html
    assert "Striker Sprite" in html
    assert "Fishy Sprite" in html
    assert "Aura Sprite" in html
    assert "Boss Sprite" in html
    assert "Seven Sprite" in html
    assert "Air Sprite" in html
    assert "assets/sprites/v4110-grim-reaper.webp" in html
    assert "assets/sprites/v4110-soccer-striker.webp" in html
    assert "FNAssist v41.10" not in html


def test_tracker_uses_uniform_fortnitegg_images_instead_of_crops():
    html = INDEX.read_text()

    assert "const V4110_CROPS" not in html
    assert "makeV4110Crop" not in html
    assert "cropViewBox" not in html
    assert "assets/sprites/" in html
    assert "preserveAspectRatio=\"xMidYMid meet\"" not in html
    assert "sprite-crop" not in html
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


def test_tracker_includes_fortnitegg_metadata():
    html = INDEX.read_text()

    assert "rarity" in html
    assert "dropRate" in html
    assert "availability" in html
    assert '{ id: "mat1", name: "Water Sprite", image: "assets/sprites/mat1.webp", rarity: "rare", dropRate: "12.83%", released: true' in html
    assert '{ id: "v4110-air", name: "Air Sprite", image: "assets/sprites/v4110-air.webp", rarity: "rare", dropRate: "0%", released: false' in html


def test_sprite_cards_show_verified_player_skills_only():
    html = INDEX.read_text()

    assert "spriteSkills" in html
    assert "row-skill" in html
    assert "Shield regen in water" in html
    assert "Rare chest boost" in html
    assert "Overdrive on mantle" in html
    assert "Max HP/Shield up" in html
    assert "Mark attackers" in html
    assert "Sprint/jump boost" in html
    assert "Enemy foot trails" in html
    assert "${groupSkill ? `<span class=\"row-skill\" title=\"${groupSkill}\">${groupSkill}</span>` : \"\"}" in html
    assert "${sprite.skill ? `<div class=\"skill-strip\"" not in html
    assert "Aqua pulse" not in html
    assert "Gold sheen" not in html
    assert "variantEffects" not in html


def test_sprite_rows_show_level_effects():
    html = INDEX.read_text()

    assert "spriteLevelEffects" in html
    assert "row-levels" in html
    assert "row-level" in html
    assert "2 Shield/tick" in html
    assert "150 dmg trigger" in html
    assert "10% rare loot" in html
    assert "6s Overdrive" in html
    assert "+25 HP/Shield" in html

def test_variant_chips_get_variant_classes():
    html = INDEX.read_text()

    assert "const variantClass = sprite.variant.toLowerCase()" in html
    assert "variantClass," in html
    assert 'class="variant-chip ${sprite.variantClass}"' in html
    assert 'variant-chip undefined' not in html



def test_tracker_has_local_favicon():
    html = INDEX.read_text()

    assert 'rel="icon"' in html
    assert 'assets/favicon.svg' in html
    assert (ROOT / "assets" / "favicon.svg").exists()

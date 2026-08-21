from scripts.build_slides import decks, validate_sources


def test_romeo_delivery_decks_cover_curriculum_macro_blocks():
    validate_sources()
    assert len(decks()) == 10

import importlib

SEGMENTS = tuple(
    importlib.import_module(".{}".format(mod), "pbIII.parts").make(**kwargs)
    for mod, kwargs in (
        ("bell_chords", {"name": "ONE_BELLS"}),
        ("fade_in", {"name": "ONE_FADE_IN"}),
        ("cantus_firmus", {"name": "ONE_CANTUS_FIRMUS"}),
        ("bell_chords_two", {"name": "TWO_BELLS"}),
        ("dense_glitter", {"name": "TWO_DENSE_GLITTER"}),
        ("three", {"name": "THREE"}),
        # ("glitter", {"name": "TWO_GLITTER"}),
        # ("cantus_firmus_two", {"name": "TWO_CANTUS_FIRMUS"}),
        # ("silent_speech", {"name": "ONE_SILENT_SPEECH"}),
        # ("chords_with_speech", {"name": "ONE_CHORDS_WITH_SPEECH"}),
        # ("cantus_firmus_inverse", {"name": "ONE_CANTUS_FIRMUS_INVERSE"}),
        # ("calm_cp2", {}),
        # ("radio_chords", {}),
    )
)

import importlib

SEGMENTS = tuple(
    importlib.import_module(".{}".format(mod), "pbIII.parts").make(**kwargs)
    for mod, kwargs in (
        ("bell_chords", {"name": "ONE_BELLS"}),
        ("fade_in", {"name": "ONE_FADE_IN"}),
        ("cantus_firmus", {"name": "ONE_CANTUS_FIRMUS"}),
        ("silent_speech", {"name": "ONE_SILENT_SPEECH"}),
        ("chords_with_speech", {"name": "ONE_CHORDS_WITH_SPEECH"}),
        # ("dense_glitter", {"name": "ONE_DENSE_GLITTER"}),
        # ("cantus_firmus_inverse", {"name": "ONE_CANTUS_FIRMUS_INVERSE"}),
        # ("calm_cp", {}),
        # ("glitter", {}),
        # ("radio_chords", {}),
    )
)

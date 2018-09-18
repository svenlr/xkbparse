import pypeg2


class KeyCode:
    grammar = "<", pypeg2.name(), ">"


class KeySym:
    grammar = pypeg2.name()


class KeySymLevels(pypeg2.List):
    grammar = "[", pypeg2.optional(pypeg2.maybe_some(KeySym, ","), KeySym), "]"


class KeyDefSymbols:
    grammar = "symbols", "[", pypeg2.attr("group", pypeg2.Symbol), "]", "=", pypeg2.attr("levels", KeySymLevels)


class KeyDef(pypeg2.List):
    grammar = "key", KeyCode, "{", \
              pypeg2.optional(("type", "=", "\"", pypeg2.attr("type", pypeg2.Symbol), "\""), ","), \
              pypeg2.maybe_some(KeyDefSymbols, ","), \
              KeyDefSymbols, \
              "}"

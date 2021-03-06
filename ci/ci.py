import json


def load_spells():
    with open("./spells.json") as f:
        spells = json.load(f)
    return spells


def ensure_no_dupes(data):
    names = [s['name'] for s in data]
    assert len(list(set(names))) == len(names)
    print("No duplicates found.")


def ensure_keys(spell):
    assert "name" in spell and "automation" in spell
    assert isinstance(spell['name'], str)
    assert isinstance(spell['automation'], list) or spell['automation'] is None


def check_automation(spell, automation):
    for effect in automation:
        check_effect(spell, effect)


def check_effect(spell, effect):
    assert isinstance(effect, dict)
    assert "type" in effect
    assert effect['type'] in EFFECT_TYPES
    EFFECT_TYPES[effect['type']](spell, effect)
    if 'meta' in effect:
        for metaeffect in effect['meta']:
            check_effect(spell, metaeffect)


def check_target(spell, effect):
    print("Found target...")
    assert 'target' in effect
    assert effect['target'] in ("all", "each", "self") or (isinstance(effect['target'], int) and effect['target'] > 0)
    assert 'effects' in effect
    for effect_ in effect['effects']:
        check_effect(spell, effect_)


def check_attack(spell, effect):
    print("Found attack...")
    assert 'hit' in effect
    assert 'miss' in effect
    for effect_ in effect['hit']:
        check_effect(spell, effect_)
    for effect_ in effect['miss']:
        check_effect(spell, effect_)
    if 'attackBonus' in effect:
        assert isinstance(effect['attackBonus'], str)


def check_save(spell, effect):
    print("Found save...")
    assert 'stat' in effect
    assert effect['stat'] in ('str', 'dex', 'con', 'int', 'wis', 'cha')
    assert 'fail' in effect
    assert 'success' in effect
    for effect_ in effect['fail']:
        check_effect(spell, effect_)
    for effect_ in effect['success']:
        check_effect(spell, effect_)
    if 'dc' in effect:
        assert isinstance(effect['dc'], str)


def check_damage(spell, effect):
    print("Found damage...")
    assert 'damage' in effect
    if 'higher' in effect:
        check_higher(effect['higher'])
    if 'cantripScale' in effect:
        assert isinstance(effect['cantripScale'], bool)

def check_temphp(spell, effect):
    print("Found temphp...")
    assert 'amount' in effect
    if 'higher' in effect:
        check_higher(effect['higher'])
    if 'cantripScale' in effect:
        assert isinstance(effect['cantripScale'], bool)


def check_ieffect(spell, effect):
    print("Found ieffect...")
    assert 'name' in effect
    assert 'duration' in effect
    assert 'effects' in effect
    assert isinstance(effect['name'], str)
    assert isinstance(effect['duration'], (int, str))
    assert isinstance(effect['effects'], str)

    if effect['name'] == spell['name']:
        print("Warning: ieffect name is same as spell name")
    if 'end' in effect:
        assert isinstance(effect['end'], bool)


def check_roll(spell, effect):
    print("Found roll...")
    assert 'dice' in effect
    assert 'name' in effect
    assert isinstance(effect['dice'], str)
    assert isinstance(effect['name'], str)
    if 'higher' in effect:
        check_higher(effect['higher'])
    if 'cantripScale' in effect:
        assert isinstance(effect['cantripScale'], bool)
    if 'hidden' in effect:
        assert isinstance(effect['hidden'], bool)


def check_text(spell, effect):
    print("Found text...")
    assert 'text' in effect
    assert isinstance(effect['text'], str)


EFFECT_TYPES = {
    "target": check_target,
    "attack": check_attack,
    "save": check_save,
    "damage": check_damage,
    "temphp": check_temphp,
    "ieffect": check_ieffect,
    "roll": check_roll,
    "text": check_text
}


def check_higher(higher):
    for k, v in higher.items():
        assert isinstance(k, (str, int))
        assert isinstance(v, str)
        assert 0 <= int(k) <= 9


def run():
    data = load_spells()
    ensure_no_dupes(data)
    for spell in data:
        print(f"Running checks on {spell['name']}...")
        ensure_keys(spell)
        if spell['automation'] is not None:
            check_automation(spell, spell['automation'])
        print("OK")


if __name__ == '__main__':
    run()
    print("All checks passed.")

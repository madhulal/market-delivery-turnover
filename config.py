from mongo_utils import get_record_by_id


def is_fundamnetal_enabled():
    return is_settings_enabled('fundamental')


def is_technical_enabled():
    return is_settings_enabled('technical')


def is_nse_fetch_enabled():
    return is_settings_enabled('nse')


def is_bse_fetch_enabled():
    return is_settings_enabled('bse')


def is_settings_enabled(collection):
    record = get_record_by_id('config', collection)
    return record['enabled']

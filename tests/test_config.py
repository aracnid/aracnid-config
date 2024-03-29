# pylint: disable=protected-access,unused-variable
"""Test functions for config.py.
"""
import os

from datetime import datetime, timezone
import pytest

from aracnid_config import Config
import aracnid_config

# initialize module variables
TEST_PROPS_NAME = '_test_props'
UTC = timezone.utc


@pytest.fixture(name='config_obj')
def fixture_config_obj():
    """Pytest fixture to initialize and return a Config object
    """
    return Config()

@pytest.fixture(name='config_props')
def fixture_config_props(config_obj):
    """Pytest fixture to initialize and load a configuration set.
    """
    config_obj.load_properties(TEST_PROPS_NAME)
    return config_obj

def test_init_config_db(config_obj):
    """Tests Config initialization.
    """
    assert isinstance(config_obj, aracnid_config.config.Config)
    assert config_obj._collection_name == os.environ.get('CONFIG_COLLECTION')

def test_init_config_collection(config_obj):
    """Tests Config collection initialization.
    """
    config_collection = os.environ.get('CONFIG_COLLECTION')
    assert config_obj._collection_name == config_collection

    assert config_obj._collection is not None
    assert config_obj._collection.name == config_collection

def test_init_config_by_name():
    """Tests Config initialization, passing config set name.
    """
    config_collection = os.environ.get('CONFIG_COLLECTION')
    config_obj = Config(TEST_PROPS_NAME)

    assert config_obj
    assert config_obj._collection is not None
    assert config_obj._collection.name == config_collection
    assert config_obj.name == TEST_PROPS_NAME

def test_load_properties(config_props):
    """Tests loading config properties.
    """
    assert config_props.name == TEST_PROPS_NAME

def test_create_update_and_read_property(config_props):
    """Tests creating, updating, and reading config properties.
    """
    config_props.newprop = 'abc'
    config_props.update()
    props = config_props.props
    assert props['newprop'] == 'abc'

    config_collection = config_props._collection
    props = config_collection.find_one({'_id': TEST_PROPS_NAME})['props']
    assert props['newprop'] == 'abc'

def test_create_update_and_read_datetime_property(config_props):
    """Tests creating, updating, and reading datetime properties.
    """
    config_props.auto_update = False
    dt_utc = datetime(2020, 8, 24, 10, 50).astimezone(UTC)
    config_props.prop_attr = dt_utc
    # config_props.update()
    props = config_props.props
    assert config_props.prop_attr == dt_utc

    config_collection = config_props._collection
    props = config_collection.find_one({'_id': TEST_PROPS_NAME})['props']
    with pytest.raises(KeyError) as excinfo:
        var = props['prop_attr']

    assert 'prop_attr' in str(excinfo.value)

def test_create_update_and_read_datetime_property_auto_update(config_props):
    """Tests creating, updating, and reading datetime property with auto update.
    """
    dt_utc = datetime(2020, 8, 24, 10, 50).astimezone(UTC)
    config_props.prop_attr_auto = dt_utc
    props = config_props.props
    assert config_props.prop_attr_auto == dt_utc

    config_collection = config_props._collection
    props = config_collection.find_one({'_id': TEST_PROPS_NAME})['props']
    assert props['prop_attr_auto'] == dt_utc

def test_create_update_and_read_datetime_property_subscripted(config_props):
    """Tests creating, updating, and reading subscripted property.
    """
    config_props.auto_update = False
    dt_utc = datetime(2020, 8, 24, 10, 50).astimezone(UTC)
    config_props['sub'] = dt_utc
    # config_props.update()
    props = config_props.props
    assert config_props['sub'] == dt_utc

    config_collection = config_props._collection
    props = config_collection.find_one({'_id': TEST_PROPS_NAME})['props']
    with pytest.raises(KeyError) as excinfo:
        var = props['sub']

    assert 'sub' in str(excinfo.value)

def test_create_update_and_read_datetime_property_subscripted_auto_update(config_props):
    """Tests creating, updating, and reading subscripted property, auto update.
    """
    dt_utc = datetime(2020, 8, 24, 10, 50).astimezone(UTC)
    config_props['sub_auto'] = dt_utc
    props = config_props.props
    assert config_props['sub_auto'] == dt_utc

    config_collection = config_props._collection
    props = config_collection.find_one({'_id': TEST_PROPS_NAME})['props']
    assert props['sub_auto'] == dt_utc

def test_delete_property(config_props):
    """Tests deleting property.
    """
    config_collection = config_props._collection
    props = config_collection.find_one({'_id': TEST_PROPS_NAME})['props']
    count_previous = len(props)

    del config_props.newprop
    config_props.update()

    props = config_collection.find_one({'_id': TEST_PROPS_NAME})['props']
    count_deleted = len(props)

    assert count_previous == count_deleted + 1

def test_delete_properties(config_props):
    """Tests deleting entire config set.
    """
    config_collection = config_props._collection
    count_previous = config_collection.count_documents({})

    config_props.delete()

    count_after_deleted = config_collection.count_documents({})

    assert count_previous == count_after_deleted + 1
    assert config_props.name == TEST_PROPS_NAME

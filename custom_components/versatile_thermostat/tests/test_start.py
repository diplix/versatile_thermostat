""" Test the normal start of a Thermostat """
from unittest.mock import patch, call

from homeassistant.core import HomeAssistant
from homeassistant.components.climate import HVACAction, HVACMode
from homeassistant.config_entries import ConfigEntryState

from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components.climate import ClimateEntity, DOMAIN as CLIMATE_DOMAIN

from pytest_homeassistant_custom_component.common import MockConfigEntry

from ..climate import VersatileThermostat

from .commons import *  # pylint: disable=wildcard-import, unused-wildcard-import


@pytest.mark.parametrize("expected_lingering_tasks", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_over_switch_full_start(hass: HomeAssistant, skip_hass_states_is_state):
    """Test the normal full start of a thermostat in thermostat_over_switch type"""

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverSwitchMockName",
        unique_id="uniqueId",
        data=FULL_SWITCH_CONFIG,
    )

    with patch(
        "custom_components.versatile_thermostat.climate.VersatileThermostat.send_event"
    ) as mock_send_event:
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.state is ConfigEntryState.LOADED

        def find_my_entity(entity_id) -> ClimateEntity:
            """Find my new entity"""
            component: EntityComponent[ClimateEntity] = hass.data[CLIMATE_DOMAIN]
            for entity in component.entities:
                if entity.entity_id == entity_id:
                    return entity

        entity: VersatileThermostat = find_my_entity("climate.theoverswitchmockname")

        assert entity

        assert entity.name == "TheOverSwitchMockName"
        assert entity._is_over_climate is False
        assert entity.hvac_action is HVACAction.OFF
        assert entity.hvac_mode is HVACMode.OFF
        assert entity.target_temperature == entity.min_temp
        assert entity.preset_modes == [
            PRESET_NONE,
            PRESET_ECO,
            PRESET_COMFORT,
            PRESET_BOOST,
            PRESET_ACTIVITY,
        ]
        assert entity.preset_mode is PRESET_NONE
        assert entity._security_state is False
        assert entity._window_state is None
        assert entity._motion_state is None
        assert entity._presence_state is None
        assert entity._prop_algorithm is not None

        # should have been called with EventType.PRESET_EVENT and EventType.HVAC_MODE_EVENT
        assert mock_send_event.call_count == 2

        mock_send_event.assert_has_calls(
            [
                call.send_event(EventType.PRESET_EVENT, {"preset": PRESET_NONE}),
                call.send_event(
                    EventType.HVAC_MODE_EVENT,
                    {"hvac_mode": HVACMode.OFF},
                ),
            ]
        )


@pytest.mark.parametrize("expected_lingering_tasks", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_over_climate_full_start(hass: HomeAssistant, skip_hass_states_is_state):
    """Test the normal full start of a thermostat in thermostat_over_climate type"""

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOverClimateMockName",
        unique_id="uniqueId",
        data=PARTIAL_CLIMATE_CONFIG,
    )

    fake_underlying_climate = MockClimate(hass, "mockUniqueId", "MockClimateName", {})

    with patch(
        "custom_components.versatile_thermostat.climate.VersatileThermostat.send_event"
    ) as mock_send_event, patch(
        "custom_components.versatile_thermostat.underlyings.UnderlyingClimate.find_underlying_climate",
        return_value=fake_underlying_climate,
    ) as mock_find_climate:
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.state is ConfigEntryState.LOADED

        def find_my_entity(entity_id) -> ClimateEntity:
            """Find my new entity"""
            component: EntityComponent[ClimateEntity] = hass.data[CLIMATE_DOMAIN]
            for entity in component.entities:
                if entity.entity_id == entity_id:
                    return entity

        entity = find_my_entity("climate.theoverclimatemockname")

        assert entity

        assert entity.name == "TheOverClimateMockName"
        assert entity._is_over_climate is True
        assert entity.hvac_action is HVACAction.OFF
        assert entity.hvac_mode is HVACMode.OFF
        assert entity.target_temperature == entity.min_temp
        assert entity.preset_modes == [
            PRESET_NONE,
            PRESET_ECO,
            PRESET_COMFORT,
            PRESET_BOOST,
        ]
        assert entity.preset_mode is PRESET_NONE
        assert entity._security_state is False
        assert entity._window_state is None
        assert entity._motion_state is None
        assert entity._presence_state is None

        # should have been called with EventType.PRESET_EVENT and EventType.HVAC_MODE_EVENT
        assert mock_send_event.call_count == 2
        mock_send_event.assert_has_calls(
            [
                call.send_event(EventType.PRESET_EVENT, {"preset": PRESET_NONE}),
                call.send_event(
                    EventType.HVAC_MODE_EVENT,
                    {"hvac_mode": HVACMode.OFF},
                ),
            ]
        )

        assert mock_find_climate.call_count == 1
        assert mock_find_climate.mock_calls[0] == call()
        mock_find_climate.assert_has_calls([call.find_underlying_entity()])


@pytest.mark.parametrize("expected_lingering_tasks", [True])
@pytest.mark.parametrize("expected_lingering_timers", [True])
async def test_over_4switch_full_start(hass: HomeAssistant, skip_hass_states_is_state):
    """Test the normal full start of a thermostat in thermostat_over_switch with 4 switches type"""

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="TheOver4SwitchMockName",
        unique_id="uniqueId",
        data=FULL_4SWITCH_CONFIG,
    )

    with patch(
        "custom_components.versatile_thermostat.climate.VersatileThermostat.send_event"
    ) as mock_send_event:
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.state is ConfigEntryState.LOADED

        def find_my_entity(entity_id) -> ClimateEntity:
            """Find my new entity"""
            component: EntityComponent[ClimateEntity] = hass.data[CLIMATE_DOMAIN]
            for entity in component.entities:
                if entity.entity_id == entity_id:
                    return entity

        entity: VersatileThermostat = find_my_entity("climate.theover4switchmockname")

        assert entity

        assert entity.name == "TheOver4SwitchMockName"
        assert entity._is_over_climate is False
        assert entity.hvac_action is HVACAction.OFF
        assert entity.hvac_mode is HVACMode.OFF
        assert entity.target_temperature == entity.min_temp
        assert entity.preset_modes == [
            PRESET_NONE,
            PRESET_ECO,
            PRESET_COMFORT,
            PRESET_BOOST,
            PRESET_ACTIVITY,
        ]
        assert entity.preset_mode is PRESET_NONE
        assert entity._security_state is False
        assert entity._window_state is None
        assert entity._motion_state is None
        assert entity._presence_state is None
        assert entity._prop_algorithm is not None

        assert entity.nb_underlying_entities == 4

        # Checks that we have the 4 UnderlyingEntity correctly configured
        for idx in range(4):
            under = entity.underlying_entity(idx)
            assert under is not None
            assert isinstance(under, UnderlyingSwitch)
            assert under.entity_id == "switch.mock_4switch" + str(idx)
            assert under.initial_delay_sec == 8 * 60 / 4 * idx

        # should have been called with EventType.PRESET_EVENT and EventType.HVAC_MODE_EVENT
        assert mock_send_event.call_count == 2

        mock_send_event.assert_has_calls(
            [
                call.send_event(EventType.PRESET_EVENT, {"preset": PRESET_NONE}),
                call.send_event(
                    EventType.HVAC_MODE_EVENT,
                    {"hvac_mode": HVACMode.OFF},
                ),
            ]
        )

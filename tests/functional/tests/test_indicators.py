import pytest
from ctrlibrary.core.utils import get_observables
from ctrlibrary.threatresponse.enrich import enrich_observe_observables
from tests.functional.tests.constants import (
    MODULE_NAME,
    ALIEN_VAULT_URL,
    CONFIDENCE_LEVEL
)


@pytest.mark.parametrize(
    'observable_type, observable',
    (('ip', '54.38.157.11'),
     ('domain', 'jsebnawkndwandawd.sh'),
     ('sha256',
      'af689a29dab28eedb5b2ee5bf0b94be2112d0881fad815fa082dc3b9d224fce0'),
     ('md5', 'f8290f2d593a05ea811edbd3bff6eacc'),
     ('sha1', 'da892cf09cf37a5f3aebed596652d209193c47eb'))
)
def test_positive_smoke_enrich_indicators(module_headers, observable,
                                          observable_type):
    """Perform testing for enrich observe observable endpoint to check
    indicators of AlienVault OTX module

    ID: CCTRI-1334-bcef4d6e-c1df-11ea-b3de-0242ac130004

    Steps:
        1. Send request to enrich observe observable endpoint

    Expectedresults:
        1. Response body contains indicators entity with needed fields from
        AlienVault OTX module

    Importance: Critical
    """
    observables = [{'type': observable_type, 'value': observable}]
    response_from_all_modules = enrich_observe_observables(
        payload=observables,
        **{'headers': module_headers}
    )['data']
    response_from_alien_vault = get_observables(response_from_all_modules,
                                                MODULE_NAME)
    assert response_from_alien_vault['module'] == MODULE_NAME
    assert response_from_alien_vault['module_instance_id']
    assert response_from_alien_vault['module_type_id']

    indicators = response_from_alien_vault['data']['indicators']

    assert len(indicators['docs']) > 0

    for indicator in indicators['docs']:
        assert 'tags' in indicator
        assert indicator['valid_time']['start_time']
        assert indicator['producer']
        assert indicator['schema_version']
        assert indicator['type'] == 'indicator'
        assert indicator['source'] == MODULE_NAME
        assert indicator['external_ids']
        assert 'short_description' in indicator
        assert indicator['title']
        assert indicator['source_uri'] == (
            f'{ALIEN_VAULT_URL}/pulse/{indicator["external_ids"][0]}')
        assert indicator['id'].startswith('transient:indicator')
        assert indicator['tlp']
        assert indicator['confidence'] == CONFIDENCE_LEVEL

    assert indicators['count'] == len(indicators['docs'])
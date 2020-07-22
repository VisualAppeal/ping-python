import json

from ping.ping import check_site


def test_200():
    response = check_site(json.loads('''{
        "name": "My Website",
        "checks": [
            {
                "type": "https",
                "enabled": true,
                "options": {
                    "validate_ssl": false,
                    "timeout": 5,
                    "urls": [
                        "http://httpstat.us/200"
                    ]
                }
            }
        ]
    }'''))

    assert response[0]["success"]


def test_500():
    response = check_site(json.loads('''{
        "name": "My Website",
        "checks": [
            {
                "type": "https",
                "enabled": true,
                "options": {
                    "validate_ssl": false,
                    "timeout": 5,
                    "urls": [
                        "http://httpstat.us/500"
                    ]
                }
            }
        ]
    }'''))

    assert not response[0]["success"]
    assert "Internal Server Error" in response[0]["message"]


def test_timeout():
    response = check_site(json.loads('''{
        "name": "My Website",
        "checks": [
            {
                "type": "https",
                "enabled": true,
                "options": {
                    "validate_ssl": false,
                    "timeout": 1,
                    "urls": [
                        "http://10.255.255.1"
                    ]
                }
            }
        ]
    }'''))

    assert not response[0]["success"]
    assert "Timeout" in response[0]["message"]


def test_valid_ssl():
    response = check_site(json.loads('''{
        "name": "My Website",
        "checks": [
            {
                "type": "https",
                "enabled": true,
                "options": {
                    "validate_ssl": true,
                    "timeout": 5,
                    "urls": [
                        "https://badssl.com/"
                    ]
                }
            }
        ]
    }'''))

    assert response[0]["success"]


def test_expired_ssl():
    response = check_site(json.loads('''{
        "name": "My Website",
        "checks": [
            {
                "type": "https",
                "enabled": true,
                "options": {
                    "validate_ssl": true,
                    "timeout": 5,
                    "urls": [
                        "https://expired.badssl.com/"
                    ]
                }
            }
        ]
    }'''))

    assert not response[0]["success"]
    assert "certificate has expired" in response[0]["message"]

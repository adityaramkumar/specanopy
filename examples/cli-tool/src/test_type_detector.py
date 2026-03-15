# generated_from: contracts/formats/json
# spec_hash: 8f053498a5673becd45aa5ef6eba1727bdeb891c42ec72c0e8ba055b6b13b7b2
# generated_at: 2026-03-15T02:27:44.663978+00:00
# agent: testing-agent
import pytest
from type_detector import TypeDetector


class TestTypeDetector:
    @pytest.mark.parametrize('value,expected', [
        ('123', 123),
        ('-456', -456),
        ('0', 0),
    ])
    def test_detect_integer(self, value, expected):
        """Verify integer detection for fields matching ^-?\d+$."""
        result = TypeDetector.detect(value)
        assert result == expected
        assert isinstance(result, int)

    @pytest.mark.parametrize('value,expected', [
        ('123.45', 123.45),
        ('-0.5', -0.5),
        ('0.0', 0.0),
    ])
    def test_detect_float(self, value, expected):
        """Verify float detection for fields matching ^-?\d+\.\d+$."""
        result = TypeDetector.detect(value)
        assert result == expected
        assert isinstance(result, float)

    @pytest.mark.parametrize('value,expected', [
        ('true', True),
        ('True', True),
        ('TRUE', True),
        ('false', False),
        ('False', False),
        ('FALSE', False),
    ])
    def test_detect_boolean(self, value, expected):
        """Verify boolean detection for true/false (case-insensitive)."""
        result = TypeDetector.detect(value)
        assert result == expected
        assert isinstance(result, bool)

    def test_detect_null(self):
        """Verify empty fields become null."""
        result = TypeDetector.detect('')
        assert result is None

    @pytest.mark.parametrize('value', [
        'abc',
        '12.3.4',
        '12a',
        'truee',
        '1.2.3',
        '--1',
        '1.',
    ])
    def test_detect_string(self, value):
        """Verify everything else remains a string."""
        result = TypeDetector.detect(value)
        assert result == value
        assert isinstance(result, str)

    def test_detect_row(self):
        """Verify type detection applied to all values in row dictionary."""
        row = {
            'id': '123',
            'price': '19.99',
            'active': 'true',
            'name': 'John Doe',
            'empty': '',
            'invalid_num': '12a'
        }
        expected = {
            'id': 123,
            'price': 19.99,
            'active': True,
            'name': 'John Doe',
            'empty': None,
            'invalid_num': '12a'
        }
        result = TypeDetector.detect_row(row)
        assert result == expected

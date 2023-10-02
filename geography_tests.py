from unittest import main, mock, TestCase

from geography import pick_location

def geography_mock(location_name):
    LOCATION_DATA = {
        "Tesco" : {"importance": 0.2},
        "London": {"importance": 0.3},
    }
    try:
        return LOCATION_DATA[location_name]
    except:
        return None

class TestPickLocationTestCase(TestCase):

    @mock.patch("geography.get_coordinates", side_effect=geography_mock)
    def test_calls_thingy(self, get_coordinates_mock):
        locations = ["Tesco", "London"]

        result = pick_location(locations)
        self.assertEqual(get_coordinates_mock.call_count, 2)
        get_coordinates_mock.assert_any_call("Tesco")
        get_coordinates_mock.assert_any_call("London")
        self.assertEqual(result, "London")


if __name__ == "__main__":
    main()
from dataclasses import dataclass
import datetime

@dataclass
class Coordinate:
    lat: float
    lng: float

    def __init__(self, coordinate: str):
        lat, lng = coordinate.split(',')

        if len(lat) == 0 or len(lng) == 0:
            raise ValueError('Invalid coordinate')

        self.lat = float(lat)
        self.lng = float(lng)

@dataclass
class CoordinateData:
    start: Coordinate
    end: Coordinate

    def __init__(self, start_coordinate: str, end_coordinate: str):
        try:
            self.start = Coordinate(start_coordinate)
            self.end = Coordinate(end_coordinate)
        except ValueError:
            raise ValueError('Invalid coordinate')


@dataclass
class DayConfigData:
    interval: int
    start_time: datetime.datetime
    end_time: datetime.datetime

# Holds all the days config
class DayConfig:
    days: dict[str, DayConfigData]

    def __init__(self):
        now = datetime.datetime.now()

        self.days = {
            'Monday': DayConfigData(
                interval=30,
                start_time=now.replace(hour=6, minute=0, second=0, microsecond=0),
                end_time=now.replace(hour=22, minute=0, second=0, microsecond=0),
            ),
            'Tuesday': DayConfigData(
                interval=60,
                start_time=now.replace(hour=6, minute=30, second=0, microsecond=0),
                end_time=now.replace(hour=21, minute=30, second=0, microsecond=0),
            ),
            'Wednesday': DayConfigData(
                interval=60,
                start_time=now.replace(hour=6, minute=0, second=0, microsecond=0),
                end_time=now.replace(hour=22, minute=0, second=0, microsecond=0),
            ),
            'Thursday': DayConfigData(
                interval=30,
                start_time=now.replace(hour=6, minute=0, second=0, microsecond=0),
                end_time=now.replace(hour=22, minute=0, second=0, microsecond=0),
            ),
            'Friday': DayConfigData(
                interval=30,
                start_time=now.replace(hour=6, minute=0, second=0, microsecond=0),
                end_time=now.replace(hour=22, minute=0, second=0, microsecond=0),
            ),
            'Saturday': DayConfigData(
                interval=60,
                start_time=now.replace(hour=6, minute=30, second=0, microsecond=0),
                end_time=now.replace(hour=21, minute=30, second=0, microsecond=0),
            ),
            'Sunday': DayConfigData(
                interval=60,
                start_time=now.replace(hour=6, minute=0, second=0, microsecond=0),
                end_time=now.replace(hour=22, minute=0, second=0, microsecond=0),
            ),
        }

    def get_day_config(self, day: str) -> DayConfigData:
        return self.days[day]

    def get_days(self) -> list[str]:
        return list(self.days.keys())

    def __datetime_range(self, start, end, delta):
        current = start
        while current <= end:
            yield current
            current += delta

    def get_time_range(self, day: str) -> list[datetime.time]:
        config = self.get_day_config(day)
        return [dt for dt in self.__datetime_range(config.start_time, config.end_time, datetime.timedelta(minutes=config.interval))]

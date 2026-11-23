import argparse
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse


REQUEST_COUNT = 10
CHUNK_SIZE = 64 * 1024
TIMEOUT = 30


def download_file(url):
    request = Request(
        url,
        headers={"User-Agent": "SpeedCheck/1.0"}
    )

    downloaded_bytes = 0
    start_time = time.perf_counter()

    with urlopen(request, timeout=TIMEOUT) as response:
        while True:
            chunk = response.read(CHUNK_SIZE)

            if not chunk:
                break

            downloaded_bytes += len(chunk)

    elapsed_time = time.perf_counter() - start_time

    return elapsed_time, downloaded_bytes


def main():
    parser = argparse.ArgumentParser(
        description="Измерение скорости скачивания файлов"
    )
    parser.add_argument("url", help="Адрес файла для скачивания")
    args = parser.parse_args()

    parsed_url = urlparse(args.url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        parser.error("Укажите корректный HTTP или HTTPS адрес")

    total_time = 0
    total_bytes = 0

    print(f"Адрес: {args.url}")
    print(f"Количество запросов: {REQUEST_COUNT}")
    print("-" * 45)

    for i in range(1, REQUEST_COUNT + 1):
        elapsed, size = download_file(args.url)

        total_time += elapsed
        total_bytes += size

        print(
            f"Запрос {i}: "
            f"{elapsed:.2f} сек., "
            f"{size / 1_000_000:.2f} MB"
        )

    average_time = total_time / REQUEST_COUNT
    speed = total_bytes / total_time / 1_000_000

    print("-" * 45)
    print(f"Среднее время запроса: {average_time:.2f} сек.")
    print(f"Общий объём данных: {total_bytes / 1_000_000:.2f} MB")
    print(f"Средняя скорость скачивания: {speed:.2f} MB/s")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as error:
        print(f"HTTP-ошибка: {error.code}")
    except URLError as error:
        print(f"Ошибка подключения: {error.reason}")
    except TimeoutError:
        print("Превышено время ожидания ответа")
    except OSError as error:
        print(f"Ошибка сети: {error}")

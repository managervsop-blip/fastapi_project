import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Настроить логирование: время, уровень, модуль, сообщение."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
        force=True,  # перезаписать существующую конфигурацию
    )

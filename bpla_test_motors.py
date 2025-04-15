from pymavlink import mavutil
import time


def set_motor_speed(mav, motor_id, percent, timeout=5):
    """Усовершенствованная функция управления моторами"""
    # 1. Проверка соединения
    if not mav.target_system:
        print("Нет подключения к автопилоту!")
        return False

    # 2. Подготовка команды
    pwm = int(1000 + percent * 10)
    pwm = max(1000, min(2000, pwm))

    # 3. Отправка команды
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,
        0,  # confirmation
        motor_id,
        mavutil.mavlink.MOTOR_TEST_THROTTLE_PWM,  # Используем PWM напрямую
        pwm,
        timeout,  # Время действия команды
        0, 0, 0  # unused
    )

    # 4. Проверка подтверждения
    ack = mav.recv_match(type='COMMAND_ACK', blocking=True, timeout=2)
    if ack:
        print(f"Результат: {mavutil.mavlink.enums['MAV_RESULT'][ack.result].name}")
        return ack.result == 0
    else:
        print("Нет подтверждения команды!")
        return False
def test_motors(connection_string='COM4'):
    try:
        # 1. Инициализация
        mav = mavutil.mavlink_connection(connection_string)
        mav.wait_heartbeat()
        print(f"Подключено к системе {mav.target_system}")



        # 3. Тест моторов
        print("\nТестирование моторов:")
        for motor_id in range(1, 5):
            print(f"\nМотор {motor_id}:")

            # Плавное увеличение скорости
            for percent in [1, 2, 3]:
                print(f"Установка {percent}%...", end=' ')
                success = set_motor_speed(mav, motor_id, percent)
                print("Успех" if success else "Ошибка")
                time.sleep(1)

            # Остановка
            set_motor_speed(mav, motor_id, 0)

    except Exception as e:
        print(f"Ошибка: {str(e)}")
    finally:
        # Гарантированная остановка
        for motor_id in range(1, 5):
            set_motor_speed(mav, motor_id, 0)
        print("\nТест завершен")


if __name__ == "__main__":
    test_motors()
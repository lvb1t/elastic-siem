"""
ICMP Flood Generator для тестирования Suricata
Правило: detection_filter: track by_src, count 50, seconds 1
"""

import socket
import struct
import time
import sys
from threading import Thread

def checksum(data):
    """Вычисление ICMP checksum"""
    if len(data) % 2 != 0:
        data += b'\x00'
    s = sum(struct.unpack('!%dH' % (len(data)//2), data))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff

def create_icmp_packet(seq):
    """Создание ICMP Echo Request пакета"""
    icmp_type = 8  # Echo Request
    icmp_code = 0
    checksum_val = 0
    identifier = 12345
    seq_num = seq
    payload = b'X' * 56  # 56 байт полезной нагрузки
    
    # Создаем временный пакет для расчета checksum
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum_val, identifier, seq_num)
    packet = icmp_header + payload
    
    # Рассчитываем checksum
    checksum_val = checksum(packet)
    
    # Создаем финальный пакет
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum_val, identifier, seq_num)
    return icmp_header + payload

def send_icmp_flood(target_ip, duration=2, packets_per_second=100):
    """Отправка ICMP флуда"""
    try:
        # Создаем raw socket (требует root прав)
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        
        print(f"🔥 Начинаем ICMP флуд на {target_ip}...")
        print(f"📊 Цель: {packets_per_second} пакетов/сек в течение {duration} секунд")
        
        start_time = time.time()
        packet_count = 0
        
        while time.time() - start_time < duration:
            for i in range(packets_per_second):
                # Создаем и отправляем пакет
                packet = create_icmp_packet(packet_count)
                sock.sendto(packet, (target_ip, 0))
                packet_count += 1
            
            # Спим 1 секунду между пакетами
            time.sleep(1)
            
            # Показываем прогресс
            elapsed = int(time.time() - start_time)
            print(f"✅ Отправлено {packet_count} пакетов за {elapsed} сек")
            
    except PermissionError:
        print("❌ Ошибка: требуются root права! Запустите с sudo")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        sock.close()

def main():
    if len(sys.argv) < 2:
        print("Использование: sudo python3 icmp_flood.py <TARGET_IP>")
        print("Пример: sudo python3 icmp_flood.py 192.168.1.50")
        sys.exit(1)
    
    target = sys.argv[1]
    
    # Отправляем 100 пакетов в секунду в течение 1 секунды
    # Этого достаточно чтобы превысить порог count 50, seconds 1
    send_icmp_flood(target, duration=1, packets_per_second=100)

if __name__ == "__main__":
    main()

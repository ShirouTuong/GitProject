"""
Script cap nhat toan dien Bao cao Bai tap lon / Bai kiem tra cuoi ky
Mon: Trien khai va Quan tri He thong Phan mem
Sinh vien: Trinh Ngoc Tuong - MSSV: DTC245200211 - STT: 54
De tai 14: He thong Quan ly Du an (Project Management)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from generate_perfect_report import create_full_report
except ImportError:
    from scripts.generate_perfect_report import create_full_report

if __name__ == '__main__':
    create_full_report()

"""
KimpTrader - Cryptocurrency Arbitrage Calculator
Copyright (C) 2024 Ji-ha-hi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import ttk
import ccxt
import pyupbit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import requests

class KimpTrader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        # 기본 설정
        self.bg_color = "#ffffff"
        self.frame_bg = "#ffffff"
        self.label_font = ("Arial", 12)
        self.price_font = ("Arial", 14, "bold")
        
        # 창 크기 설정
        self.master.geometry("1280x800")
        self.master.minsize(1200, 700)
        
        # 거래소 초기화
        self.binance = ccxt.binance()
        
        # 환율 정보
        self.exchange_rate = self.get_exchange_rate()
        
        # 데이터 저장용
        self.times = []
        self.kimps = []
        
        self.create_widgets()
        self.update_data()
    
    def create_widgets(self):
        # 메인 프레임
        self.main_frame = tk.Frame(self, bg=self.bg_color)
        self.main_frame.pack(fill="both", expand=True)
        
        # 왼쪽 프레임
        self.left_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.left_frame.pack(side=tk.LEFT, fill="both", padx=20, pady=20)
        
        # 오른쪽 프레임
        self.right_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(10,20))
        
        # 코인 선택 프레임
        coin_frame = tk.LabelFrame(self.left_frame, text="코인 선택", 
                                 font=self.label_font, bg=self.frame_bg)
        coin_frame.pack(fill="x", padx=10, pady=5)
        
        self.coin_var = tk.StringVar(value="BTC")
        coins = ["BTC", "ETH", "XRP", "SOL", "MATIC", "DOGE", "ADA", "DOT"]
        
        for coin in coins:
            tk.Radiobutton(coin_frame, text=coin, value=coin, 
                          variable=self.coin_var, font=self.label_font,
                          bg=self.frame_bg, command=self.update_data).pack(anchor="w")
        
        # 가격 정보 프레임
        price_frame = tk.LabelFrame(self.left_frame, text="실시간 가격", 
                                  font=self.label_font, bg=self.frame_bg)
        price_frame.pack(fill="x", padx=10, pady=5)
        
        # 바이낸스 가격
        binance_frame = tk.Frame(price_frame, bg=self.frame_bg)
        binance_frame.pack(fill="x", padx=5, pady=2)
        tk.Label(binance_frame, text="Binance:", font=self.label_font,
                bg=self.frame_bg).pack(side=tk.LEFT)
        self.binance_price_var = tk.StringVar(value="0")
        self.binance_label = tk.Label(binance_frame, textvariable=self.binance_price_var,
                                    font=self.price_font, bg=self.frame_bg)
        self.binance_label.pack(side=tk.LEFT, padx=5)
        self.binance_krw_var = tk.StringVar(value="(₩0)")
        self.binance_krw_label = tk.Label(binance_frame, textvariable=self.binance_krw_var,
                                    font=self.label_font, bg=self.frame_bg)
        self.binance_krw_label.pack(side=tk.LEFT)
        
        # 업비트 가격
        upbit_frame = tk.Frame(price_frame, bg=self.frame_bg)
        upbit_frame.pack(fill="x", padx=5, pady=2)
        tk.Label(upbit_frame, text="Upbit:", font=self.label_font,
                bg=self.frame_bg).pack(side=tk.LEFT)
        self.upbit_price_var = tk.StringVar(value="0")
        self.upbit_label = tk.Label(upbit_frame, textvariable=self.upbit_price_var,
                                  font=self.price_font, bg=self.frame_bg)
        self.upbit_label.pack(side=tk.LEFT, padx=5)
        
        # 김프 표시
        kimp_frame = tk.Frame(price_frame, bg=self.frame_bg)
        kimp_frame.pack(fill="x", padx=5, pady=2)
        tk.Label(kimp_frame, text="김프:", font=self.label_font,
                bg=self.frame_bg).pack(side=tk.LEFT)
        self.kimp_var = tk.StringVar(value="0%")
        self.kimp_label = tk.Label(kimp_frame, textvariable=self.kimp_var,
                                 font=self.price_font, bg=self.frame_bg)
        self.kimp_label.pack(side=tk.LEFT, padx=5)
        
        # 대시보드 프레임
        dashboard_frame = tk.LabelFrame(self.left_frame, text="대시보드", 
                                      font=self.label_font, bg=self.frame_bg)
        dashboard_frame.pack(fill="x", padx=10, pady=5)
        
        self.dashboard_label = tk.Label(dashboard_frame, text="데이터 로딩 중...",
                                      font=self.label_font, bg=self.frame_bg,
                                      justify=tk.LEFT)
        self.dashboard_label.pack(anchor="w", padx=10, pady=5)
        
        # 차트 프레임
        chart_frame = tk.LabelFrame(self.right_frame, text="김프 차트", 
                                  font=self.label_font, bg=self.frame_bg)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # 수익성 분석 프레임
        profit_frame = tk.LabelFrame(self.right_frame, text="수익성 구간 분석",
                                   font=self.label_font, bg=self.frame_bg)
        profit_frame.pack(fill="x", padx=10, pady=5)
        
        guides = [
            ("10%↑: 매우 높은 수익 구간", "#ff0000"),
            ("7~10%: 높은 수익 구간", "#ff0000"),
            ("5~7%: 중간 수익 구간", "#ff9933"),
            ("3~5%: 낮은 수익 구간", "#33cc33"),
            ("3%↓: 손실 위험 구간", "#3399ff"),
            ("0%↓: 역김프 구간", "#0066ff"),
        ]
        
        for text, color in guides:
            tk.Label(profit_frame, text=text, font=self.label_font,
                    fg=color, bg=self.frame_bg).pack(anchor="w")
        
        # 패딩 값 증가
        for widget in self.left_frame.winfo_children():
            widget.pack(fill="x", padx=20, pady=10)
        
        for widget in self.right_frame.winfo_children():
            widget.pack(fill="both", expand=True, padx=20, pady=10)
    
    def get_exchange_rate(self):
        try:
            url = "https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD"
            response = requests.get(url)
            data = response.json()
            return data[0]["basePrice"]
        except:
            return 1300  # 기본값
    
    def get_binance_price(self, coin):
        try:
            symbol = f"{coin}USDT"
            ticker = self.binance.fetch_ticker(symbol)
            return float(ticker['last'])
        except:
            return 0.0
    
    def get_upbit_price(self, coin):
        try:
            ticker = f"KRW-{coin}"
            price = pyupbit.get_current_price(ticker)
            return float(price)
        except:
            return 0.0
    
    def get_kimp_color(self, kimp):
        if kimp >= 10:
            return "#ff0000"
        elif kimp >= 7:
            return "#ff0000"
        elif kimp >= 5:
            return "#ff9933"
        elif kimp >= 3:
            return "#33cc33"
        elif kimp >= 0:
            return "#3399ff"
        else:
            return "#0066ff"
    
    def update_data(self):
        # 위젯이 유효한지 확인
        if not self.winfo_exists():
            return
            
        try:
            selected_coin = self.coin_var.get()
            
            # 가격 업데이트
            binance_price = self.get_binance_price(selected_coin)
            upbit_price = self.get_upbit_price(selected_coin)
            binance_krw = binance_price * self.exchange_rate
            
            # 위젯이 여전히 유효한지 다시 확인
            if not self.winfo_exists():
                return
                
            self.binance_price_var.set(f"${binance_price:,.2f}")
            self.binance_krw_var.set(f"(₩{binance_krw:,.0f})")
            self.upbit_price_var.set(f"₩{upbit_price:,.0f}")
            
            # 김프 계산
            kimp = ((upbit_price / (binance_price * self.exchange_rate)) - 1) * 100
            self.kimp_var.set(f"{kimp:.2f}%")
            self.kimp_label.config(fg=self.get_kimp_color(kimp))
            
            # 대시보드 업데이트
            dashboard_text = (
                f"[기본 정보]\n"
                f"• 선택 코인: {selected_coin}\n"
                f"• 환율: {self.exchange_rate:,.2f} KRW/USD\n\n"
                f"[가격 정보]\n"
                f"• 바이낸스: ${binance_price:,.2f} (₩{binance_krw:,.0f})\n"
                f"• 업비트: ₩{upbit_price:,.0f}\n"
                f"• 현재 김프: {kimp:.2f}%\n\n"
                f"[거래 정보]\n"
                f"• 예상 수수료: 0.45% + 5000원\n"
                f"• 바이낸스 → 업비트 전송가: ₩{binance_krw * 1.0045 + 5000:,.0f}\n"
                f"• 업비트 → 바이낸스 전송가: ₩{upbit_price * 0.9955 - 5000:,.0f}"
            )
            
            self.dashboard_label.config(text=dashboard_text)
            
            # 차트 업데이트
            current_time = datetime.now().strftime('%H:%M:%S')
            self.times.append(current_time)
            self.kimps.append(kimp)
            
            if len(self.times) > 30:  # 최근 30개 데이터만 표시
                self.times.pop(0)
                self.kimps.pop(0)
            
            self.ax.clear()
            self.ax.plot(self.times, self.kimps, 'b-')
            self.ax.set_title('김프 변동')
            self.ax.set_ylabel('김프 (%)')
            plt.xticks(rotation=45)
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"데이터 업데이트 오류: {e}")
        
        # 위젯이 유효할 때만 다음 업데이트 예약
        if self.winfo_exists():
            self.after(1000, self.update_data)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("KimpTrader")
    app = KimpTrader(root)
    app.pack()
    root.mainloop()
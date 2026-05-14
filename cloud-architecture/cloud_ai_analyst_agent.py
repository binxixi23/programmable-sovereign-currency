import numpy as np
import time
from sklearn.ensemble import IsolationForest

class FinancialIntelligenceAgent:
    def __init__(self):
        print("[AI AGENT] Bộ não Thám tử Tài chính Trung ương đang khởi tạo...")
        # Sử dụng thuật toán Học máy Isolation Forest để tự động tìm bất thường dòng tiền
        self.ai_model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False
        
    def train_baseline_behavior(self, historical_flows: list):
        """
        Huấn luyện AI hiểu thế nào là dòng tiền mặt giao dịch HỢP PHÁP của người dân.
        Mỗi luồng gồm: [Số lượng tờ tiền, Khoảng cách di chuyển (km), Thời gian giao dịch (giờ trong ngày)]
        """
        print("[AI AGENT] Đang nạp dữ liệu lịch sử để học hành vi tiêu dùng hợp pháp...")
        X = np.array(historical_flows)
        self.ai_model.fit(X)
        self.is_trained = True
        print("[AI AGENT] Huấn luyện hoàn tất. Hệ thống bắt đầu giám sát tự động toàn quốc.")

    def analyze_live_cash_flow(self, volume: int, distance_km: float, hour_of_day: int) -> dict:
        """
        Phân tích thời gian thực một luồng tiền mặt di chuyển được quét từ Đám mây.
        """
        if not self.is_trained:
            return {"action": "ALLOW", "reason": "AI Model not trained yet."}

        current_flow = np.array([[volume, distance_km, hour_of_day]])
        # Dự đoán: 1 là bình thường, -1 là hành vi kinh tế ngầm bất thường
        prediction = self.ai_model.predict(current_flow)[0]

        if prediction == -1:
            # Nếu phát hiện bất thường, AI tự động phân loại rủi ro để đưa ra hành động
            return self._dispatch_autonomous_action(volume, distance_km, hour_of_day)
            
        return {"action": "ALLOW", "reason": "Giao dịch nằm trong mô hình chi tiêu an toàn của người dân."}

    def _dispatch_autonomous_action(self, volume: int, distance_km: float, hour_of_day: int) -> dict:
        """
        HÀNH ĐỘNG TỰ HÀNH: AI tự đưa ra quyết định xử lý và điều phối các lực lượng chức năng.
        """
        # Kịch bản 1: Lượng tiền rất lớn di chuyển vào ban đêm gần biên giới -> Rửa tiền/Chuyển lậu
        if hour_of_day >= 23 or hour_of_day <= 4:
            return {
                "action": "INTERCEPT_AND_LOCK",
                "risk_level": "CRITICAL",
                "reason": f"Phát hiện dấu hiệu RỬA TIỀN vĩ mô. Gom lô {volume} tờ tiền chạy ngầm ban đêm.",
                "autonomous_execution": [
                    "Kích hoạt chặn Geofencing khóa cứng giá trị cọc tiền",
                    "Bắn tọa độ GPS của máy quét biên giới về Đội tuần tra Hải quan gần nhất"
                ]
            }
        
        # Kịch bản 2: Tiền di chuyển đột ngột không rõ nguồn gốc thương mại -> Nghi vấn Hối lộ / Trốn thuế
        if volume >= 10000: # Ví dụ: Cọc $1,000,000 (10,000 tờ $100)
            return {
                "action": "FLAG_FOR_AUDIT",
                "risk_level": "HIGH",
                "reason": "Phát hiện mô hình dòng tiền có dấu hiệu TRỐN THUẾ hoặc NHẬN HỐI LỘ quy mô lớn.",
                "autonomous_execution": [
                    "Tự động xuất lệnh kiểm toán điện tử gửi sang Cục Thuế",
                    "Gửi yêu cầu rà soát camera an ninh tại vị trí máy quét phát hiện"
                ]
            }

        return {
            "action": "MONITOR",
            "risk_level": "MEDIUM",
            "reason": "Dòng chảy sai lệch nhẹ so với thói quen khu vực. Tiếp tục giám sát ngầm.",
            "autonomous_execution": ["Tăng tần suất quét định vị của lô seri này"]
        }

# ==========================================
# KỊCH BẢN CHẠY THỬ NGHIỆM AI AGENT (MÔ PHỎNG)
# ==========================================
if __name__ == "__main__":
    agent = FinancialIntelligenceAgent()

    # Giả lập 100 giao dịch bình thường của người dân:
    # Người dân thường tiêu ít tiền (1-20 tờ), đi chợ gần (1-5km), mua ban ngày (8h - 20h)
    normal_flows = []
    for _ in range(100):
        normal_flows.append([np.random.randint(1, 20), np.random.uniform(0.5, 5.0), np.random.randint(8, 20)])
        
    # Huấn luyện AI với thói quen sạch này
    agent.train_baseline_behavior(normal_flows)

    print("\n" + "="*50 + "\n[GIÁM SÁT SỐNG] AI BẮT ĐẦU QUÉT DÒNG CHẢY TOÀN QUỐC\n" + "="*50)

    # Tình huống 1: Người dân đi siêu thị mua đồ ban ngày
    tx1 = agent.analyze_live_cash_flow(volume=5, distance_km=2.3, hour_of_day=14)
    print(f"Sự kiện 1: {tx1['reason']} -> HÀNH ĐỘNG AI: {tx1['action']}\n")

    # Tình huống 2: Tội phạm ôm vali tiền lớn đổi địa điểm lúc 2 giờ sáng tại cửa khẩu
    tx2 = agent.analyze_live_cash_flow(volume=8000, distance_km=45.0, hour_of_day=2)
    print(f"💥 Sự kiện 2 (BẤT THƯỜNG): {tx2['reason']}")
    print(f"-> Mức độ rủi ro: {tx2['risk_level']}")
    print(f"-> Quyết định tự hành của AI Agent: {tx2['action']}")
    print(f"-> Lệnh thực thi hệ thống:")
    for step in tx2['autonomous_execution']:
        print(f"   [+] {step}")

import pandas as pd

def main():
    # 1. Đọc file kết quả
    df = pd.read_parquet(r"data\results\local_metric_results.parquet")

    # 2. Cập nhật lại tên cột chuẩn theo dữ liệu thực tế của bạn
    report_cols = [
        'question_id', 
        'evaluation_mode',
        'latency_ms', 
        'estimated_cost_usd',
        'true_hit_rate_at_k',
        'mrr_at_k',          # Tên cột thực tế
        'precision_at_k',    # Tên cột thực tế
        'recall_at_k',       # Tên cột thực tế
    ]

    # Kiểm tra xem các cột này có thực sự tồn tại không trước khi lọc
    available_cols = [c for c in report_cols if c in df.columns]
    
    # 3. Lấy 10 dòng đầu tiên
    report_df = df[available_cols].head(10)

    # 4. Làm tròn số cho đẹp
    report_df = report_df.round(4)

    # 5. Xuất ra Markdown
    print("\n--- BÁO CÁO KẾT QUẢ PHASE 2 ---\n")
    print(report_df.to_markdown(index=False))

if __name__ == "__main__":
    main()
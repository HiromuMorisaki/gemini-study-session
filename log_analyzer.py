import os
import random
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Iterator, Dict, List, Tuple

LOG_FILE = "access.log"

def generate_dummy_log(file_path: str, num_lines: int = 100) -> None:
    """
    指定されたファイルパスにダミーのログファイルを生成します。

    Args:
        file_path (str): 生成するログファイルのパス。
        num_lines (int, optional): 生成するログの行数。デフォルトは100。
    """
    levels = ["INFO", "WARN", "ERROR"]
    error_msgs = [
        "Connection timeout",
        "Database locked",
        "Null pointer exception",
        "Out of memory",
        "Unauthorized access"
    ]
    general_msgs = [
        "User logged in",
        "Job completed",
        "Request processed",
        "Cache cleared"
    ]

    base_time = datetime.now() - timedelta(days=1)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(num_lines):
            # ランダムな時間を生成（過去24時間以内）
            log_time = base_time + timedelta(minutes=random.randint(0, 1440))
            level = random.choices(levels, weights=[60, 20, 20])[0]
            
            if level == "ERROR":
                message = random.choice(error_msgs)
            else:
                message = random.choice(general_msgs)
                
            log_line = f"{log_time.strftime('%Y-%m-%d %H:%M:%S')} [{level}] {message}\n"
            f.write(log_line)

def parse_logs(file_path: str) -> Iterator[Tuple[datetime, str, str]]:
    """
    ログファイルを読み込み、パースした結果をジェネレータとして返します。

    Args:
        file_path (str): 読み込むログファイルのパス。

    Yields:
        Tuple[datetime, str, str]: (日時, ログレベル, メッセージ) のタプル。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split("] ")
            if len(parts) != 2:
                continue
                
            time_level_str = parts[0]
            message = parts[1]
            
            # "YYYY-MM-DD HH:MM:SS [LEVEL" を分割
            time_str, level_str = time_level_str.split(" [")
            
            try:
                log_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                yield log_time, level_str, message
            except ValueError:
                continue

def analyze_error_logs(log_generator: Iterator[Tuple[datetime, str, str]]) -> Dict[str, Any]:
    """
    ERRORレベルのログを抽出して集計します。

    Args:
        log_generator (Iterator[Tuple[datetime, str, str]]): パースされたログのジェネレータ。

    Returns:
        Dict[str, Any]: エラーメッセージごとの集計と、時間帯ごとの集計結果を含む辞書。
    """
    error_counts: Counter = Counter()
    hourly_trends: Counter = Counter()

    for log_time, level, message in log_generator:
        if level == "ERROR":
            error_counts[message] += 1
            hourly_trends[log_time.hour] += 1

    return {
        "error_counts": error_counts,
        "hourly_trends": hourly_trends
    }

def print_markdown_table(headers: List[str], rows: List[List[str]]) -> None:
    """
    データをMarkdown風の表形式でコンソールに出力します。

    Args:
        headers (List[str]): 表のヘッダー要素のリスト。
        rows (List[List[str]]): 表の各行のデータを含むリスト。
    """
    # 各列の最大幅を計算
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
    
    def format_row(row: List[str]) -> str:
        return "| " + " | ".join(str(item).ljust(width) for item, width in zip(row, col_widths)) + " |"

    print(format_row(headers))
    print("|" + "|".join("-" * (width + 2) for width in col_widths) + "|")
    
    for row in rows:
        print(format_row(row))
    print()

def main() -> None:
    """
    メインの実行関数。ファイルの準備、解析、出力を行います。
    """
    if not os.path.exists(LOG_FILE):
        print(f"[{LOG_FILE}] が見つからないため、ダミーデータを生成します...\n")
        generate_dummy_log(LOG_FILE, num_lines=150)

    # ログのパースと解析
    logs = parse_logs(LOG_FILE)
    analysis_result = analyze_error_logs(logs)

    error_counts = analysis_result["error_counts"]
    hourly_trends = analysis_result["hourly_trends"]

    # 1. エラー種類ごとの集計結果を出力
    print("### エラー種類ごとの発生回数\n")
    if error_counts:
        headers_errors = ["Error Message", "Count"]
        rows_errors = [[msg, str(count)] for msg, count in error_counts.most_common()]
        print_markdown_table(headers_errors, rows_errors)
    else:
        print("ERRORログは検出されませんでした。\n")

    # 2. 時間帯ごとの集計結果を出力
    print("### 発生時間帯（1時間単位）の傾向\n")
    if hourly_trends:
        headers_hours = ["Hour", "Error Count"]
        # 0時から23時までソートして表示
        rows_hours = [[f"{hour:02d}:00 - {hour:02d}:59", str(hourly_trends[hour])] for hour in sorted(hourly_trends.keys())]
        print_markdown_table(headers_hours, rows_hours)
    else:
        print("ERRORログは検出されませんでした。\n")

if __name__ == "__main__":
    main()

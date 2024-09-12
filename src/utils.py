import sys

def progress_bar(progress, total, length=30):
    percent = int((progress / total) * 100)
    bar_length = int((progress / total) * length)
    bar = f"[{'#' * bar_length}{'.' * (length - bar_length)}] {percent}%"
    return bar
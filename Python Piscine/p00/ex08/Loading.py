import time
import shutil

PROGRESS_LEN = shutil.get_terminal_size().columns - 30


def formatTime(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{int(s):02d}"


def ft_tqdm(lst) -> None:
    total = len(lst)
    start_time = time.time()
    progressBarWidth = PROGRESS_LEN - 10
    for i, item in enumerate(lst, start=1):
        progress = int(i / total * progressBarWidth)
        elapsed_time = time.time() - start_time
        speed = (i / elapsed_time) if elapsed_time != 0.0 else 0.0
        eta = (total - i) / speed if speed != 0 else 0

        elapsed_formatted = formatTime(elapsed_time)
        eta_formatted = formatTime(eta)

        progress_bar = f"|{'█' * progress:<{progressBarWidth}}|"
        progressPercentage = progress * 100 // progressBarWidth
        progressInfo = f"{progressPercentage}%{progress_bar} {i}/{total}"
        timeInfo = f"[{elapsed_formatted}<{eta_formatted}, {speed:.2f}it/s]"

        print(f"\r{progressInfo} {timeInfo}", end="", flush=True)
        yield item

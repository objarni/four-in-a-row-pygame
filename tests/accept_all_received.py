from pathlib import Path


def run():
    for received in Path(__file__).parent.glob("*.received.txt"):
        approved = Path(str(received).replace(".received.", ".approved."))
        print(f"r:{received}\n\ta:{approved}")
        approved.write_text(received.read_text(encoding='utf8'), encoding='utf8')


if __name__ == '__main__':
    run()

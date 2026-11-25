"""Record one live run for replay: python3 record.py "question" "4 label"  ->  replays/4 label.json"""
import json, pathlib, sys
import stability

rec = stability.check(sys.argv[1])
out = pathlib.Path(__file__).parent / "replays" / f"{sys.argv[2]}.json"
out.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
print(out, rec["outcome"])

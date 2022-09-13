bash scripts/sbv2tsv.sh
python3 scripts/tsv_added_fields.py
python3 scripts/test_clip_duration.py
rm caption.tsv

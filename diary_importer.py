"""
Universal School Diary Importer & Converter for Tharun (Class 8)
Supports: Word (.docx, .doc), PDF (.pdf), Images (.jpg, .jpeg, .png), Text (.txt), and JSON (.json)
Converts any format into structured JSON style format (tharun_diary_format.json)
"""

import os
import re
import json
import asyncio
from datetime import datetime

# Optional imports for various document formats
try:
    import docx
except ImportError:
    docx = None

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    from PIL import Image, ImageEnhance, ImageOps, ImageFilter
    import winocr
except ImportError:
    winocr = None
    Image = None


SUBJECT_PATTERNS = [
    {
        "name": "Biology", "code": "Bio",
        "prefix_regex": r"^(bio|biology)$",
        "regex": r"\b(biology|cell|microorganism|lab manual)\b"
    },
    {
        "name": "Physics", "code": "Phy",
        "prefix_regex": r"^(phy|physics)$",
        "regex": r"\b(physics|force|pressure|sound|friction|d\.n)\b"
    },
    {
        "name": "Chemistry", "code": "Chem",
        "prefix_regex": r"^(chem|chemistry)$",
        "regex": r"\b(chemistry|revision zone|reaction|combustion|metal)\b"
    },
    {
        "name": "Science", "code": "Sci",
        "prefix_regex": r"^(sci|science)$",
        "regex": r"\b(science|diagram)\b"
    },
    {
        "name": "History", "code": "His",
        "prefix_regex": r"^(his|history)$",
        "regex": r"\b(history|timeline|period|modern|tribal)\b"
    },
    {
        "name": "Geography", "code": "Geo",
        "prefix_regex": r"^(geo|geography)$",
        "regex": r"\b(geography|resources|activity|agriculture|minerals)\b"
    },
    {
        "name": "Social Science", "code": "SST",
        "prefix_regex": r"^(sst|social|civics|civ)$",
        "regex": r"\b(social science|civics|judiciary|constitution|parliament)\b"
    },
    {
        "name": "Tamil", "code": "தமிழ்",
        "prefix_regex": r"^(tamil|tam|தமிழ்)$",
        "regex": r"(தமிழ்|tamil|இயல்|குருவினா|சிறுவினா|பாடம்|வினா)"
    },
    {
        "name": "English", "code": "Eng",
        "prefix_regex": r"^(eng|english)$",
        "regex": r"\b(english|grammar|tenses|prose|poem|comprehension|diary entry)\b"
    },
    {
        "name": "Hindi", "code": "Hindi",
        "prefix_regex": r"^(hindi|hin|हिंदी)$",
        "regex": r"(हिंदी|hindi|व्याकरण|पाठ|वर्तनी|वसंत)"
    },
    {
        "name": "Mathematics", "code": "Math",
        "prefix_regex": r"^(math|maths|mathematics|mat)$",
        "regex": r"\b(mathematics|maths|math|algebra|geometry|ch-\d+|ex-[\d\.]+)\b"
    },
    {
        "name": "Computer Science", "code": "CS",
        "prefix_regex": r"^(cs|computer|comp)$",
        "regex": r"\b(computer|coding|python|scratch|it)\b"
    },
    {
        "name": "Handwriting & Language Clinic", "code": "Lang",
        "prefix_regex": r"^(handwriting|handwrite|hand\s*write|hw)$",
        "regex": r"\b(handwriting|handwrite|cursive|speed writing)\b"
    }
]


class UniversalDiaryImporter:
    """
    Extracts diary homework text from Word, PDF, Images, Text, or JSON,
    parses subjects and activities, and returns standard JSON structure.
    """

    @classmethod
    def extract_text_from_file(cls, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        extracted_lines = []

        # 1. JSON File (Direct format)
        if ext == ".json":
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return "JSON_DIRECT", data

        # 2. Word Document (.docx)
        elif ext in [".docx", ".doc"]:
            if docx:
                try:
                    doc = docx.Document(filepath)
                    for p in doc.paragraphs:
                        text = p.text.strip()
                        if text:
                            extracted_lines.append(text)
                    for table in doc.tables:
                        for row in table.rows:
                            row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                            if row_text:
                                extracted_lines.append(row_text)
                except Exception as e:
                    extracted_lines.append(f"Word read error: {e}")
            else:
                extracted_lines.append("python-docx not installed.")

        # 3. PDF Document (.pdf)
        elif ext == ".pdf":
            if pypdf:
                try:
                    reader = pypdf.PdfReader(filepath)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            for line in text.splitlines():
                                if line.strip():
                                    extracted_lines.append(line.strip())
                except Exception as e:
                    extracted_lines.append(f"PDF read error: {e}")
            else:
                extracted_lines.append("pypdf not installed.")

        # 4. Images (.jpg, .jpeg, .png, .bmp) via Windows Native OCR
        elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
            if winocr and Image:
                try:
                    orig = Image.open(filepath)
                    best_lines = []
                    candidates = []
                    # Try 0, 90, 270 rotations
                    for rot in [0, 90, 270]:
                        test_img = orig if rot == 0 else orig.rotate(rot, expand=True)
                        candidates.append(test_img)
                        # Also add contrast enhanced + grayscale version
                        try:
                            gray = ImageOps.grayscale(test_img)
                            enhancer = ImageEnhance.Contrast(gray)
                            high_c = enhancer.enhance(2.0)
                            candidates.append(high_c)
                        except Exception:
                            pass

                    for cand in candidates:
                        res = asyncio.run(winocr.recognize_pil(cand))
                        lines = [l.text.strip() for l in res.lines if l.text.strip()]
                        if len(lines) > len(best_lines):
                            best_lines = lines
                    extracted_lines = best_lines
                except Exception as e:
                    extracted_lines.append(f"Image OCR error: {e}")
            else:
                extracted_lines.append("OCR engine (winocr/PIL) not available.")

            raw_text = "\n".join(extracted_lines)
            return "IMAGE_PHOTO", raw_text

        # 5. Plain Text / CSV (.txt, .csv)
        else:
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.strip():
                            extracted_lines.append(line.strip())
            except Exception as e:
                extracted_lines.append(f"Text read error: {e}")

        raw_text = "\n".join(extracted_lines)
        return "TEXT", raw_text

    @classmethod
    def parse_text_to_json_diary(cls, raw_text, default_date=None):
        if not default_date:
            default_date = datetime.now().strftime("%Y-%m-%d")

        # Find all date matches: e.g. "06/10/26", "07/10/2026", "DATE : 06-10-26"
        date_pattern = r'(?:DATE\s*[:;\-\.]*\s*)?(\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b)'
        matches = list(re.finditer(date_pattern, raw_text, re.IGNORECASE))

        date_chunks = []
        if not matches:
            date_chunks.append((default_date, raw_text))
        else:
            for i, m in enumerate(matches):
                d_raw = m.group(1)
                start = m.start()
                end = matches[i+1].start() if i+1 < len(matches) else len(raw_text)
                chunk = raw_text[start:end]
                date_chunks.append((d_raw, chunk))

        # Group and parse by standardized ISO date
        entries_by_date = {}

        for d_raw, chunk in date_chunks:
            iso_date = default_date
            disp_date = datetime.strptime(default_date, "%Y-%m-%d").strftime("%d/%m/%Y")

            d_parts = re.split(r'[\/\-\.]', d_raw)
            if len(d_parts) == 3:
                if len(d_parts[0]) == 4:
                    # YYYY-MM-DD or YYYY/MM/DD
                    y, mo, d = d_parts[0], d_parts[1], d_parts[2]
                else:
                    # DD-MM-YYYY or DD/MM/YY
                    d, mo, y = d_parts[0], d_parts[1], d_parts[2]
                    if len(y) == 2:
                        y = "20" + y
                try:
                    dt = datetime(int(y), int(mo), int(d))
                    iso_date = dt.strftime("%Y-%m-%d")
                    disp_date = dt.strftime("%d/%m/%Y")
                except Exception:
                    pass

            if iso_date not in entries_by_date:
                entries_by_date[iso_date] = {
                    "date": iso_date,
                    "display_date": disp_date,
                    "efficiency_split_core": True,
                    "items": []
                }

            lines = chunk.splitlines()
            for line in lines:
                line_str = line.strip()
                if not line_str or len(line_str) < 3:
                    continue

                # Ignore diary headers
                if any(h in line_str.upper() for h in [
                    "SENTHIL PUBLIC SCHOOL", "STUDENT'S HANDBOOK", "DAILY ACTIVITIES",
                    "TEACHER'S SIGNATURE", "PARENT'S SIGNATURE", "MESSAGE", "REMARKS"
                ]):
                    continue

                # Skip standalone date header lines like "DATE : 06/10/26"
                if re.match(r'^(?:DATE\s*[:;\-\.]*\s*)?\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b$', line_str, re.IGNORECASE):
                    continue

                # Match subject
                matched_sub = None
                clean_task = line_str
                match_source = "keyword"

                # 1. Try explicit leading prefix: e.g. "Math: ...", "Bio - ...", "தமிழ்: ..."
                prefix_match = re.match(r"^\s*([A-Za-z\u0B80-\u0BFF\u0900-\u097F]+)[\s:\-\|\.]+\s*(.*)$", line_str)
                if prefix_match:
                    cand_pfx = prefix_match.group(1).lower()
                    rem = prefix_match.group(2).strip()
                    for spat in SUBJECT_PATTERNS:
                        if re.search(spat["prefix_regex"], cand_pfx, re.IGNORECASE):
                            matched_sub = spat
                            clean_task = rem if rem else line_str
                            match_source = f"Prefix '{cand_pfx}:'"
                            break

                # 2. If no leading prefix matched, try keyword scan across the whole line
                if not matched_sub:
                    for spat in SUBJECT_PATTERNS:
                        if re.search(spat["regex"], line_str, re.IGNORECASE):
                            matched_sub = spat
                            clean_task = re.sub(r"^" + spat["prefix_regex"] + r"[\s:\-\|\.]*", "", line_str, flags=re.IGNORECASE).strip()
                            if not clean_task:
                                clean_task = line_str
                            match_source = "Keyword in line"
                            break

                if matched_sub:
                    clean_task = clean_task.lstrip(":-| \t")
                    if not clean_task:
                        clean_task = line_str

                    # Determine task type
                    ttype = "written"
                    est_mins = 25
                    reason = "Written exercise / problem solving"
                    line_lower = line_str.lower()

                    if "lab manual" in line_lower or "bring" in line_lower:
                        ttype = "bag_pack"
                        est_mins = 5
                        reason = "School bag equipment / lab manual reminder"
                    elif "read" in line_lower or "pg no" in line_lower:
                        ttype = "reading"
                        est_mins = 15
                        reason = "Textbook page reading & review"
                    elif "learn" in line_lower or "memorize" in line_lower or "d.n" in line_lower:
                        ttype = "memorize"
                        est_mins = 20
                        reason = "Concept memorization & active recall"
                    elif "activity" in line_lower or "map" in line_lower:
                        ttype = "activity"
                        est_mins = 20
                        reason = "Practical activity / diagram"
                    elif "math" in matched_sub["name"].lower() or "ch-" in line_lower:
                        ttype = "written"
                        est_mins = 30
                        reason = "Mathematics problem solving practice"

                    entries_by_date[iso_date]["items"].append({
                        "subject": matched_sub["name"],
                        "code": matched_sub["code"],
                        "task": clean_task,
                        "task_type": ttype,
                        "est_mins": est_mins,
                        "completed": False,
                        "raw_source": line_str,
                        "match_source": match_source,
                        "categorization_reason": reason
                    })

        result_entries = list(entries_by_date.values())
        for entry in result_entries:
            if not entry["items"]:
                entry["items"].append({
                    "subject": "General Homework",
                    "code": "HW",
                    "task": "Review daily school notes",
                    "task_type": "reading",
                    "est_mins": 20,
                    "completed": False,
                    "raw_source": "General diary review",
                    "match_source": "Default",
                    "categorization_reason": "No specific subject detected"
                })

        return result_entries

    @classmethod
    def convert_any_file_to_json(cls, filepath, output_json_path=None):
        """
        Reads Word / PDF / Image / Text, parses all dates and logs, and updates/merges into JSON format.
        """
        mode, data = cls.extract_text_from_file(filepath)

        if mode == "JSON_DIRECT":
            if isinstance(data, dict) and "diary_entries" in data:
                parsed_entries = data["diary_entries"]
            elif isinstance(data, list):
                parsed_entries = data
            else:
                parsed_entries = [data]
            raw_text = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            raw_text = data
            # Check filename for date fallback (e.g. 08-10-2026_diary.jpg)
            fn = os.path.basename(filepath)
            fn_date_match = re.search(r'(\b\d{1,2}[\/\-\._]\d{1,2}[\/\-\._]\d{2,4}\b)', fn)
            default_d = None
            if fn_date_match:
                d_raw = fn_date_match.group(1).replace('_', '-')
                d_parts = re.split(r'[\/\-\.]', d_raw)
                if len(d_parts) == 3:
                    if len(d_parts[0]) == 4:
                        y, mo, d = d_parts[0], d_parts[1], d_parts[2]
                    else:
                        d, mo, y = d_parts[0], d_parts[1], d_parts[2]
                        if len(y) == 2:
                            y = "20" + y
                    try:
                        default_d = f"{y}-{int(mo):02d}-{int(d):02d}"
                    except Exception:
                        pass
            parsed_entries = cls.parse_text_to_json_diary(raw_text, default_date=default_d)

        # Merge into master JSON file if exists
        target_file = output_json_path or "tharun_diary_format.json"
        master_data = {
            "student_name": "Tharun",
            "school": "Senthil Public School",
            "format_version": "1.0",
            "description": "Tharun's Official School Diary Homework Entries - Max 1-2 Timetable Slots per Day",
            "diary_entries": []
        }

        if os.path.exists(target_file):
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    master_data = json.load(f)
            except Exception:
                pass

        # Merge or update every parsed date entry
        for p_entry in parsed_entries:
            existing = False
            for idx, entry in enumerate(master_data.get("diary_entries", [])):
                if entry.get("date") == p_entry.get("date"):
                    master_data["diary_entries"][idx] = p_entry
                    existing = True
                    break
            if not existing:
                master_data.setdefault("diary_entries", []).append(p_entry)

        # Sort dates ascending
        master_data["diary_entries"].sort(key=lambda x: x.get("date", ""))

        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(master_data, f, indent=2, ensure_ascii=False)

        return parsed_entries, master_data, raw_text

    @classmethod
    def convert_multiple_files_to_json(cls, filepath_list, output_json_path=None):
        """
        Processes a list of files (Word/PDF/Photos/Text/JSON) and merges all entries into output_json_path.
        """
        all_parsed = []
        combined_raw = []
        processed_files = []
        errors = []

        for fp in filepath_list:
            if not os.path.exists(fp):
                continue
            try:
                p_entries, master_data, raw_text = cls.convert_any_file_to_json(fp, output_json_path)
                all_parsed.extend(p_entries)
                combined_raw.append(f"=== File: {os.path.basename(fp)} ===\n{raw_text}")
                processed_files.append(fp)
            except Exception as e:
                errors.append(f"{os.path.basename(fp)}: {e}")

        # Final master data read
        target_file = output_json_path or "tharun_diary_format.json"
        master_data = {"diary_entries": []}
        if os.path.exists(target_file):
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    master_data = json.load(f)
            except Exception:
                pass

        return all_parsed, master_data, "\n\n".join(combined_raw), processed_files, errors

    @classmethod
    def convert_folder_to_json(cls, folder_path, output_json_path=None):
        """
        Scans a folder for all supported diary files (.docx, .doc, .pdf, .jpg, .jpeg, .png, .bmp, .txt, .json)
        and converts/merges them all into the structured diary JSON format.
        """
        valid_exts = {".docx", ".doc", ".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".txt", ".json", ".md"}
        if not os.path.isdir(folder_path):
            raise ValueError(f"Path is not a valid folder: {folder_path}")

        files_to_process = []
        for root_dir, _, filenames in os.walk(folder_path):
            for fn in filenames:
                ext = os.path.splitext(fn)[1].lower()
                target_bn = os.path.basename(output_json_path or "tharun_diary_format.json")
                if ext in valid_exts and not fn.startswith("~") and not fn.startswith(".") and fn != target_bn:
                    files_to_process.append(os.path.join(root_dir, fn))

        files_to_process.sort()
        return cls.convert_multiple_files_to_json(files_to_process, output_json_path)


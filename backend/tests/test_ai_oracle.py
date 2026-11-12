import asyncio
from pathlib import Path
from PIL import Image
from app.services.ai_oracle import ai_oracle
from app.config import settings

def setup_module():
    upload_dir = Path(settings.UPLOAD_FOLDER)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Compliant image with visual contrast and details
    img = Image.new('RGB', (400, 300), color=(30, 41, 59))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([(30, 30), (370, 270)], outline=(16, 185, 129), width=3, fill=(15, 23, 42))
    draw.text((50, 50), "COMPLIANT DELIVERABLE UNIT", fill=(255, 255, 255))
    draw.rectangle([(60, 100), (200, 200)], outline=(59, 130, 246), width=2, fill=(30, 60, 90))
    img.save(upload_dir / "test_compliant.jpg")
    
    fail_img = Image.new('RGB', (400, 300), color=(150, 50, 50))
    draw_fail = ImageDraw.Draw(fail_img)
    draw_fail.rectangle([(30, 30), (370, 270)], outline=(239, 68, 68), width=3, fill=(60, 10, 10))
    fail_img.save(upload_dir / "test_fail_wiring.jpg")
    
    # Blurry / tiny image
    tiny_img = Image.new('RGB', (50, 50), color=(0, 0, 0))
    tiny_img.save(upload_dir / "test_tiny_blurry.jpg")
    
    # Corrupt non-image file
    with open(upload_dir / "test_corrupt.jpg", "wb") as f:
        f.write(b"NOT_A_VALID_IMAGE_HEADER_DATA_123456789")

def test_ai_oracle_pass_evaluation():
    img_path = str(Path(settings.UPLOAD_FOLDER) / "test_compliant.jpg")
    specs = [
        "Capacitor securely mounted",
        "Manifold gauge reading between 60-70 PSI"
    ]
    verdict = asyncio.run(ai_oracle.evaluate_deliverable(
        milestone_title="HVAC Maintenance",
        milestone_description="Replace capacitor and calibrate pressure",
        specifications=specs,
        file_path=img_path,
        file_hash="dummy_hash_123456"
    ))
    assert verdict.confidence_score >= 85
    assert verdict.verdict == "PASS"
    assert len(verdict.criteria_checklist) == 2
    assert all(c.satisfied for c in verdict.criteria_checklist)

def test_ai_oracle_fail_evaluation():
    img_path = str(Path(settings.UPLOAD_FOLDER) / "test_fail_wiring.jpg")
    specs = [
        "Ground continuity verified",
        "No exposed wires"
    ]
    verdict = asyncio.run(ai_oracle.evaluate_deliverable(
        milestone_title="Electrical Subpanel",
        milestone_description="Inspection of wiring",
        specifications=specs,
        file_path=img_path,
        file_hash="dummy_fail_hash"
    ))
    assert verdict.confidence_score < 60
    assert verdict.verdict == "FAIL"
    assert verdict.fraud_risk_score > 50

def test_ai_oracle_corrupt_file_evaluation():
    img_path = str(Path(settings.UPLOAD_FOLDER) / "test_corrupt.jpg")
    specs = ["Capacitor replaced", "Pressure calibrated"]
    verdict = asyncio.run(ai_oracle.evaluate_deliverable(
        milestone_title="HVAC Maintenance",
        milestone_description="Replace capacitor",
        specifications=specs,
        file_path=img_path,
        file_hash="corrupt_hash_999"
    ))
    assert verdict.confidence_score == 0
    assert verdict.verdict == "FAIL"
    assert verdict.fraud_risk_score == 100
    assert all(not c.satisfied for c in verdict.criteria_checklist)
    assert len(verdict.visual_anomalies) > 0

def test_ai_oracle_clarity_failure_evaluation():
    img_path = str(Path(settings.UPLOAD_FOLDER) / "test_tiny_blurry.jpg")
    specs = ["Wiring intact", "Multimeter reading valid"]
    verdict = asyncio.run(ai_oracle.evaluate_deliverable(
        milestone_title="Electrical Subpanel",
        milestone_description="Verify subpanel",
        specifications=specs,
        file_path=img_path,
        file_hash="tiny_hash_888"
    ))
    assert verdict.confidence_score <= 25
    assert verdict.verdict == "FAIL"
    assert verdict.fraud_risk_score >= 80

def test_ai_oracle_needs_review_evaluation():
    img_path = str(Path(settings.UPLOAD_FOLDER) / "test_compliant.jpg")
    specs = ["Capacitor installed", "Calibration complete", "Secondary seal applied"]
    verdict = asyncio.run(ai_oracle.evaluate_deliverable(
        milestone_title="HVAC Partial",
        milestone_description="Partial inspection",
        specifications=specs,
        file_path=img_path,
        file_hash="partial_hash_777",
        contractor_notes="Job is 90% done, final seal is incomplete pending dry time"
    ))
    assert verdict.verdict == "NEEDS_REVIEW"
    assert 60 <= verdict.confidence_score <= 84

import asyncio
import os
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

async def record_full_demo():
    output_dir = Path(r"c:\Users\Srishanth S\Desktop\Sri folder\PayPal AI Hackathon\demo_recording")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_dir = output_dir / "temp_video_full"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("Launching Playwright for full 2:45 - 2:55 demo recording...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--disable-infobars"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(temp_dir),
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        async def pause(seconds):
            await page.wait_for_timeout(seconds * 1000)

        # ------------------------------------------------------------------
        # SCENE 1: Introduction & Client Escrow Dashboard (0:00 - 0:25) ~25s
        # ------------------------------------------------------------------
        print("[Scene 1] Dashboard Overview & Architecture (25s)...")
        await page.goto("http://localhost:8000")
        await page.wait_for_load_state("networkidle")
        await pause(6)

        # Hover over Top Ribbon and PayPal status badge
        await page.mouse.move(960, 25)
        await pause(3)
        await page.mouse.move(1450, 70)
        await pause(3)

        # Smooth scrolling through all 3 milestone states
        print("[Scene 1] Scrolling across contract cards...")
        await page.mouse.wheel(0, 350)
        await pause(4)
        await page.mouse.wheel(0, 350)
        await pause(5)
        await page.mouse.wheel(0, -700)
        await pause(4)

        # ------------------------------------------------------------------
        # SCENE 2: Template Creation & Specifications (0:25 - 0:55) ~30s
        # ------------------------------------------------------------------
        print("[Scene 2] Milestone Creation & Contract Specifications (30s)...")
        create_btn = page.locator("button:has-text('+ New Milestone')").first
        if await create_btn.is_visible():
            await create_btn.hover()
            await pause(2)
            await create_btn.click()
            await pause(4)

            # Choose template
            hvac_template = page.locator("button:has-text('HVAC Capacitor & Calibration')").first
            if await hvac_template.is_visible():
                await hvac_template.hover()
                await pause(2)
                await hvac_template.click()
                await pause(5)

            # Highlight the AI specifications
            await page.mouse.wheel(0, 250)
            await pause(5)
            await page.mouse.wheel(0, -250)
            await pause(3)

            # Submit milestone
            submit_create = page.locator("button:has-text('Create Escrow Milestone')").first
            if await submit_create.is_visible():
                await submit_create.hover()
                await pause(2)
                await submit_create.click()
                await pause(7)

        # ------------------------------------------------------------------
        # SCENE 3: PayPal Authorization Hold Flow (0:55 - 1:15) ~20s
        # ------------------------------------------------------------------
        print("[Scene 3] Inspecting PayPal Escrow Status (20s)...")
        # Find the newly created or draft milestone
        lock_btn = page.locator("button:has-text('Lock Escrow'), button:has-text('Authorize')").first
        if await lock_btn.is_visible():
            await lock_btn.hover()
            await pause(3)
            await lock_btn.click()
            await pause(6)

            # Close modal if open
            close_paypal = page.locator("button:has-text('Close'), button:has(svg.lucide-x)").first
            if await close_paypal.is_visible():
                await close_paypal.click()
                await pause(3)
        else:
            await pause(8)

        # ------------------------------------------------------------------
        # SCENE 4: Contractor Proof View (1:15 - 1:35) ~20s
        # ------------------------------------------------------------------
        print("[Scene 4] Contractor View & Spec Inspection (20s)...")
        contractor_tab = page.locator("button:has-text('Contractor & AI Scanner'), button:has-text('AI Scanner')").first
        await contractor_tab.hover()
        await pause(2)
        await contractor_tab.click()
        await pause(6)

        # Examine requirements panel
        await page.mouse.wheel(0, 200)
        await pause(5)
        await page.mouse.wheel(0, -200)
        await pause(4)

        # ------------------------------------------------------------------
        # SCENE 5: AI Multimodal Verification & Auto-Capture (1:35 - 2:05) ~30s
        # ------------------------------------------------------------------
        print("[Scene 5] Submitting Deliverable & Autonomous AI Scan (30s)...")
        pass_sample = page.locator("button:has-text('Compliant')").first
        if await pass_sample.is_visible():
            await pass_sample.hover()
            await pause(3)
            await pass_sample.click()
            await pause(5)

            submit_scan_btn = page.locator("button:has-text('Submit Proof & Trigger AI Scan')").first
            if await submit_scan_btn.is_visible():
                await submit_scan_btn.hover()
                await pause(3)
                await submit_scan_btn.click()
                # Watch animated scan, criteria checklist, confidence score & confetti
                await pause(12)

        # Scroll to inspect detailed AI checklist
        await page.mouse.wheel(0, 350)
        await pause(5)
        await page.mouse.wheel(0, -350)
        await pause(3)

        # ------------------------------------------------------------------
        # SCENE 6: Cryptographic Proof Ledger (2:05 - 2:25) ~20s
        # ------------------------------------------------------------------
        print("[Scene 6] Proof Ledger & Cryptographic Chain Verification (20s)...")
        ledger_tab = page.locator("button:has-text('Proof Ledger'), button:has-text('Ledger')").first
        await ledger_tab.hover()
        await pause(2)
        await ledger_tab.click()
        await pause(5)

        # Highlight verified badge
        await page.mouse.move(750, 160)
        await pause(3)

        # Scroll down through blockchain blocks
        await page.mouse.wheel(0, 450)
        await pause(5)
        await page.mouse.wheel(0, 450)
        await pause(5)
        await page.mouse.wheel(0, -900)
        await pause(3)

        # ------------------------------------------------------------------
        # SCENE 7: One-Click Dispute Defense Pack & PDF (2:25 - 2:45) ~20s
        # ------------------------------------------------------------------
        print("[Scene 7] Dispute Defense Pack & PDF Bundle (20s)...")
        client_tab = page.locator("button:has-text('Client Escrow'), button:has-text('Client')").first
        await client_tab.click()
        await pause(3)

        dispute_btn = page.locator("button:has-text('Dispute Pack')").first
        if await dispute_btn.is_visible():
            await dispute_btn.hover()
            await pause(2)
            await dispute_btn.click()
            await pause(6)

            # Hover over download PDF and copy JSON buttons
            pdf_btn = page.locator("button:has-text('Download Official PDF'), a:has-text('Download PDF'), button:has-text('Download PDF')").first
            if await pdf_btn.is_visible():
                await pdf_btn.hover()
                await pause(3)

            # Close modal cleanly
            await page.keyboard.press("Escape")
            await pause(1)
            close_btn = page.locator("button:has(svg.lucide-x)").first
            if await close_btn.is_visible():
                await close_btn.click()
                await pause(2)

        # ------------------------------------------------------------------
        # SCENE 8: Webhook Simulator & Closing Summary (2:45 - 2:55) ~10s
        # ------------------------------------------------------------------
        print("[Scene 8] Webhooks & Final Closing (10s)...")
        webhook_tab = page.locator("button:has-text('Webhook Simulator'), button:has-text('Webhooks')").first
        await webhook_tab.hover()
        await pause(2)
        await webhook_tab.click()
        await pause(6)

        # Return to main dashboard for clean finish
        await client_tab.click()
        await pause(4)

        print("Finished full demo script. Closing browser to generate video...")
        await page.close()
        await context.close()
        await browser.close()

    recorded_files = list(temp_dir.glob("*.webm"))
    if recorded_files:
        raw_video = recorded_files[0]
        final_mp4 = output_dir / "proofledger_demo_walkthrough_full.mp4"
        print(f"Recorded raw video to: {raw_video}")
        print("Encoding full high-quality 1080p MP4...")
        ffmpeg_cmd = f'ffmpeg -y -i "{raw_video}" -c:v libx264 -pix_fmt yuv420p -r 30 "{final_mp4}"'
        os.system(ffmpeg_cmd)
        print(f"SUCCESS! Full 3-minute video saved to: {final_mp4}")
    else:
        print("No video file captured.")

if __name__ == "__main__":
    asyncio.run(record_full_demo())

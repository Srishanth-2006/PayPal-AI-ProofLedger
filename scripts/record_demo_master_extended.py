import asyncio
import os
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

async def record_master_demo_extended():
    output_dir = Path(r"c:\Users\Srishanth S\Desktop\Sri folder\PayPal AI Hackathon\demo_recording")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_dir = output_dir / "temp_video_extended"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("Launching Playwright for EXTENDED 2:45 Master Recording...")
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
        # SCENE 1: Introduction & Client Escrow Dashboard (~22s)
        # ------------------------------------------------------------------
        print("[Scene 1] Dashboard Overview & Architecture Badges (22s)...")
        await page.goto("http://localhost:8000")
        await page.wait_for_load_state("networkidle")
        await pause(5)

        # Highlight Top Ribbon and PayPal Sandbox badge
        await page.mouse.move(960, 25)
        await pause(3)
        await page.mouse.move(1430, 70)
        await pause(3)

        # Smooth scrolling across all 4 milestone cards
        print("[Scene 1] Scrolling across all milestone states...")
        await page.mouse.wheel(0, 380)
        await pause(4)
        await page.mouse.wheel(0, 380)
        await pause(4)
        await page.mouse.wheel(0, -760)
        await pause(3)

        # ------------------------------------------------------------------
        # SCENE 2: Milestone Creation & AI Specifications (~28s)
        # ------------------------------------------------------------------
        print("[Scene 2] Milestone Creation & Contract Specifications (28s)...")
        create_btn = page.locator("button:has-text('+ New Milestone')").first
        if await create_btn.is_visible():
            await create_btn.hover()
            await pause(2)
            await create_btn.click()
            await pause(4)

            # Choose the Agentic AI Data Bounty template
            bounty_template = page.locator("button:has-text('Agentic AI Data Bounty')").first
            if await bounty_template.is_visible():
                await bounty_template.hover()
                await pause(2)
                await bounty_template.click()
                await pause(4)
            else:
                hvac_template = page.locator("button:has-text('HVAC Capacitor & Calibration')").first
                if await hvac_template.is_visible():
                    await hvac_template.click()
                    await pause(4)

            # Scroll inside modal to highlight AI specifications checklist
            await page.mouse.wheel(0, 250)
            await pause(5)
            await page.mouse.wheel(0, -250)
            await pause(3)

            # Submit milestone creation
            submit_create = page.locator("button:has-text('Create Escrow Milestone')").first
            if await submit_create.is_visible():
                await submit_create.hover()
                await pause(2)
                await submit_create.click()
                await pause(6)

        # ------------------------------------------------------------------
        # SCENE 3: PayPal Authorization Hold Flow (~16s)
        # ------------------------------------------------------------------
        print("[Scene 3] Demonstrating PayPal Authorization Lock (16s)...")
        lock_btn = page.locator("button:has-text('Lock Escrow')").first
        if await lock_btn.is_visible():
            await lock_btn.hover()
            await pause(2.5)
            await lock_btn.click()
            await pause(6)

            # Close PayPal modal
            close_paypal = page.locator("button:has(svg.lucide-x)").first
            if await close_paypal.is_visible():
                await close_paypal.click()
                await pause(3)

        # ------------------------------------------------------------------
        # SCENE 4: Contractor View & AI PASS (Auto-Capture) (~34s)
        # ------------------------------------------------------------------
        print("[Scene 4] Contractor View - Submitting Compliant Deliverable (34s)...")
        contractor_tab = page.locator("button:has-text('Contractor & AI Scanner'), button:has-text('AI Scanner')").first
        await contractor_tab.hover()
        await pause(2)
        await contractor_tab.click()
        await pause(5)

        # Select the HVAC milestone
        milestone_select = page.locator("select").first
        if await milestone_select.is_visible():
            try:
                await milestone_select.select_option(value="ms-hvac-7701")
                await pause(3)
            except Exception:
                pass

        # Select compliant sample
        pass_sample = page.locator("button:has-text('Compliant')").first
        if await pass_sample.is_visible():
            await pass_sample.hover()
            await pause(2.5)
            await pass_sample.click()
            await pause(4)

            # Trigger AI Scan
            submit_scan_btn = page.locator("button:has-text('Submit Proof & Trigger AI Scan')").first
            if await submit_scan_btn.is_visible():
                await submit_scan_btn.hover()
                await pause(2.5)
                await submit_scan_btn.click()
                # Watch live scanning animation, criteria verification & confetti auto-capture!
                await pause(12)

        # Scroll to inspect detailed criteria checklist with green checks
        await page.mouse.wheel(0, 380)
        await pause(5)
        await page.mouse.wheel(0, -380)
        await pause(3)

        # ------------------------------------------------------------------
        # SCENE 5: AI REJECTION & AUTO-VOID (~28s) ⭐ CRITICAL
        # ------------------------------------------------------------------
        print("[Scene 5] Submitting Deficient Deliverable (FAIL -> Auto-VOID) (28s)...")
        # Select the Industrial Chiller milestone
        if await milestone_select.is_visible():
            try:
                await milestone_select.select_option(value="ms-refrig-8805")
                await pause(3.5)
            except Exception:
                pass

        # Select the Deficient sample
        fail_sample = page.locator("button:has-text('Violation'), button:has-text('Deficient')").first
        if await fail_sample.is_visible():
            await fail_sample.hover()
            await pause(2.5)
            await fail_sample.click()
            await pause(4)

            # Trigger AI Scan on deficient proof
            if await submit_scan_btn.is_visible():
                await submit_scan_btn.hover()
                await pause(2.5)
                await submit_scan_btn.click()
                # Watch scanning animation detect deficiencies, score drop, and auto-void!
                await pause(11)

        # Scroll down to inspect AI failure reasoning & void notice
        await page.mouse.wheel(0, 380)
        await pause(5)
        await page.mouse.wheel(0, -380)
        await pause(3)

        # ------------------------------------------------------------------
        # SCENE 6: Human Override Controls (~12s)
        # ------------------------------------------------------------------
        print("[Scene 6] Human Override Controls (12s)...")
        client_tab = page.locator("button:has-text('Client Escrow'), button:has-text('Client')").first
        await client_tab.hover()
        await pause(2)
        await client_tab.click()
        await pause(4)

        # Hover over manual override buttons
        manual_btn = page.locator("button:has-text('Manual Release'), button:has-text('Manual Void')").first
        if await manual_btn.is_visible():
            await manual_btn.hover()
            await pause(4)

        # ------------------------------------------------------------------
        # SCENE 7: Cryptographic Proof Ledger (~16s)
        # ------------------------------------------------------------------
        print("[Scene 7] Proof Ledger & Cryptographic Integrity (16s)...")
        ledger_tab = page.locator("button:has-text('Proof Ledger'), button:has-text('Ledger')").first
        await ledger_tab.hover()
        await pause(2)
        await ledger_tab.click()
        await pause(4)

        # Highlight verified badge
        await page.mouse.move(750, 160)
        await pause(3)

        # Scroll through SHA-256 blocks showing BOTH captured & voided records
        await page.mouse.wheel(0, 500)
        await pause(5)
        await page.mouse.wheel(0, 500)
        await pause(5)
        await page.mouse.wheel(0, -1000)
        await pause(3)

        # ------------------------------------------------------------------
        # SCENE 8: Dispute Defense Pack & PDF Bundle (~14s)
        # ------------------------------------------------------------------
        print("[Scene 8] Dispute Defense Pack & PDF Evidence Bundle (14s)...")
        await client_tab.click()
        await pause(3)

        dispute_btn = page.locator("button:has-text('Dispute Pack')").first
        if await dispute_btn.is_visible():
            await dispute_btn.hover()
            await pause(2)
            await dispute_btn.click()
            await pause(6)

            # Hover over Download PDF button
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
        # SCENE 9: Webhook Simulator & Closing Wrap-up (~7s)
        # ------------------------------------------------------------------
        print("[Scene 9] Webhooks & Final Closing View (7s)...")
        webhook_tab = page.locator("button:has-text('Webhook Simulator'), button:has-text('Webhooks')").first
        await webhook_tab.hover()
        await pause(2)
        await webhook_tab.click()
        await pause(4)

        # Return to main dashboard for final shot
        await client_tab.click()
        await pause(4)

        print("Extended Master recording finished! Closing browser...")
        await page.close()
        await context.close()
        await browser.close()

    recorded_files = list(temp_dir.glob("*.webm"))
    if recorded_files:
        raw_video = recorded_files[0]
        final_mp4 = output_dir / "proofledger_master_demo_extended_2m45s.mp4"
        print(f"Recorded raw video to: {raw_video}")
        print("Encoding extended high-definition 1080p MP4...")
        ffmpeg_cmd = f'ffmpeg -y -i "{raw_video}" -c:v libx264 -pix_fmt yuv420p -r 30 "{final_mp4}"'
        os.system(ffmpeg_cmd)
        print(f"SUCCESS! Extended Master demo video saved to: {final_mp4}")
    else:
        print("No video file captured.")

if __name__ == "__main__":
    asyncio.run(record_master_demo_extended())
